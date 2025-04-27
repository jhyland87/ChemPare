from __future__ import annotations

import json
from typing import TYPE_CHECKING

from bs4 import BeautifulSoup

from chempare.suppliers.supplier_base import SupplierBase
from chempare.utils import _general, _quantity

if TYPE_CHECKING:
    from typing import ClassVar, Final

    from datatypes import SupplierType


# File: /suppliers/supplier_3schem.py
class Supplier3SChem(SupplierBase):
    _limit: ClassVar[int] = 20

    _supplier: Final[SupplierType] = {"name": "3S Chemicals LLC", "base_url": "https://3schemicalsllc.com"}
    """Supplier specific data"""

    def _query_products(self) -> None:
        """Query products from supplier"""

        # Example request url for 3S Supplier
        # https://3schemicalsllc.com/search/suggest.json?
        #   q=clean
        #   &resources[type]=product
        #   &resources[limit]=6
        #   &resources[options][unavailable_products]=last
        #
        get_params = {
            "q": self._query,
            "resources[type]": "product",
            # Setting the limit here to 1000, since the limit parameter should
            # apply to results returned from Supplier3SChem, not the rquests
            # made by it.
            "resources[limit]": 1000,
            "resources[options][unavailable_products]": "last",
        }

        if not (search_result := self.http_get_json("search/suggest.json", params=get_params)):
            return

        self._query_results = (
            search_result
            .get('resources', {})
            .get('results', {})
            .get('products', [])[: self._limit]
        )

    def _parse_products(self) -> None:
        """Parse products stored at self._query_results"""
        for product in self._query_results:
            # Skip unavailable
            if product.get("available") is False:
                continue

            if not (product_json := self._get_product_data(
                url=product.get("url"),
                product_id=product.get("id"))
            ):
                raise ValueError("Failed to retrieve the product page for product")

            quantity= _quantity.parse_quantity(
                _general.get_nested(product_json, "variants[0].options[0]", default="")
            )

            product_obj = {
                "uuid": product.get("id"),
                "title": product.get("title"),
                "price": product_json["variants"][0]["price"],
                "currency_symbol": "$",
                "currency": "USD",
                "url": self._supplier["base_url"] + product.get("url"),
                "supplier": self._supplier["name"],
                "quantity": quantity.get("quantity"),
                "uom": quantity.get("uom", ""),
                # **quantity.__dict__,
            }

            self._products.append(product_obj)

    def _get_product_data(self, url: str, product_id: int) -> dict | None:
        """
        _get_product_data Get specific info about a product

        Some additional info is stored in a <script/> element with the product ID in
        the class name. The content is in JSON format and can easily be retrieved. This
        also contains the variant information.

        :param url: URL of product
        :type url: str
        :param product_id: ID of product
        :type product_id: int
        :return: Parsed JSON object for product
        :rtype: dict
        """
        product_page = self.http_get_html(url)

        product_page_soup = BeautifulSoup(product_page, "html.parser")

        product_data_elem = product_page_soup.select_one(
            f"script.ProductJson-{product_id}"
        )
        if not product_data_elem:
            return None

        return json.loads(product_data_elem.text)


__disabled__ = False
