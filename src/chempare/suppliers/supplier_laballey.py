from typing import List, Tuple, Dict, NoReturn
from chempare.suppliers.supplier_base import SupplierBase
from chempare.datatypes import TypeProduct, TypeSupplier


# File: /suppliers/supplier_laboratoriumdiscounter.py
class SupplierLaballey(SupplierBase):

    _supplier: TypeSupplier = dict(
        name="Laballey",
        location=None,
        base_url="https://www.laballey.com",
        api_url="https://searchserverapi.com",
        api_key="8B7o0X1o7c",
    )
    """Supplier specific data"""

    allow_cas_search: bool = True
    """Determines if the supplier allows CAS searches in addition to name
    searches"""

    __defaults: Dict = {
        "currency": "$",
        "currency_code": "USD",
        "is_restricted": False,
    }
    """Default values applied to products from this supplier"""

    def _query_products(self, query: str) -> NoReturn:
        """Query products from supplier

        Args:
            query (str): Query string to use
        """

        # Example request url for Laboratorium Discounter
        # https://searchserverapi.com/getwidgets?
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
        get_params = {
            # Setting the limit here to 1000, since the limit parameter should
            # apply to results returned from Supplier3SChem, not the rquests
            # made by it.
            "api_key": self._supplier["api_key"],
            "q": query,
            "maxResults": 6,
            "startIndex": 0,
            "items": True,
            "pages": False,
            "facets": False,
            "categories": True,
            "suggestions": True,
            "vendors": False,
            "tags": False,
            "pageStartIndex": 0,
            "pagesMaxResults": 10,
            "categoryStartIndex": 0,
            "categoriesMaxResults": 3,
            "suggestionsMaxResults": 4,
            "vendorsMaxResults": 3,
            "tagsMaxResults": 3,
            "output": "json",
            "_": self._epoch,
        }

        search_result = self.http_get_json("getwidgets", params=get_params)

        if not search_result:
            return

        self._query_results = search_result["items"][: self._limit]

    # Method iterates over the product query results stored at
    # self._query_results and returns a list of TypeProduct objects.
    def _parse_products(self) -> NoReturn:
        for product_obj in self._query_results:
            # Add each product to the self._products list in the form of a
            # TypeProduct object.
            self._products.append(self._parse_product(product_obj))

    def _parse_product(self, product_obj: Tuple[List, Dict]) -> TypeProduct:
        """Parse single product and return single TypeProduct object

        Args:
            product_obj (Tuple[List, Dict]): Single product object from JSON

        Returns:
            TypeProduct: Instance of TypeProduct

        Todo:
            - It looks like each product has a shopify_variants array that
              stores data about the same product but in different quantities.
              This could maybe be included?
        """

        product = TypeProduct(
            **self.__defaults,
            uuid=product_obj["product_id"],
            name=product_obj["title"],
            title=product_obj["title"],
            description=(
                str(product_obj["description"]).strip()
                if product_obj["description"]
                else None
            ),
            price=f"{float(product_obj['price']):.2f}",
            url="{0}{1}".format(
                self._supplier["base_url"], product_obj["link"]
            ),
            manufacturer=product_obj["vendor"],
            supplier=self._supplier["name"],
        )

        quantity_matches = self._parse_quantity(product_obj["product_code"])

        if quantity_matches:
            product.update(quantity_matches)

        return product


if __package__ == "suppliers":
    __disabled__ = False
