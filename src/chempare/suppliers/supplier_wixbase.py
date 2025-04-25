"""Base class for wix websites"""
from __future__ import annotations

import json
from typing import TYPE_CHECKING

import chempare.utils as utils
import regex
from chempare.exceptions import ProductListQueryError
from chempare.suppliers import SupplierBase

if TYPE_CHECKING:
    from datatypes import ProductType
    from typing import Any


class SupplierWixBase(SupplierBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _setup(self):
        if not hasattr(self, '_headers') or not isinstance(self._headers, dict):
            self._headers = {}

        if not hasattr(self, '_cookies') or not isinstance(self._cookies, dict):
            self._cookies = {}

        # 1 Get the session binding from the initial request headers
        headers = self.http_get_headers(
            "/", headers={"sec-fetch-mode": "navigate", "sec-fetch-dest": "document", "sec-fetch-site": "none"}
        )
        if "set-cookie" not in headers:
            raise LookupError("Expected to find set-cookie in response headers")

        cookies = utils.split_set_cookie(headers.get("set-cookie", ""))

        for cookie in cookies:
            cookie_data = utils.parse_cookie(cookie)

            if cookie_data.get("name") == "ssr-caching" or cookie_data.get("name") == "server-session-bind":
                self._cookies[cookie_data.get("name")] = cookie_data.get("value")
                continue

            if cookie_data.get("name") == "client-session-bind":
                self._headers["client-binding"] = cookie_data.get("value")
                continue

        # 2 Get the XSRF id thingy
        xsrf_token_headers = self.http_get_headers(
            "_api/wix-laboratory-server/laboratory/conductAllInScope",
            params={"scope": "wix-one-app"},
            cookies=self._cookies,
            headers=self._headers,
        )

        # xsrf_header_cookies = list(v for k, v in xsrf_token_headers.multi_items() if k == "set-cookie") or None
        xsrf_header_cookies = utils.split_set_cookie(xsrf_token_headers.get("set-cookie", ""))

        for xsrf_cookie in xsrf_header_cookies:
            if "XSRF-TOKEN" not in xsrf_cookie:
                continue

            cookie_data = utils.parse_cookie(xsrf_cookie)

            if cookie_data.get("name") != "XSRF-TOKEN":
                continue

            self._headers["XSRF-TOKEN"] = cookie_data.get("value")
            self._cookies["XSRF-TOKEN"] = cookie_data.get("value")
            break

        # 3 Get the website instance ID ("access tokens")
        auth = self.http_get_json("_api/v1/access-tokens", cookies=self._cookies, headers=self._headers)

        self._headers["Authorization"] = utils.get_nested(
            auth, "apps", "1380b703-ce81-ff05-f115-39571d94dfcd", "instance"
        )

    def _query_products(self):
        query_params = {
            "o": "getFilteredProducts",
            "s": "WixStoresWebClient",
            # Below is a GraphQL structure
            "q": """\
                query,getFilteredProductsWithHasDiscount(
                    $mainCollectionId:String\u0021,
                    $filters:ProductFilters,
                    $sort:ProductSort,
                    $offset:Int,
                    $limit:Int,
                    $withOptions:Boolean,=,false,
                    $withPriceRange:Boolean,=,false
                ){
                    catalog{
                        category(categoryId:$mainCollectionId){
                            numOfProducts,
                            productsWithMetaData(
                                filters:$filters,
                                limit:$limit,
                                sort:$sort,
                                offset:$offset,
                                onlyVisible:true
                            ){
                                totalCount,
                                list{
                                    id,
                                    options{
                                        id,key,title,@include(if:$withOptions),
                                        optionType,@include(if:$withOptions),
                                        selections,@include(if:$withOptions){
                                            id,value,description,key,inStock
                                        }
                                    }
                                    productItems,
                                    @include(if:$withOptions){
                                        id,optionsSelections,price,formattedPrice
                                    }
                                    productType,price,sku,isInStock,urlPart,
                                    formattedPrice,name,description,brand,
                                    priceRange(withSubscriptionPriceRange:true),
                                    @include(if:$withPriceRange){
                                        fromPriceFormatted
                                    }
                                }
                            }
                        }
                    }
                }
            """,
            # Query used with the above GraphQL structure
            "v": {
                "mainCollectionId": "00000000-000000-000000-000000000001",
                "offset": 0,
                "limit": 100,
                "sort": None,
                "filters": {"term": {"field": "name", "op": "CONTAINS", "values": [f"*{self._query}*"]}},
                "withOptions": True,
                "withPriceRange": False,
            },
        }

        query_params["q"] = regex.sub(r"\n?\s*", "", query_params["q"])
        query_params["v"] = json.dumps(query_params["v"])
        search_result = self.http_get_json(
            "_api/wix-ecommerce-storefront-web/api", params=query_params, headers=self._headers, cookies=self._cookies
        )

        if not search_result:
            raise ProductListQueryError(
                supplier=self._supplier.get('name'), url="_api/wix-ecommerce-storefront-web/api"
            )

        self._query_results = utils.get_nested(
            search_result, "data", "catalog", "category", "productsWithMetaData", "list"
        )

    def _parse_products(self) -> None:
        for product_obj in self._query_results:

            # Add each product to the self._products list in the form of a
            # ProductType object.
            product = self._parse_product(product_obj)

            self._products.append(product)

    def _parse_product(self, product_obj: dict[str, Any]) -> ProductType:
        """
        Parse single product and return single ProductType object

        Args:
            product_obj (dict): Single product object from JSON body

        Returns:
            ProductType: Instance of ProductType

        Todo:
            - It looks like each product has a shopify_variants array that
              stores data about the same product but in different quantities.
              This could maybe be included?
        """

        qty = utils.parse_quantity(product_obj["options"][0]["selections"][0]["value"])

        price = utils.parse_price(product_obj["productItems"][0]["formattedPrice"])

        product: ProductType = {
            # "uuid": product_obj.get("id"),
            "title": str(product_obj.get("name")),
            "description": str(product_obj.get("description")),
            "url": f"${self._supplier["base_url"]}/product-page/{product_obj["urlPart"]}",
            "supplier": self._supplier["name"],
            "currency": "USD",
            "cas": utils.find_cas(str(product_obj.get("name"))),
            "quantity": qty.get("quantity", None),
            "uom": qty.get("uom", None),
            "price": price.get("price"),
        }

        # if qty is not None:
        #     product.update(qty)

        # if price is not None:
        #     product.update(price)

        return product
