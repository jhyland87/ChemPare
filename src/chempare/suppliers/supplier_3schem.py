from chempare.datatypes import ProductType
from chempare.datatypes import SupplierType
from chempare.suppliers.supplier_base import SupplierBase


# File: /suppliers/supplier_3schem.py
class Supplier3SChem(SupplierBase):
    _limit: int = 20

    _supplier: SupplierType = SupplierType(
        name="3S Chemicals LLC", location=None, base_url="https://3schemicalsllc.com"
    )
    """Supplier specific data"""

    def _query_products(self, query: str) -> None:
        """Query products from supplier

        Args:
            query (str): Query string to use
        """

        # Example request url for 3S Supplier
        # https://3schemicalsllc.com/search/suggest.json?
        #   q=clean
        #   &resources[type]=product
        #   &resources[limit]=6
        #   &resources[options][unavailable_products]=last
        #
        get_params = {
            "q": query,
            "resources[type]": "product",
            # Setting the limit here to 1000, since the limit parameter should
            # apply to results returned from Supplier3SChem, not the rquests
            # made by it.
            "resources[limit]": 1000,
            "resources[options][unavailable_products]": "last",
        }

        search_result = self.http_get_json("search/suggest.json", params=get_params)

        if not search_result:
            return

        self._query_results = search_result.get('resources', {}).get('results', {}).get('products', [])[: self._limit]

    def _parse_products(self) -> None:
        """Parse products stored at self._query_results"""
        for product in self._query_results:
            # Skip unavailable
            if product.get("available") is False:
                continue

            product_obj = dict(
                uuid=product.get("id"),
                name=product.get("title"),
                title=product.get("title"),
                price=product.get("price"),
                currency="$",
                currency_code="UAT",
                url=self._supplier.base_url + product.get("url"),
                supplier=self._supplier.name,
            )

            # price = self._parse_price(product.get("price"))

            # if not price:
            #     continue

            # product_obj.update(price)

            # print("product_obj:", product_obj)

            self._products.append(ProductType(**product_obj))


__supplier_class = Supplier3SChem

if __package__ == "suppliers":
    __disabled__ = False
