"""Warchem Module"""
from threading import Thread
from typing import NoReturn
from bs4 import BeautifulSoup
from chempare.datatypes import TypeProduct, TypeSupplier
from chempare.suppliers.supplier_base import SupplierBase


# File: /suppliers/supplier_warchem.py
class SupplierWarchem(SupplierBase):
    """Warchem Module"""

    _limit: int = 5
    """Maximum amount of allowed search results to be returned"""

    _supplier: TypeSupplier = dict(
        name="WarChem",
        location=None,
        base_url="https://warchem.pl",
        api_url="https://warchem.pl",
    )
    """Supplier specific data"""

    allow_cas_search: bool = True
    """Determines if the supplier allows CAS searches in addition to name
    searches"""

    def _setup(self, query: str = None) -> NoReturn:
        """The setup for WarChem is to store a randomly generated string in the
        eGold cookie, then set the product return count to the max (36), which
        will be carried on to any request afterwords.

        Args:
            query (str, optional):  Query beig ran. This is here because
                                    sometimes the HTTP calls preceeding the
                                    actual query might use the query in some
                                    hash generation logic. Defaults to None.

        Returns:
            NoReturn: Nothing
        """

        # This eGold cookie seems to be what they use to keep track of your
        # settings
        self._cookies["eGold"] = self._random_string(26)

        # Make the request to keep the product listing limit at 36 (max)
        self.http_post(
            path=f"szukaj.html/szukaj={query}", data=dict(ilosc_na_stronie=36)
        )

    def _query_products(self, query: str) -> NoReturn:
        """Query products from supplier

        Args:
            query (str): Query string to use
        """

        # https://warchem.pl/szukaj.html/szukaj=ACET/s=2

        search_result = self.http_get_html(
            # path=f"szukaj.html/szukaj={query}/opis=tak/fraza=nie/nrkat=tak/kodprod=tak/ean=tak/kategoria=1/podkat=tak"
            path=f"szukaj.html/szukaj={query}"
        )

        search_result_soup = BeautifulSoup(search_result, "html.parser")
        product_container = search_result_soup.find(
            "div", class_="ListingWierszeKontener"
        )

        if not product_container:
            return

        product_elements = product_container.find_all(
            "div", class_="LiniaDolna"
        )

        if not product_elements:
            return

        self._query_results = product_elements[: self._limit]

    def _parse_products(self) -> NoReturn:
        """Method iterates over the product query results stored at
        self._query_results and returns a list of TypeProduct objects.
        """

        # Each product page query will have its own thread stored here
        threads = []

        for product_elem in self._query_results:
            # Add each product to the self._products list in the form of
            # a TypeProduct object.

            link = product_elem.find("h3").find("a")
            thread = Thread(
                target=self.__query_and_parse_product,
                kwargs=dict(href=link.attrs["href"]),
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
            NoReturn: Nothing, just inserts a new TypeProduct into
                      self._products (if successful).
        """

        product_page_html = self.http_get_html(href)
        product_soup = BeautifulSoup(product_page_html, "html.parser")

        product = TypeProduct(
            title=product_soup.find("h1").get_text(strip=True),
            supplier=self._supplier["name"],
            url=href,
        )

        details = product_soup.find(
            "div", class_="DodatkowyProduktuOpis"
        ).find_all("tr")

        # The details table has some useful values. Add the key in the table
        # and its assocaited key in the product object below, and it will get
        # included
        translated_keys = {"Nazwa (ang.):": "name", "Numer CAS:": "cas"}

        for tr in details:
            td = tr.find_all("td")
            attr = td[0].get_text(strip=True)
            val = td[1].get_text(strip=True)

            if attr.strip() not in translated_keys:
                continue

            attr_key = translated_keys[attr.strip()]
            product.set(attr_key, val)

        price_elem = product_soup.find("span", {"itemprop": "price"})

        product.price = price_elem.attrs["content"]
        product.currency = price_elem.get_text(strip=True).split(" ")[-1]

        quantity_elem_container = product_soup.find("div", id="nr_cechy_1")
        quantity_options = quantity_elem_container.find_all(
            "div", class_="PoleWyboruCechy"
        )

        quantity = quantity_options[0].find("label").find("span")
        if quantity:
            product.update(self._parse_quantity(quantity.get_text(strip=True)))

        self._products.append(product.cast_properties())


if __package__ == "suppliers":
    __disabled__ = True
