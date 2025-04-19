import re

from bs4 import BeautifulSoup

from chempare.datatypes import ProductType
from chempare.datatypes import SupplierType
from chempare.suppliers.supplier_base import SupplierBase


# File: /suppliers/supplier_esdrei.py
class SupplierEsDrei(SupplierBase):

    _supplier: SupplierType = SupplierType(
        name="EsDrei",
        # location = '',
        base_url="https://shop.es-drei.de",
    )
    """Supplier specific data"""

    def _query_products(self, query: str) -> None:
        """Query products from supplier

        Args:
            query (str): Query string to use
        """

        self._query = query

        self._debug(f"Querying for {self._query}")

        # Example request url for S3Chem Supplier
        # https://shop.es-drei.de/search/index/sSearch/mercury?p=1&n=48
        # https://shop.es-drei.de/search?sSearch=mercury&p=1&n=48
        #
        get_params = {"sSearch": self._query, "p": 1, "n": 48}  # Page number  # Must be one of: 12, 24, 36, 48

        search_result = self.http_get_html("search", params=get_params)

        if not search_result:
            return

        self._query_results = search_result

    def _parse_products(self) -> None:
        """Parse product query results.

        Iterate over the products returned from self._query_products, creating
        new requests for each to get the HTML content of the individual product
        page, and creating a new ProductType object for each to add to _products

        Todo:
            Have this execute in parallen using AsyncIO
        """

        product_page_soup = BeautifulSoup(self._query_results, "html.parser")
        product_containers = product_page_soup.find_all("div", class_="product--info")

        for product_elem in product_containers[: self._limit]:
            r = self._parse_product(product_elem)
            self._products.append(r)

    def _parse_product(self, product_elem: BeautifulSoup) -> ProductType:
        """Parse a single div.product--info element, creating a Partner object

        Args:
            product_elem (BeautifulSoup): One of the elements returned from the
                                          BS search

        Returns:
            ProductType: Object of parsed product
        """

        # Get some of the basic elements from this product_element object
        # (which is just a BeautifulSoup object)
        title_elem = product_elem.find("a", class_="product--title")
        product_desc = product_elem.find("div", class_="product--description")
        price_info = product_elem.find("div", class_="product--price-info")

        # Parse the nested elements under the product_elem children
        price_default = price_info.find("span", class_="price--default")
        price_unit = price_info.find("div", class_="price--unit")

        # price_units = price_unit.find_all('span')
        price_string = price_default.string.strip().split("\n")[0]

        # Parse the price for the useful information
        # Pattern tested at: https://regex101.com/r/R4PQ5K/1
        price_string = re.sub(r"\s+", r" ", price_string)
        price_data = self._parse_price(price_string)

        product_data = dict(
            title=title_elem.attrs["title"],
            name=title_elem.attrs["title"],
            description=product_desc.get_text(strip=True),
            url=title_elem.attrs["href"],
            supplier=self._supplier.name,
            cas=self._find_cas(product_desc.string.strip()),
        )

        # Since the pattern were matching for will name the matched groups
        # 'price' and 'currency', we can use the `groupdict()` method to return
        # a dictionary like {price: 123, currency: '$'}, which we can then just
        # directly update the product with.
        #
        # This is just faster than doing:
        #   product.price = price_matches.price
        #   product.currency = price_matches.currency
        # product.update(price_matches.groupdict())

        quantity = price_unit.find_all("span")[-1].get_text(strip=True)
        quantity_data = self._parse_quantity(quantity)
        if quantity_data:
            product_data.update(quantity_data)

        # I notice the prices sometimes will have a 'from     32.24', so lets
        # reduce any multi-spaced gaps down to a single space
        # product.price = re.sub(r"\s+", r" ", product.price)
        if price_data:
            product_data.update(price_data)
        elif price_string:
            product_data["price"] = price_string

        return ProductType(**product_data)


__supplier_class = SupplierEsDrei
