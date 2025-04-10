from chempare.datatypes import TypeProduct
from chempare.datatypes import TypeSupplier
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
        name="Laboratorium Discounter",
        base_url="https://www.laboratoriumdiscounter.nl",
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
        # Alternative:
        # https://www.laboratoriumdiscounter.nl/en/search/{search_query}/?format=json
        #
        get_params = {
            # Setting the limit here to 1000, since the limit parameter should
            # apply to results returned from Supplier3SChem, not the rquests
            # made by it.
            "limit": 1000
        }
        search_result = self.http_get_json(
            f"en/search/{query}/page1.ajax?", params=get_params
        )

        if not search_result:
            return

        self._query_results = search_result["products"][: self._limit]

    # Method iterates over the product query results stored at
    # self._query_results and returns a list of TypeProduct objects.
    def _parse_products(self) -> None:
        for product in self._query_results:
            # Skip unavailable
            if product["available"] is False:
                continue

            # Add each product to the self._products list in the form of a
            # TypeProduct object.
            # quantity = self._parse_quantity(product["title"])
            quantity = self._parse_quantity(product["variant"])
            # price = self._parse_price(product["price"])

            product_obj = TypeProduct(
                uuid=str(product["id"]).strip(),
                name=product["title"],
                title=product["fulltitle"],
                # cas=self._get_cas_from_variant(product["variant"]),
                cas=self._find_cas(str(product["variant"])),
                description=str(product["description"]).strip() or None,
                price=str(product["price"]["price"]).strip(),
                currency_code=product["price"]["currency"].upper(),
                currency=self._currency_symbol_from_code(
                    product["price"]["currency"]
                ),
                url=product["url"],
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


if __package__ == "suppliers":
    __disabled__ = False
