from functools import partial

from datatypes import ProductType
from datatypes import SupplierType
from chempare.exceptions import NoProductsFoundError
from chempare.suppliers.supplier_base import SupplierBase
from chempare.utils import utils


# File: /suppliers/supplier_laboratoriumdiscounter.py
class SupplierLaboratoriumDiscounter(SupplierBase):
    """
    Todo:
        Creat a method that can query and parse individual products. This can
        be done by just taking the product page URL and appending ?format=json:
            https://www.laboratoriumdiscounter.nl/en/lithium-borohydride-ca-4mol-l-in-tetrahydrofuran-1.html?format=json
    """

    _supplier: SupplierType = SupplierType(
        name="Laboratorium Discounter", base_url="https://www.laboratoriumdiscounter.nl"
    )
    """Supplier specific data"""

    allow_cas_search: bool = True
    """Determines if the supplier allows CAS searches in addition to name
    searches"""

    _defaults = {}

    # def _setup(self) -> None:
    #     self._partial_product = partial(ProductType, supplier='Foo', currency="USD", currency='$')

    def _query_products(self) -> None:
        """Query products from supplier     None: Nothing"""

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

        search_result = self.http_get_json(f"en/search/{self._query}", params=get_params)

        self._defaults = {}

        shop_currency = utils.get_nested(search_result, "shop", "currency")

        self._defaults["currency"] = utils.get_nested(search_result, "shop", "currencies", shop_currency, "symbol")
        self._defaults["currency_code"] = utils.get_nested(search_result, "shop", "currencies", shop_currency, "code")
        # .shop.currencies[.shop.currency].symbol, .shop.currencies[.shop.currency].code

        # self._query_results = search_result["collection"]["products"][: self._limit]
        self._query_results = utils.get_nested(search_result, "collection", "products")

        if self._query_results is False:
            print(f"No products found for search query: {self._query}")
            raise NoProductsFoundError(supplier=self._supplier["name"], query=self._query)

    # Method iterates over the product query results stored at
    # self._query_results and returns a list of ProductType objects.
    def _parse_products(self) -> None:
        if not isinstance(self._query_results, dict):
            raise ValueError(f"Expected a dictionary from search, received {type(self._query_results)}")

        for product in self._query_results.values():
            # Skip unavailable
            if product.get("available") is False:
                continue

            # Add each product to the self._products list in the form of a
            # ProductType object.
            # quantity = self._parse_quantity(product["title"])
            quantity = self._parse_quantity(product.get("variant"))
            # price = self._parse_price(product["price"])
            if not quantity:
                continue

            price = utils.get_nested(product, "price", "price")

            product_obj = {
                "uuid": str(product.get("id", "")).strip(),
                "name": product.get("title", None),
                "title": product.get("fulltitle", None),
                # cas=self._get_cas_from_variant(product["variant"]),
                "cas": self._find_cas(str(product.get("variant", ""))),
                "description": str(product.get("description", "")).strip() or None,
                "price": price,
                # currency_code=self._defaults["curre"],
                # currency=shop_currency_symbol,
                "currency": self._defaults["currency"],
                "url": product.get("url", None),
                "supplier": self._supplier["name"],
                "usd": self._to_usd(from_currency=self._defaults.get("currency_code"), amount=price),
                # **self._defaults,
                # **quantity.__dict__,
                # quantity=quantity["quantity"],
                # uom=quantity["uom"],
            }

            # product_obj.update(self._defaults)

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
