import os

from chempare.datatypes import ProductType
from chempare.datatypes import SupplierType
from chempare.suppliers.supplier_base import SupplierBase


# File: /suppliers/supplier_laboratoriumdiscounter.py
class SupplierLaballey(SupplierBase):

    _supplier: SupplierType = SupplierType(
        name="Laballey",
        base_url="https://www.laballey.com",
        api_url="https://searchserverapi.com",
        api_key="8B7o0X1o7c",
    )
    """Supplier specific data"""

    allow_cas_search: bool = True
    """Determines if the supplier allows CAS searches in addition to name
    searches"""

    __defaults: dict = {"currency": "$", "currency_code": "USD", "is_restricted": False}
    """Default values applied to products from this supplier"""

    def _query_products(self, query: str) -> None:
        """Query products from supplier

        Args:
            query (str): Query string to use
        """

        # Example request url for Laboratorium Discounter
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
        epoch_ts = self._epoch

        if os.environ.get("PYTEST_VERSION") is not None:
            epoch_ts = 1234567890

        get_params = {
            # Setting the limit here to 1000, since the limit parameter should
            # apply to results returned from Supplier3SChem, not the rquests
            # made by it.
            "api_key": self._supplier.api_key,
            "q": query,
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

        product = ProductType(
            **self.__defaults,
            uuid=product_obj.get("product_id"),
            name=product_obj.get("title"),
            title=product_obj.get("title"),
            description=str(product_obj.get("description", "")).strip() or None,
            price=f"{float(product_obj.get("price")):.2f}",
            url="{0}{1}".format(self._supplier.base_url, product_obj.get("link")),
            manufacturer=product_obj.get("vendor"),
            supplier=self._supplier.name,
        )

        quantity_matches = self._parse_quantity(product_obj.get("product_code"))

        if quantity_matches:
            product.update(quantity_matches)

        return product


__supplier_class = SupplierLaballey
