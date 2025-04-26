from __future__ import annotations

from threading import Thread
from typing import TYPE_CHECKING

import chempare.utils as utils
from bs4 import BeautifulSoup
from chempare.suppliers.supplier_base import SupplierBase

if TYPE_CHECKING:
    from datatypes import SupplierType
    from datatypes import ProductType
    from typing import Final, ClassVar


# File: /suppliers/supplier_loudwolf.py
class SupplierLoudwolf(SupplierBase):
    """
    Todo: Currently, the LoudWolf module has the allow_cas_search set to False
          since searching using the CAS won't work. But it turns out that if
          you allow it to search in the product descriptions (using
          &description=true), then it will match the CAS values. Should the
          &description=true only be added when searching via CAS?..
    """

    _limit: ClassVar[int] = 5
    """Max results to store"""

    _supplier: Final[SupplierType] = {
        "name": "Loudwolf Scientific",
        "location": "US",
        "base_url": "https://www.loudwolf.com/",
    }
    """Supplier specific data"""

    allow_cas_search: Final[bool] = False
    """Determines if the supplier allows CAS searches in addition to name
    searches"""

    def _query_products(self) -> None:
        """Query products from supplier"""

        self.__product_pages = {}

        def __query_search_page(query: str, limit: int = 10, page_idx: int = 1):
            """Handles the pagination on the search page"""
            get_params = {
                # Setting the limit here to 1000, since the limit parameter
                # should apply to results returned from Supplier3SChem, not the
                # rquests made by it.
                # 'q': f'{query}:productNameExactMatch',
                "search": query,
                "limit": 10,
                "route": "product/search",
                "sort": "p.price",  # pd.name, p.model, p.sort_order (default)
                "order": "ASC",  # or DESC
                "page": page_idx,
            }

            # If were doing a CAS search, then we must include description
            # matching
            if utils.is_cas(query) is True:
                get_params["description"] = True

            if not (search_result := self.http_get_html("storefront/index.php", params=get_params)):
                return

            product_soup = BeautifulSoup(search_result, "html.parser")

            # Since we know the element is a <h3 class=product-price /> element,
            # search for H3's
            if not (product_elements := product_soup.find_all("div", class_="product-layout")):
                # No product wrapper found
                return

            # Iterate through the product elements, getting the product_id and
            # link for each
            for pe in product_elements:
                if len(self.__product_pages) >= self._limit:
                    break

                if (
                    not (product_link := utils.bs4_css_selector(pe, "div.image>a")) or
                    not (product_attrs := product_link.attrs) or
                    not (product_href := product_attrs.get("href", None)) or
                    not (product_href_params := utils.get_param_from_url(product_href.strip())) or
                    not (product_id := product_href_params.get("product_id", None)) or
                    product_id in self.__product_pages
                ):
                    continue

                self.__product_pages[product_id] = product_href.strip()

        __query_search_page(self._query)

    # Method iterates over the product query results stored at
    # self._query_results and
    # returns a list of ProductType objects.
    def _parse_products(self) -> None:
        """Parse products from initial query. This will iterate over
        self.__product_pages, and execute the self.__query_and_parse_product
        method using multiple thrads to speed things up.
        """

        threads = []

        for product_href in self.__product_pages.values():
            thread = Thread(target=self.__query_and_parse_product, kwargs=dict(href=product_href))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

    def __query_and_parse_product(self, href: str) -> None:
        """Execute the product page query and parse functions, one after the
        other, then updating the self._products

        Args:
            href (str): URL for product
        """

        # product_params = utils.get_param_from_url(href)
        # #product_html: bytes = self.http_get_html("storefront/index.php", params=product_params)

        # if not product_page:
        #     return

        product = self.__parse_product_page(href)

        if not product:
            return

        # If this is a CAS search, but there is no CAS found, or it's a
        # mismatch, then skip this product.
        if utils.is_cas(self._query) is True:
            if not product.cas or product.cas != self._query:
                return

        # product.uuid = product_params["product_id"]
        # product.url = href
        # product.supplier = self._supplier["name"]

        self._products.append(product)

    # def __query_product_page(self, params: dict) -> bytes | None:
    #     """Query a specific product page given the GET params

    #     Args:
    #         params (dict): The HTTP Get parameters (with product_id)

    #     Returns:
    #         bytes: The html content
    #     """

    #     product_html: bytes = self.http_get_html("storefront/index.php", params=params)
    #     return product_html or None

    def __parse_product_page(self, url: str) -> ProductType | None:
        """Parse a specific product page's HTML

        Args:
            product_html (bytes): Product pages HTML
                                  (ie: from __query_product_page)

        Returns:
            ProductType: A new product object, if valid
        """

        product_params = utils.get_param_from_url(url)
        product_html: bytes = self.http_get_html("storefront/index.php", params=product_params)
        product_soup = BeautifulSoup(product_html, "html.parser")
        product_content = product_soup.find("div", id="content")

        # find the title (should be only h1 tag), and require one be found
        title_elem = product_content.find("h1")
        if not title_elem:
            return None

        # product_id = product_soup.find('input', {'name':'product_id'})

        product = {
            "title": title_elem.get_text(strip=True),
            "supplier": self._supplier["name"],
            "url": "test",
            # uuid=product_id.attrs['value'].strip()
        }

        # find the price (should be only h2 tag), and require one be found
        price_elem = product_content.find("h2")
        if not price_elem:
            return None

        price_txt = price_elem.get_text(strip=True)
        if not price_txt or price_txt.startswith("$") is False:
            return None

        # Attempt to parse the price out to get the currency and price
        price_data = utils.parse_price(price_txt)

        # if isinstance(price_data, PriceType):
        # if isinstance(price_data, PriceType) and price_data:
        if price_data:
            product.update(price_data)
        else:
            product["price"] = price_txt

        product_desc_tab = product_content.find("div", id="tab-description")
        paragraphs = product_desc_tab.find_all("p", class_="MsoNormal")

        # There's no useful ID's or classes, so just enumerating over them and
        # checking for specific values (GRADE, CAS, etc), then grabbing the
        # value of the next element seems to work ok. Though it kinda sucks and
        # will backfire if the format changes.
        for idx, p in enumerate(paragraphs):
            p_txt = p.get_text(strip=True)
            if idx == 0:
                product["name"] = p_txt
                continue

            if "TOTAL WEIGHT OF PRODUCT" in p_txt:
                idx = idx + 1
                quantity = paragraphs[idx].get_text(strip=True)
                qty = utils.parse_quantity(quantity)
                if qty is not None:
                    product.update(qty)
                continue

            if "GRADE" == p_txt:
                idx = idx + 1
                product["grade"] = paragraphs[idx].get_text(strip=True)
                continue

            if "CAS#" in p_txt:
                idx = idx + 1
                product["cas"] = paragraphs[idx].get_text(strip=True)
                continue

            # Arbitrary value to abort parsing after, since the find_all('p')
            # will return a lot more than just the necessary elements.
            if idx > 13:
                break

        return product
