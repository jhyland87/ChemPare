from __future__ import annotations

import os

from chempare.suppliers.supplier_base import SupplierBase

import chempare.utils as utils
from datatypes import ProductType


# File: /suppliers/supplier_shopifybase.py.py
class SupplierShopifyBase(SupplierBase):

    allow_cas_search: bool = True
    """Determines if the supplier allows CAS searches in addition to name
    searches"""

    __defaults: dict = {"currency": "$", "currency_code": "USD", "is_restricted": False}
    """Default values applied to products from this supplier"""

    def _query_products(self) -> None:
        """Query products from supplier"""

        # https://searchserverapi.com/getresults?
        #   api_key=8B7o0X1o7c
        #   &q=sulf
        #   &maxResults=6
        #   &startIndex=0
        #   &items=true
        #   &pages=true
        #   &facets=false
        #   &categories=true
        #   &suggestions=true
        #   &vendors=false
        #   &tags=false
        #   &pageStartIndex=0
        #   &pagesMaxResults=3
        #   &categoryStartIndex=0
        #   &categoriesMaxResults=3
        #   &suggestionsMaxResults=4
        #   &vendorsMaxResults=3
        #   &tagsMaxResults=3
        #   &output=json
        #   &_=1740051794061
        #
        epoch_ts = utils.epoch()

        if os.environ.get("PYTEST_VERSION") is not None:
            epoch_ts = 1234567890

        get_params = {
            # Setting the limit here to 1000, since the limit parameter should
            # apply to results returned from Supplier3SChem, not the rquests
            # made by it.
            "api_key": self._supplier["api_key"],
            "q": self._query,
            "maxResults": 15,
            "startIndex": 0,
            "items": True,
            "pages": True,
            "facets": True,
            "categories": True,
            "suggestions": True,
            "vendors": True,
            "tags": True,
            "pageStartIndex": 0,
            "pagesMaxResults": 15,
            "categoryStartIndex": 0,
            "categoriesMaxResults": 3,
            "suggestionsMaxResults": 4,
            "vendorsMaxResults": 4,
            "tagsMaxResults": 3,
            "output": "json",
            "_": epoch_ts,
        }

        search_result = self.http_get_json("getresults", params=get_params)

        if not search_result:
            return

        self._query_results = search_result["items"][: self._limit]

    # Method iterates over the product query results stored at
    # self._query_results and returns a list of ProductType objects.
    def _parse_products(self) -> None:
        for product_obj in self._query_results:
            # Add each product to the self._products list in the form of a
            # ProductType object.
            self._products.append(self._parse_product(product_obj))

    def _parse_product(self, product_obj: tuple[list, dict]) -> ProductType:
        """Parse single product and return single ProductType object

        Args:
            product_obj (tuple[list, dict]): Single product object from JSON

        Returns:
            ProductType: Instance of ProductType

        Todo:
            - It looks like each product has a shopify_variants array that
              stores data about the same product but in different quantities.
              This could maybe be included?
        """

        quantity_matches = utils.parse_quantity(product_obj.get("product_code"))

        uom = "item(s)"
        quantity = product_obj.get("quantity")

        if quantity_matches:
            uom = getattr(quantity_matches, "uom", uom)
            quantity = getattr(quantity_matches, "quantity", quantity)

        price = float(product_obj.get("price"))
        product = {
            # **self.__defaults,
            "uuid": product_obj.get("product_id"),
            "name": product_obj.get("title"),
            "title": product_obj.get("title"),
            "description": str(product_obj.get("description", "")).strip() or None,
            "price": f"{price:.2f}",
            "url": "{}{}".format(self._supplier["base_url"], product_obj.get("link")),
            "manufacturer": product_obj.get("vendor"),
            "supplier": self._supplier["name"],
            "quantity": quantity,
            "uom": uom,
        }

        utils.set_multiple_defaults(product, self.__defaults)
        return product
