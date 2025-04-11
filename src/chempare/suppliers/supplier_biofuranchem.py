# pylint: disable=unreachable
from typing import Dict

from chempare.datatypes import TypeProduct
from chempare.datatypes import TypeSupplier
from chempare.suppliers.supplier_base import SupplierBase


# File: /suppliers/supplier_biofuranchem.py
class SupplierBioFuranChem(SupplierBase):

    _supplier: TypeSupplier = TypeSupplier(
        name="BioFuran Chem",
        location=None,
        base_url="https://www.biofuranchem.com",
        api_url="https://www.biofuranchem.com",
    )
    """Supplier specific data"""

    allow_cas_search: bool = True
    """Determines if the supplier allows CAS searches in addition to name
    searches"""

    # If any extra init logic needs to be called... uncmment the below and add
    # changes
    # def __init__(self, query, limit=123):
    #     super().__init__(id, query, limit)
    # Do extra stuff here

    def _setup(self, query: str | None = None) -> None:
        # 1 Get the session binding from the initial request headers
        headers = self.http_get_headers(
            "/shop",
            headers={
                "sec-fetch-mode": "navigate",
                "sec-fetch-dest": "document",
                "sec-fetch-site": "none",
            },
        )
        cookies = (
            list(v for k, v in headers.multi_items() if k == "set-cookie")
            or None
        )

        auth_cookies = {}
        auth_headers = {}

        if cookies:
            for cookie in cookies:
                segs = cookie.split("=")
                name = segs[0]
                val = "=".join(segs[1:-1])

                if name == "ssr-caching" or name == "server-session-bind":
                    auth_cookies[name] = val.split(";")[0]
                    continue

                if name == "client-session-bind":
                    auth_headers["client-binding"] = val.split(";")[0]
                    continue

        # 2 Get the XSRF id thingy
        xsrf_token_headers = self.http_get_headers(
            "_api/wix-laboratory-server/laboratory/conductAllInScope",
            params={"scope": "wix-one-app"},
            cookies=auth_cookies,
            headers=auth_headers,
        )

        xsrf_header_cookies = (
            list(
                v
                for k, v in xsrf_token_headers.multi_items()
                if k == "set-cookie"
            )
            or None
        )

        for xsrf_cookie in xsrf_header_cookies:
            segs = xsrf_cookie.split("=")
            name = segs[0]
            val = "=".join(segs[1:-1])

            if name == "XSRF-TOKEN":
                auth_cookies[name] = val.split(";")[0]
                self._headers["XSRF-TOKEN"] = val.split(";")[0]
                break

        # 3 Get the website instance ID ("access tokens")
        auth = self.http_get_json(
            "_api/v1/access-tokens", cookies=auth_cookies, headers=auth_headers
        )

        self._headers["Authorization"] = auth["apps"][
            "1380b703-ce81-ff05-f115-39571d94dfcd"
        ]["instance"]

    def _query_products(self, query: str) -> None:
        """Query products from supplier

        Args:
            query (str): Query string to use

        Todo:
            - It looks like FTF will return more results than expected when
              searching via CAS. For example, if you search for 598-21-0, you
              will get Bromoacetybromide as the first result along with 224
              products that do not have the same CAS. It might be a good idea
              to add some logic to the FTF module that will _only_ return the
              item(s) with the matching CAS if a CAS search was used.
        """

        query_params = {
            "o": "getFilteredProducts",
            "s": "WixStoresWebClient",
            # Below is a GraphQL structure
            "q": """\
                query,getFilteredProductsWithHasDiscount(
                    $mainCollectionId:String!,
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
                "filters": {
                    "term": {
                        "field": "name",
                        "op": "CONTAINS",
                        "values": [f"*'{self._query}'*"],
                    }
                },
                "withOptions": True,
                "withPriceRange": False,
            },
        }

        search_result = self.http_get_json(
            "_api/wix-ecommerce-storefront-web/api", params=query_params
        )

        if not search_result:
            return

        self._query_results = search_result["data"]["catalog"]["category"][
            "productsWithMetaData"
        ]["list"]

    # Method iterates over the product query results stored at
    # self._query_results and returns a list of TypeProduct objects.
    def _parse_products(self) -> None:
        for product_obj in self._query_results:

            # Add each product to the self._products list in the form of a
            # TypeProduct object.
            product = self._parse_product(product_obj)

            self._products.append(product)

    def _parse_product(self, product_obj: Dict) -> TypeProduct:
        """Parse single product and return single TypeProduct object

        Args:
            product_obj (Dict): Single product object from JSON body

        Returns:
            TypeProduct: Instance of TypeProduct

        Todo:
            - It looks like each product has a shopify_variants array that
              stores data about the same product but in different quantities.
              This could maybe be included?
        """

        product = dict(
            uuid=product_obj["id"],
            name=product_obj["name"],
            title=product_obj["name"],
            description=product_obj["description"],
            url=f"https://www.biofuranchem.com/product-page/{product_obj["urlPart"]}",
            supplier=self._supplier.name,
            currency="$",
            cas=self._find_cas(str(product_obj["name"])),
        )

        qty = (
            self._parse_quantity(
                product_obj["options"][0]["selections"][0]["value"]
            )
            or {}
        )

        price = (
            self._parse_price(product_obj["productItems"][0]["formattedPrice"])
            or {}
        )

        product.update(dict(**qty, **price))
        product = TypeProduct(**product)
        return product.cast_properties()


if __package__ == "suppliers":
    __disabled__ = False
