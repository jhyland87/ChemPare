from suppliers.supplier_base import SupplierBase, TypeProduct, TypeSupplier
from typing import Dict, NoReturn
import pytest

pytest.skip(allow_module_level=True)


# File: /suppliers/supplier_template.py
class SupplierTemplate(SupplierBase):

    _supplier: TypeSupplier = dict(
        name="Template Example",
        location=None,
        base_url="https://www.chemical-company.com",
        api_url="https://api.chemical-company.com",
    )
    """Supplier specific data"""

    allow_cas_search: bool = True
    """Determines if the supplier allows CAS searches in addition to name searches"""

    def _setup(self, query: str = None) -> NoReturn:
        """Setup any cookies or header override values here. What's defined in self._headers and
        self._cookies will be included in all subsequent calls.
        """

        headers = self.http_get_headers()
        # cookies = list(v  for k, v in headers.multi_items() if k == 'set-cookie') or None

        self._headers["authorization"] = headers["auth_token"]

    def _query_products(self, query: str):
        """Query products from supplier

        Args:
            query (str): Query string to use
        """

        params = {"term": query}

        search_result = self.http_get_json(path="path/from/root/query", params=params)
        # search_result = self.http_post_json(path=f'path/from/root/query', json={})

        if not search_result:
            return

        self._query_results = search_result["results"]

    # Method iterates over the product query results stored at self._query_results and
    # returns a list of TypeProduct objects.
    def _parse_products(self) -> NoReturn:
        """Iterate over the self._query_results list, running the parser for each and adding the
        returned TypeProduct object to self._products
        """

        for product_obj in self._query_results:
            # Add each product to the self._products list in the form of a TypeProduct
            # object.
            self._products.append(self._parse_product(product_obj))

    def _parse_product(self, product_obj: Dict) -> TypeProduct:
        """Parse single product and return single TypeProduct object

        Args:
            product_obj (Dict): Single product object from JSON body

        Returns:
            TypeProduct: Instance of TypeProduct

        Todo:
            - It looks like each product has a shopify_variants array that stores data
              about the same product but in different quantities. This could maybe be
              included?
        """

        product = TypeProduct(
            uuid=product_obj["id"],
            name=product_obj["title"],
            title=product_obj["title"],
            description=product_obj["description"],
            price=product_obj["discountedPrice"],
            url="{0}{1}".format(self._supplier["base_url"], product_obj["url"]),
            supplier=self._supplier["name"],
            currency=product_obj["currency"],
        )

        return product


if __package__ == "suppliers":
    __disabled__ = True
