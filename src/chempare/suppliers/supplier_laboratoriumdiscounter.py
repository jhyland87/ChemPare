from chempare.datatypes import TypeProduct
from chempare.datatypes import TypeSupplier
from chempare.exceptions import NoProductsFound
from chempare.suppliers.supplier_base import SupplierBase


# File: /suppliers/supplier_laboratoriumdiscounter.py
class SupplierLaboratoriumDiscounter(SupplierBase):
    """
    Todo:
        Creat a method that can query and parse individual products. This can
        be done by just taking the product page URL and appending ?format=json:
            https://www.laboratoriumdiscounter.nl/en/lithium-borohydride-ca-4mol-l-in-tetrahydrofuran-1.html?format=json
    """

    _supplier: TypeSupplier = TypeSupplier(
        name="Laboratorium Discounter", base_url="https://www.laboratoriumdiscounter.nl"
    )
    """Supplier specific data"""

    allow_cas_search: bool = True
    """Determines if the supplier allows CAS searches in addition to name
    searches"""

    def _query_products(self, query: str) -> None:
        """Query products from supplier

        Args:
            query (str): Query string for search

        Returns:
            None: Nothing
        """

        # Example request url for Laboratorium Discounter
        # https://www.laboratoriumdiscounter.nl/en/search/{search_query}/page1.ajax?limit=100
        # which returns an array at '.products'
        #
        # Alternative:
        # https://www.laboratoriumdiscounter.nl/en/search/{search_query}/?format=json&limit=100
        # which returns an array at '.collection.products'
        #
        get_params = {
            # Setting the limit here to 1000, since the limit parameter should
            # apply to results returned from Supplier3SChem, not the rquests
            # made by it.
            "limit": self._limit or 100,
            "format": "json",
        }
        search_result = self.http_get_json(f"en/search/{query}", params=get_params)

        if not search_result or not isinstance(search_result, dict):
            return

        # self._query_results = search_result["collection"]["products"][: self._limit]
        self._query_results = search_result.get("collection", {}).get("products", [])

        if self._query_results is False:
            print(f"No products found for search query: {query}")
            raise NoProductsFound(supplier=self._supplier.name, query=query)

    # Method iterates over the product query results stored at
    # self._query_results and returns a list of TypeProduct objects.
    def _parse_products(self) -> None:
        if not isinstance(self._query_results, dict):
            raise ValueError(f"Expected a dictionary from search, received {type(self._query_results)}")

        for product in self._query_results.values():
            # Skip unavailable
            if product.get("available") is False:
                continue

            # Add each product to the self._products list in the form of a
            # TypeProduct object.
            # quantity = self._parse_quantity(product["title"])
            quantity = self._parse_quantity(product.get("variant"))
            # price = self._parse_price(product["price"])

            product_obj = TypeProduct(
                uuid=str(product.get("id", "")).strip(),
                name=product.get("title", None),
                title=product.get("fulltitle", None),
                # cas=self._get_cas_from_variant(product["variant"]),
                cas=self._find_cas(str(product.get("variant", ""))),
                description=str(product.get("description", "")).strip() or None,
                price=str(product.get("price", {}).get("price", "")).strip(),
                currency_code=product.get("price", {}).get("currency", "").upper(),
                currency=self._currency_symbol_from_code(product.get("price", {}).get("currency", None)),
                url=product.get("url", None),
                supplier=self._supplier.name,
                # quantity=quantity["quantity"],
                # uom=quantity["uom"],
            )

            if quantity:
                product_obj.update(quantity)

            self._products.append(product_obj)

    """ LABORATORIUMDISCOUNTER SPECIFIC METHODS """

    def _get_cas_from_variant(self, variant: str) -> None:
        """Get the CAS number from the variant, if applicable

        Args:
            variant (str): Variant string

        Returns:
            str: CAS, if one was found
        """
        print("variant:", variant)

        variant_dict = self._nested_arr_to_dict(variant.split(","))

        if variant_dict is not None and "CAS" in variant_dict:
            return variant_dict["CAS"]


__supplier_class = SupplierLaboratoriumDiscounter
