from __future__ import annotations

from chempare.suppliers.supplier_base import SupplierBase
from datatypes import ProductType
from datatypes import SupplierType


# File: /suppliers/supplier_labchemde.py
class SupplierLabchemDe(SupplierBase):

    _supplier: SupplierType = SupplierType(
        name="Labchem (de)", base_url="https://www.labchem.de", api_url="https://www.labchem.de"
    )
    """Supplier specific data"""

    allow_cas_search: bool = True
    """Determines if the supplier allows CAS searches in addition to name
    searches"""

    __defaults: dict = {
        "currency_symbol": "€",
        "currency": "EUR",
        # "is_restricted": False,
    }
    """Default values applied to products from this supplier"""

    def _query_products(self) -> None:
        """Query products from supplier

        Args:
            query (str): Query string to use
        """
        params = {"shop": 87762263, "resultsPerPage": 12, "page": 1, "locale": "de_DE"}
        post_json = {"filters": [], "query": self._query, "sort": "relevance"}

        # curl -s 'https://www.labchem.de/api/v2/search?shop=87762263&resultsPerPage=12&page=1&locale=de_DE' \
        #   -H 'Accept: application/json, text/plain, */*' \
        #   --data-raw '{"filters":[],"query":"acet","sort":"relevance"}'

        self._query_results = self.http_post_json("api/v2/search", json=post_json, params=params)

    # Method iterates over the product query results stored at
    # self._query_results and returns a list of ProductType objects.
    def _parse_products(self) -> None:
        for product_obj in self._query_results.get('products'):
            # Add each product to the self._products list in the form of a
            # ProductType object.
            product_result = self._query_and_parse_product(product_obj)
            self._products.append(product_result)

    def _query_and_parse_product(self, product_obj: tuple[list, dict]) -> ProductType:
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

        if (price := product_obj.get("price")) is None:
            price = product_obj.get("lowestPrice")

        product: ProductType = {
            # **self.__defaults,
            "supplier": self._supplier["name"],
            "url": product_obj.get("url"),
            "quantity": product_obj.get("orderUnitInfo", {}).get("priceQuantity"),
            "uom": product_obj.get("orderUnitInfo", {}).get("orderUnit"),
            "name": product_obj.get("name"),
            "title": product_obj.get("title"),
            "uuid": product_obj.get("productId"),
            "sku": product_obj.get("sku"),
            "description": product_obj.get("description"),
            "currency": self.__defaults["currency"],
            "price": price,
        }

        # price_data = utils.parse_price(price.get("formatted"))

        # product.update(price_data.__dict__)

        # product = ProductType(**product)

        # return product.cast_properties()
        return product
