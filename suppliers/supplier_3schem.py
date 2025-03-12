from suppliers.supplier_base import SupplierBase, TypeProduct, TypeSupplier
from typing import NoReturn


# File: /suppliers/supplier_3schem.py
class Supplier3SChem(SupplierBase):

    _supplier: TypeSupplier = dict(
        name="3S Chemicals LLC", location=None, base_url="https://3schemicalsllc.com"
    )
    """Supplier specific data"""

    def _query_products(self, query) -> NoReturn:
        """Query products from supplier

        Args:
            query (str): Query string to use
        """

        # Example request url for 3S Supplier
        # https://3schemicalsllc.com/search/suggest.json?q=clean&resources[type]=product&resources[limit]=6&resources[options][unavailable_products]=last
        #
        get_params = {
            "q": query,
            "resources[type]": "product",
            # Setting the limit here to 1000, since the limit parameter should apply to
            # results returned from Supplier3SChem, not the rquests made by it.
            "resources[limit]": 1000,
            "resources[options][unavailable_products]": "last",
        }
        search_result = self.http_get_json("search/suggest.json", params=get_params)

        if not search_result:
            return

        self._query_results = search_result["resources"]["results"]["products"][
            0 : self._limit
        ]

    def _parse_products(self) -> NoReturn:
        """Parse products stored at self._query_results"""
        for product in self._query_results:
            # Skip unavailable
            if product["available"] is False:
                continue

            self._products.append(
                TypeProduct(
                    uuid=product["id"],
                    name=product["title"],
                    title=product["title"],
                    price=product["price"],
                    url=self._supplier["base_url"] + product["url"],
                    supplier=self._supplier["name"],
                )
            )


if __package__ == "suppliers":
    __disabled__ = False
