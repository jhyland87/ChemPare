from suppliers.supplier_base import SupplierBase, TypeProduct, TypeSupplier
from typing import Dict, NoReturn
from bs4 import BeautifulSoup
from threading import Thread


# File: /suppliers/supplier_loudwolf.py
class SupplierLoudwolf(SupplierBase):
    """
    Todo: Currently, the LoudWolf module has the allow_cas_search set to False
          since searching using the CAS won't work. But it turns out that if
          you allow it to search in the product descriptions (using
          &description=true), then it will match the CAS values. Should the
          &description=true only be added when searching via CAS?..
    """

    _limit: int = 5
    """Max results to store"""

    _supplier: TypeSupplier = dict(
        name="Loudwolf Scientific",
        location="US",
        base_url="https://www.loudwolf.com/",
    )
    """Supplier specific data"""

    allow_cas_search: bool = False
    """Determines if the supplier allows CAS searches in addition to name
    searches"""

    def _query_products(self, query: str) -> NoReturn:
        """Query products from supplier

        Args:
            query (str): Query string to use
        """

        self.__product_pages = dict()

        def __query_search_page(
            query: str, limit: int = 100, page_idx: int = 1
        ):
            """Handles the pagination on the search page"""
            get_params = {
                # Setting the limit here to 1000, since the limit parameter
                # should apply to results returned from Supplier3SChem, not the
                # rquests made by it.
                # 'q': f'{query}:productNameExactMatch',
                "search": query,
                "limit": 100,
                "route": "product/search",
                "sort": "p.price",  # pd.name, p.model, p.sort_order (default)
                "order": "ASC",  # or DESC
                "page": page_idx,
            }

            # If were doing a CAS search, then we must include description
            # matching
            if self._is_cas(query) is True:
                get_params["description"] = True

            search_result = self.http_get_html(
                "storefront/index.php", params=get_params
            )

            if not search_result:
                return

            product_soup = BeautifulSoup(search_result, "html.parser")

            # Since we know the element is a <h3 class=product-price /> element,
            # search for H3's
            product_elements = product_soup.find_all(
                "div", class_="product-layout"
            )

            if product_elements is None:
                # No product wrapper found
                return

            # Iterate through the product elements, getting the product_id and
            # link for each
            for pe in product_elements:
                if len(self.__product_pages) >= self._limit:
                    break

                product_image_div = pe.find("div", class_="image")
                if not product_image_div:
                    continue

                product_link = product_image_div.find("a")

                if not product_link:
                    continue

                product_href = product_link.attrs["href"]

                if not product_href:
                    continue

                product_href_params = self._get_param_from_url(
                    product_href.strip()
                )

                if not product_href_params or not product_href_params.get(
                    "product_id", None
                ):
                    continue

                product_id = product_href_params.get("product_id", None)

                if product_id in self.__product_pages:
                    continue

                self.__product_pages[product_id] = product_href.strip()

        __query_search_page(query)

    # Method iterates over the product query results stored at
    # self._query_results and
    # returns a list of TypeProduct objects.
    def _parse_products(self) -> NoReturn:
        """Parse products from initial query. This will iterate over
        self.__product_pages, and execute the self.__query_and_parse_product
        method using multiple thrads to speed things up.
        """

        threads = []

        for product_href in self.__product_pages.values():
            thread = Thread(
                target=self.__query_and_parse_product,
                kwargs=dict(href=product_href),
            )
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

    def __query_and_parse_product(self, href: str) -> NoReturn:
        """Execute the product page query and parse functions, one after the
        other, then updating the self._products

        Args:
            href (str): URL for product
        """

        product_params = self._get_param_from_url(href)
        product_page = self.__query_product_page(product_params)

        if not product_page:
            return

        product = self.__parse_product_page(product_page)

        if not product:
            return

        # If this is a CAS search, but there is no CAS found, or it's a
        # mismatch, then skip this product.
        if self._is_cas(self._query) is True:
            if not product.cas or product.cas != self._query:
                return

        product.uuid = product_params["product_id"]
        product.url = href
        product.supplier = self._supplier["name"]

        self._products.append(product)

    def __query_product_page(self, params: Dict) -> bytes:
        """Query a specific product page given the GET params

        Args:
            params (Dict): The HTTP Get parameters (with product_id)

        Returns:
            bytes: The html content
        """

        product_html = self.http_get_html("storefront/index.php", params=params)
        return product_html or None

    def __parse_product_page(self, product_html: bytes) -> TypeProduct:
        """Parse a specific product page's HTML

        Args:
            product_html (bytes): Product pages HTML
                                  (ie: from __query_product_page)

        Returns:
            TypeProduct: A new product object, if valid
        """

        product_soup = BeautifulSoup(product_html, "html.parser")
        product_content = product_soup.find("div", id="content")

        # find the title (should be only h1 tag), and require one be found
        title_elem = product_content.find("h1")
        if not title_elem:
            return None

        # product_id = product_soup.find('input', {'name':'product_id'})

        product = TypeProduct(
            title=title_elem.get_text(strip=True),
            # uuid=product_id.attrs['value'].strip()
        )

        # find the price (should be only h2 tag), and require one be found
        price_elem = product_content.find("h2")
        if not price_elem:
            return None

        price_txt = price_elem.get_text(strip=True)
        if not price_txt or price_txt.startswith("$") is False:
            return None

        # Attempt to parse the price out to get the currency and price
        price_data = self._parse_price(price_txt)

        if price_data:
            product.update(price_data)
        else:
            product.price = price_txt

        product_desc_tab = product_content.find("div", id="tab-description")
        paragraphs = product_desc_tab.find_all("p", class_="MsoNormal")

        # There's no useful ID's or classes, so just enumerating over them and
        # checking for specific values (GRADE, CAS, etc), then grabbing the
        # value of the next element seems to work ok. Though it kinda sucks and
        # will backfire if the format changes.
        for idx, p in enumerate(paragraphs):
            p_txt = p.get_text(strip=True)
            if idx == 0:
                product.name = p_txt
                continue

            if "TOTAL WEIGHT OF PRODUCT" in p_txt:
                idx = idx + 1
                quantity = paragraphs[idx].get_text(strip=True)
                qty = self._parse_quantity(quantity)
                if qty is not None:
                    product.update(qty)
                continue

            if "GRADE" == p_txt:
                idx = idx + 1
                product.grade = paragraphs[idx].get_text(strip=True)
                continue

            if "CAS#" in p_txt:
                idx = idx + 1
                product.cas = paragraphs[idx].get_text(strip=True)
                continue

            # Arbitrary value to abort parsing after, since the find_all('p')
            # will return a lot more than just the necessary elements.
            if idx > 13:
                break

        return product


if __package__ == "suppliers":
    __disabled__ = False
