import re
from typing import NoReturn
from threading import Thread
from bs4 import BeautifulSoup
from chempare.suppliers.supplier_base import SupplierBase
from chempare.datatypes import TypeProduct, TypeSupplier


# File: /suppliers/supplier_onyxmet.py
class SupplierOnyxmet(SupplierBase):

    _limit: int = 10
    """Max results to store"""

    _supplier: TypeSupplier = dict(
        name="Onyxmet", location="Poland", base_url="https://onyxmet.com"
    )
    """Supplier specific data"""

    allow_cas_search: bool = True
    """Determines if the supplier allows CAS searches in addition to name
    searches"""

    # Regex tested at https://regex101.com/r/ddGVsT/1 (matches 66/80)
    # _title_regex_pattern = (
    #   r'^(?P<name>.*) (-\s)?(?P<quantity>[0-9,]+)"
    #   r"(?P<uom>k?g|[cmμ]m)'
    # )

    # Regex tested at https://regex101.com/r/qL8u8s/1 67/80
    # _title_regex_pattern = (
    #   r'^(?P<name>.*) (-\s)?(?P<quantity>[0-9,]+)"
    #   r"(?P<uom>[cmkμ]?[mlg])'
    # )

    # Regex tested at https://regex101.com/r/bLWC2b/3 (matches 80-ish/80)
    # NOTE: The group names here should match keys in the self._product
    #       dictionary, as the regex results will be merged into it.
    # _title_regex_pattern = (
    #   r'^(?P<product>[a-zA-Z\s\-\(\)]+[a-zA-Z\(\)])"
    #   r"[-\s]+(?P<purity>[0-9,]+%)?[-\s]*(?:(?P<quantity>[0-9,]+)"
    #   r"(?P<unit>[cmkμ]?[mlg]))?'
    # )

    # https://regex101.com/r/bLWC2b/5
    # NOTE: This misses some simple ones like "Uranyl zinc acetate  10g", and
    #       needs to be worked on
    _title_regex_pattern = (
        r"^(?P<product>[a-zA-Z0-9\s\-(\)]+[a-zA-Z\(\)])"
        r"[-\s]+(?:(?P<purity>[0-9,]+%)?[-\s]*)"
        r"(?:(?P<quantity>[0-9,]+)(?P<uom>[cmkμ]?[mlg]))?"
    )

    # If any extra init logic needs to be called... uncmment the below and add
    # changes
    def __init__(self, query: str, limit: int = 10) -> NoReturn:
        # self.__test_lock = Lock()
        super().__init__(query, limit)
        # Do extra stuff here

    def _query_products(self, query: str) -> NoReturn:
        """Query products from supplier

        Args:
            query (str): Query string to use
        """

        # Example request url for Onyxmet Supplier
        # https://onyxmet.com/index.php?route=product/search/json&term={query}
        #
        get_params = {"route": "product/search/json", "term": query}

        search_result = self.http_get_json("index.php", params=get_params)

        if not search_result:
            return

        self._query_results = search_result[: self._limit]

    def _parse_products(self) -> NoReturn:
        """Parse product query results.

        Iterate over the products returned from self._query_products, creating
        new requests for each to get the HTML content of the individual product
        page, and creating a new TypeProduct object for each to add to _products

        Todo:
            Have this execute in parallen using AsyncIO
        """

        # If no results were found, then abort early on
        if self._query_results is None or len(self._query_results) == 0:
            return

        # will store the threads
        threads = []

        # Iterate over the initial product search results, creating a thread to
        # request the product page for each item, adding it to the
        # self._products property
        for product in self._query_results:
            # self.__query_and_parse_product(product['href'])
            thread = Thread(
                target=self.__query_and_parse_product,
                kwargs=dict(href=product["href"]),
            )
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

    def __query_and_parse_product(self, href: str) -> NoReturn:
        """Query specific product page and parse results

        Args:
            href (str): The path of the web page to query and parse
                        using BeautifulSoup

        Returns:
            TypeProduct: Single instance of TypeProduct
        """

        # self.__test_lock.acquire()
        product_page_html = self.http_get_html(href)

        product_soup = BeautifulSoup(product_page_html, "html.parser")

        # Since we know the element is a <h3 class=product-price /> element,
        # search for H3's
        h3_elems = product_soup.find_all("h3")

        # Find the one with the 'product-price' class
        title_elem = next(
            obj for obj in h3_elems if "product-title" in obj.get("class")
        )
        price_elem = next(
            obj for obj in h3_elems if "product-price" in obj.get("class")
        )

        # TODO: I'm sure there's an easier way to just specifically look for
        #       the 'h3.product-price' element, instead of _all_ h3 elements
        #       then filtering the results for one that has the 'product-price'
        #       class... But I'll leave that optimization up to you :-)

        if not price_elem:
            raise Exception("No price found")

        # Get the product name and price
        # (Set the product name here to default it, we ca re-set it to the
        # parsed value down below)
        product = TypeProduct(
            title=title_elem.contents[0],
            name=title_elem.contents[0],
            # price=price_elem.contents[0],
            supplier=self._supplier["name"],
            url=href,
        )

        price = self._parse_price(price_elem.contents[0])

        product.update(price)

        # Use the regex pattern to parse the name for some useful data.
        title_pattern = re.compile(self._title_regex_pattern)
        title_matches = title_pattern.search(product.name)

        # If something is matched, then just merge the key/names into the
        # self._product property
        if title_matches:
            product.update(title_matches.groupdict())

        self._products.append(product.cast_properties())
        # self.__test_lock.release()


if __package__ == "suppliers":
    __disabled__ = False
