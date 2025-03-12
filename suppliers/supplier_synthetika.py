from suppliers.supplier_base import SupplierBase, TypeProduct, TypeSupplier
from typing import List, Tuple, Dict, NoReturn
import re


# File: /suppliers/supplier_synthetika.py
class SupplierSynthetika(SupplierBase):

    _limit: int = 20
    """Max results to store"""

    _supplier: TypeSupplier = dict(
        name="Synthetika",
        location="Eu",
        base_url="https://synthetikaeu.com",
        api_url="https://synthetikaeu.com",
    )
    """Supplier specific data"""

    allow_cas_search: bool = True
    """Determines if the supplier allows CAS searches in addition to name searches"""

    def _query_products(self, query: str) -> NoReturn:
        """Query products from supplier

        Args:
            query (str): Query string to use
        """

        def __query_list(query: str, page: int = 1) -> NoReturn:
            """Query list of products on page

            Args:
                query (str): Query string
                page (int, optional): Page number. Defaults to 1.

            Returns:
                NoReturn: Nothing, just appends data to self._query_results and
                          executes self.__query_list() again if needed
            """

            # Example request url for Synthetika
            # https://synthetikaeu.com/webapi/front/en_US/search/short-list/products?text=borohydride&org=borohydride&page=1
            #
            get_params = {
                # Setting the limit here to 1000, since the limit parameter should apply to
                # results returned from Supplier3SChem, not the rquests made by it.
                "org": query,
                "text": query,
                "page": page,
            }

            search_result = self.http_get_json(
                "webapi/front/en_US/search/short-list/products", params=get_params
            )

            if not search_result:
                return

            self._query_results.extend(search_result["list"])

            if (
                int(search_result["pages"]) > page
                and len(self._query_results) < self._limit
            ):
                __query_list(query, page + 1)

        __query_list(query, 1)

    # Method iterates over the product query results stored at self._query_results and
    # returns a list of TypeProduct objects.
    def _parse_products(self) -> NoReturn:
        for product_obj in self._query_results:

            # Add each product to the self._products list in the form of a TypeProduct
            # object.
            self._products.append(self._parse_product(product_obj))

    def _parse_product(self, product_obj: Tuple[List, Dict]) -> TypeProduct:
        """Parse single product and return single TypeProduct object

        Args:
            product_obj (Tuple[List, Dict]): Single product object from JSON body

        Returns:
            TypeProduct: Instance of TypeProduct

        Todo:
            - It looks like each product has a shopify_variants array that stores data
              about the same product but in different quantities. This could maybe be
              included?
        """
        product = TypeProduct(
            uuid=product_obj["product_code"],
            name=product_obj["name"],
            title=product_obj["name"],
            # description = str(product_obj['description']).strip() if product_obj['description'] else None,
            price=product_obj["price"],
            url="{0}{1}".format(self._supplier["base_url"], product_obj["url"]),
            manufacturer=product_obj["attributes"].get("producer_name", None),
            supplier=self._supplier["name"],
        )

        quantity_pattern = re.compile(
            r"(?P<quantity>[0-9,\.x]+)\s?(?P<uom>[gG]allon|gal|k?g|[cmμ]m|m?[lL])"
        )
        quantity_matches = quantity_pattern.search(product_obj["name"])

        if quantity_matches:
            product.update(quantity_matches.groupdict())

        price_obj = self._parse_price(product_obj["price"])

        if price_obj:
            product.update(price_obj)

        return product


if __package__ == "suppliers":
    __disabled__ = False
