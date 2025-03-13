from suppliers.supplier_base import SupplierBase, TypeProduct, TypeSupplier
from typing import List, Tuple, Dict, NoReturn
from bs4 import BeautifulSoup


# File: /suppliers/supplier_chemsavers.py
class SupplierChemsavers(SupplierBase):

    _supplier: TypeSupplier = dict(
        name="Chemsavers",
        location=None,
        base_url="https://chemsavers.com",
        api_url="https://0ul35zwtpkx14ifhp-1.a1.typesense.net",
        api_key="iPltuzpMbSZEuxT0fjPI0Ct9R1UBETTd",
    )
    """Supplier specific data"""

    _limit: int = 10
    """Limiting chemsavers output to 10 products"""

    allow_cas_search: bool = True
    """Determines if the supplier allows CAS searches in addition to name searches"""

    __defaults: Dict = {"currency": "$", "currency_code": "USD", "is_restricted": False}
    """Default values applied to products from this supplier"""

    # If any extra init logic needs to be called... uncmment the below and add changes
    # def __init__(self, query, limit=123):
    #     super().__init__(id, query, limit)
    # Do extra stuff here

    def _query_products(self, query: str) -> NoReturn:
        """Query products from supplier

        Args:
            query (str): Query string to use
        """

        # Example request url for Laboratorium Discounter
        # https://0ul35zwtpkx14ifhp-1.a1.typesense.net/multi_search?x-typesense-api-key=iPltuzpMbSZEuxT0fjPI0Ct9R1UBETTd
        #
        params = {"x-typesense-api-key": self._supplier["api_key"]}

        body = {
            "searches": [
                {
                    #'query_by': 'name, CAS, description, sku, meta_description, meta_keywords',
                    "query_by": "name, CAS",
                    "sort_by": "price:asc",
                    "highlight_full_fields": "name, CAS, description, sku, meta_description, meta_keywords",
                    "collection": "products",
                    "q": query,
                    "facet_by": "price",
                    # Setting the limit here to 100, since the limit parameter should apply to
                    # results returned from the supplier. Some products may be filtered out based
                    # on no price listed or restrictions, hence requesting a large amount now and
                    # limiting it later.
                    "max_facet_values": 100,
                    "page": 1,
                    "per_page": 100,
                }
            ]
        }

        search_result = self.http_post_json("multi_search", json=body, params=params)

        if not search_result:
            return

        self._query_results = search_result["results"][0]["hits"]

    # Method iterates over the product query results stored at self._query_results and
    # returns a list of TypeProduct objects.
    def _parse_products(self) -> NoReturn:
        for product_obj in self._query_results:
            # if len(self._products) == self._limit:
            #    break

            product = self._parse_product(product_obj["document"])

            # Ignore items with no price
            if float(product.price) == 0 or product.price is None:
                continue

            # Ignore items that don't send to residences
            if product.is_restricted is True:
                continue

            self._products.append(product)

    def _parse_product(self, product_obj: Tuple[List, Dict]) -> TypeProduct:
        """Parse single product and return single TypeProduct object

        Args:
            product_obj (Tuple[List, Dict]): Single product object from JSON body

        Returns:
            TypeProduct: Instance of TypeProduct
        """

        product = TypeProduct(
            **self.__defaults,
            uuid=product_obj["product_id"],
            name=product_obj["name"],
            description=product_obj["description"],
            cas=product_obj.get("CAS", None),
            price=product_obj.get("price", None),
            url="{0}{1}".format(self._supplier["base_url"], product_obj["url"]),
            sku=product_obj.get("sku", None),
            upc=product_obj.get("upc", None),
            supplier=self._supplier["name"]
        )

        # Since the description contains HTML, and it may contain restrictions, use BS
        description_soup = BeautifulSoup(product_obj["description"], "html.parser")

        # The restrictions always seem to be shown in <strong style="color: red;"></strong> tags
        restriction = description_soup.find("strong", {"style": "color: red;"})

        if (
            restriction is not None
            and "Restricted to qualified labs and businesses only (no residences)"
            in restriction.string
        ):
            product.restriction = restriction.string
            product.is_restricted = True

        # The whole desc is usually in <b></b> tags
        desc = description_soup.find_all(["b", "p", "strong", "font"])

        if desc and desc is not None:
            desc_parts = [
                d.string.strip() if d.string and d.string else None for d in desc
            ]
            desc_parts = list(set(desc_parts))
            desc_parts = list(filter(None, desc_parts))

            if product.restriction and product.restriction in desc_parts:
                desc_parts.remove(product.restriction)

            if desc_parts:
                product.description = "; ".join(desc_parts)

        return product.cast_properties()


if __package__ == "suppliers":
    __disabled__ = False
