from bs4 import BeautifulSoup
from typing import Any
from chempare.datatypes import ProductType
from chempare.datatypes import SupplierType
from chempare.suppliers.supplier_base import SupplierBase


# File: /suppliers/supplier_chemsavers.py
class SupplierChemsavers(SupplierBase):

    _supplier: SupplierType = SupplierType(
        name="Chemsavers",
        base_url="https://chemsavers.com",
        api_url="https://0ul35zwtpkx14ifhp-1.a1.typesense.net",
        api_key="iPltuzpMbSZEuxT0fjPI0Ct9R1UBETTd",
    )
    """Supplier specific data"""

    _limit: int = 10
    """Limiting chemsavers output to 10 products"""

    allow_cas_search: bool = True
    """Determines if the supplier allows CAS searches in addition to name
    searches"""

    __defaults: dict = {"currency": "$", "currency_code": "USD", "is_restricted": False}
    """Default values applied to products from this supplier"""

    # If any extra init logic needs to be called... uncmment the below and add
    # changes.
    # def __init__(self, query, limit=123):
    #     super().__init__(id, query, limit)
    # Do extra stuff here

    def _query_products(self) -> None:
        """Query products from supplier"""

        # Example request url for Laboratorium Discounter
        # https://0ul35zwtpkx14ifhp-1.a1.typesense.net/multi_search?
        #   x-typesense-api-key=iPltuzpMbSZEuxT0fjPI0Ct9R1UBETTd
        #
        params = {"x-typesense-api-key": self._supplier.api_key}

        body = {
            "searches": [
                {
                    # 'query_by': 'name, CAS, description, sku,
                    # meta_description, meta_keywords',
                    "query_by": "name, CAS",
                    "sort_by": "price:asc",
                    "highlight_full_fields": ("name, CAS, description, sku, " "meta_description, meta_keywords"),
                    "collection": "products",
                    "q": self._query,
                    "facet_by": "price",
                    # Setting the limit here to 100, since the limit parameter
                    # should apply to results returned from the supplier. Some
                    # products may be filtered out based on no price listed or
                    # restrictions, hence requesting a large amount now and
                    # limiting it later.
                    "max_facet_values": 5,
                    "page": 1,
                    "per_page": 100,
                }
            ]
        }

        search_result = self.http_post_json("multi_search", json=body, params=params)

        if not search_result:
            return

        self._query_results = search_result["results"][0]["hits"]

    # Method iterates over the product query results stored at
    # self._query_results and returns a list of ProductType objects.
    def _parse_products(self) -> None:
        for product_obj in self._query_results:
            # if len(self._products) == self._limit:
            #    break

            product = self._parse_product(product_obj["document"])

            # Ignore items with no price
            if float(product.get("price")) == 0 or product.get("price") is None:
                continue

            # # Ignore items that don't send to residences
            # if product.is_restricted is True:
            #     continue

            self._products.append(product)

    def _parse_product(self, product_obj: dict[str, Any]) -> ProductType:
        """Parse single product and return single ProductType object

        Args:
            product_obj (tuple[list, dict]): Single product object from JSON

        Returns:
            ProductType: Instance of ProductType
        """

        quantity = self._parse_quantity(product_obj["description"])

        if not quantity:
            quantity = self._parse_quantity(product_obj["name"])

        product: ProductType = {
            # **self.__defaults,
            "uuid": product_obj["product_id"],
            "title": product_obj["name"],
            "description": product_obj["description"],
            "cas": product_obj.get("CAS", None),
            "price": float(product_obj.get("price", "0.00")),
            # "currency": product_obj.get("currency", None),
            "currency": "USD",
            # "currency": product_obj.get("currency"),
            "url": f"{self._supplier.base_url}{product_obj["url"]}",
            "sku": product_obj.get("sku", None),
            "upc": product_obj.get("upc", None),
            "supplier": self._supplier.name,
            "quantity": quantity.get("quantity"),
            "uom": quantity.get("uom", None),
            # **quantity.__dict__,
        }

        # Since the description contains HTML, and it may contain restrictions,
        # use BS
        description_soup = BeautifulSoup(product_obj["description"], "html.parser")

        # The restrictions always seem to be shown in
        # <strong style="color: red;"></strong> tags
        restriction = description_soup.find("strong", {"style": "color: red;"})

        if (
            restriction is not None
            and hasattr(restriction, 'string') is True
            and "Restricted to qualified labs and businesses only (no residences)" in str(restriction.string)
        ):
            product["restriction"] = restriction.string

        # The whole desc is usually in <b></b> tags
        desc = description_soup.find_all(["b", "p", "strong", "font"])

        if desc and desc is not None:
            desc_parts = [d.string.strip() if d.string and d.string else None for d in desc]
            desc_parts = list(set(desc_parts))
            desc_parts = list(filter(None, desc_parts))

            if product.get("restriction", None) in desc_parts:
                desc_parts.remove(product["restriction"])

            if desc_parts:
                product["description"] = "; ".join(desc_parts)

        return product
