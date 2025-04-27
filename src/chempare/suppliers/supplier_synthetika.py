from __future__ import annotations

import re
from typing import TYPE_CHECKING

from chempare.suppliers.supplier_base import SupplierBase
from chempare.utils import _currency

if TYPE_CHECKING:
    from typing import Any, ClassVar, Final

    from datatypes import ProductType, SupplierType


# File: /suppliers/supplier_synthetika.py
class SupplierSynthetika(SupplierBase):

    _limit: ClassVar[int] = 20
    """Max results to store"""

    _supplier: Final[SupplierType] = {
        "name": "Synthetika",
        "location": "Eu",
        "base_url": "https://synthetikaeu.com",
        "api_url": "https://synthetikaeu.com",
    }
    """Supplier specific data"""

    allow_cas_search: ClassVar[bool] = True
    """Determines if the supplier allows CAS searches in addition to name
    searches"""

    def _query_products(self) -> None:
        """Query products from supplier"""

        def __query_list(query: str, page: int = 1) -> None:
            """Query list of products on page

            Args:
                query (str): Query string
                page (int, optional): Page number. Defaults to 1.

            Returns:
                None: Nothing, just appends data to self._query_results and
                          executes self.__query_list() again if needed
            """

            # Example request url for Synthetika
            # https://synthetikaeu.com/webapi/front/en_US/search/short-list/products?text=borohydride&org=borohydride&page=1
            #
            get_params: dict[str, str | int] = {
                # Setting the limit here to 1000, since the limit parameter
                # should apply to results returned from Supplier3SChem, not the
                # rquests made by it.
                "org": query,
                "text": query,
                "page": page,
            }

            search_result: dict[str, Any] = self.http_get_json(
                "webapi/front/en_US/search/short-list/products", params=get_params
            )

            if not search_result:
                return

            self._query_results.extend(search_result["list"])

            if int(search_result["pages"]) > page and len(self._query_results) < self._limit:
                __query_list(query, page + 1)

        __query_list(self._query, 1)

    # Method iterates over the product query results stored at
    # self._query_results and returns a list of ProductType objects.
    def _parse_products(self) -> None:
        for product_obj in self._query_results:

            # Add each product to the self._products list in the form of a
            # ProductType object.
            if product := self._parse_product(product_obj):
                self._products.append(product)

    def _parse_product(self, product_obj: dict[str, Any]) -> ProductType | None:
        """Parse single product and return single ProductType object

        Args:
            product_obj (tuple[list, dict]): Single product object from the
                                             JSON body

        Returns:
            ProductType: Instance of ProductType

        Todo:
            - It looks like each product has a shopify_variants array that
              stores data about the same product but in different quantities.
              This could maybe be included?
        """

        quantity_pattern = re.compile(
            r"(?P<quantity>[0-9,\.x]+)\s?"
            r"(?P<uom>[gG]allon|gal|k?g|[cmμ]m|m?[lL])"
        )

        if (not (price_obj := _currency.parse_price(product_obj["price"]))
            or "price" not in price_obj
            or "currency" not in price_obj
            or not (quantity_matches := quantity_pattern.search(product_obj["name"]))
            or not (quantity_matches := quantity_matches.groupdict())
            or not (uom := quantity_matches.get("uom", None))
            or not (quantity := quantity_matches.get("quantity", None))):
            return None

        product: ProductType = {
            "uuid": product_obj["product_code"],
            "name": product_obj["name"],
            "title": product_obj["name"],
            "url": f"{self._supplier["base_url"]}{product_obj["url"]}",
            "manufacturer": product_obj["attributes"].get("producer_name", None),
            "supplier": self._supplier["name"],
            "quantity": float(quantity),
            "uom": uom,
            "price": price_obj["price"],
            "currency": price_obj["currency"]
        }

        return product
