from bs4 import BeautifulSoup

from chempare.datatypes import ProductType
from chempare.datatypes import SupplierType
from chempare.suppliers.supplier_base import SupplierBase


# File: /suppliers/supplier_tcichemicals.py
class SupplierTciChemicals(SupplierBase):

    allow_cas_search: bool = True
    """Determines if this supplier allows CAS searches"""

    _limit: int = 20
    """Max results to store"""

    _supplier: SupplierType = SupplierType(
        name="TCI Chemicals",
        # location = 'Eu',
        base_url="https://www.tcichemicals.com",
    )
    """Supplier specific data"""

    _headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "sec-ch-ua-platform": "macOS",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    }

    allow_cas_search: bool = True
    """Determines if the supplier allows CAS searches in addition to name
    searches"""

    def _query_products(self) -> None:
        """Query products from supplier"""

        # Example request url for Synthetika
        # JSON (limited search results)
        # https://synthetikaeu.com/webapi/front/en_US/search/short-list/products
        #   ?text=borohydride&org=borohydride&page=1
        # HTML
        # https://www.tcichemicals.com/US/en/search/?text=benz'
        #
        def __query_search_page(query: str, page_idx: int = 0) -> None:
            """Handles the pagination on the search page

            Args:
                query (str): Query string
                page_idx (int, optional): Page number to query for.
                                          Defaults to 0.

            Returns:
                None: Nothing, just adds new entries to self._query_results,
                          and executes self.__query_search_page if needed.
            """
            get_params = {
                # Setting the limit here to 1000, since the limit parameter
                # should apply to results returned from Supplier3SChem, not
                # the rquests made by it.
                # 'q': f'{query}:productNameExactMatch',
                "text": query,
                "page": page_idx,
            }

            search_result = self.http_get_html("US/en/search", params=get_params, headers=self._headers)

            if not search_result:
                return

            product_soup = BeautifulSoup(search_result, "html.parser")

            # Since we know the element is a <h3 class=product-price />
            # element, search for H3's
            product_basic = product_soup.find("div", id="product-basic-wrap")

            if product_basic is None:
                # No product wrapper found
                return

            self._query_results.extend(product_basic.find_all("div", class_="prductlist"))

            if self._limit == len(self._query_results):
                return

            if self._limit < len(self._query_results):
                self._query_results = self._query_results[: self._limit]
                return

            if self._limit > len(self._query_results):
                __query_search_page(query, page_idx + 1)
                return

        __query_search_page(self._query, 0)

    def _parse_products(self) -> None:
        """Method iterates over the product query results stored at
        self._query_results and returns a list of ProductType objects.

        Returns:
            None: Nothing.
        """
        for product_elem in self._query_results:
            self.__parse_product(product_elem)

    def __parse_product(self, product_obj: BeautifulSoup) -> None:
        """Parse single product and return single ProductType object

        Args:
            product_obj (tuple[list, dict]): Single product object from the
                                             JSON body

        Todo:
            - It looks like each product has a shopify_variants array that
              stores data about the same product but in different quantities.
              This could maybe be included?
        """

        title = product_obj.find("a", class_="product-title")

        if not title.string:
            return

        quantity = product_obj.find(attrs={"data-attr": "Size:"})
        price = product_obj.find("div", class_="listPriceNoStrike")

        if not price:
            return

        price_obj = self._parse_price(price.get_text(strip=True))

        product_dict = dict(
            title=title.get_text(strip=True),
            quantity=quantity.get_text(strip=True),
            supplier=self._supplier.name,
            url=self._supplier.base_url + str(title.attrs["href"]),
        )

        if price_obj:
            product_dict.update(price_obj)

        description_container = product_obj.find("div", class_="product-description")
        data = description_container.find_all("td")

        for idx, d in enumerate(data):
            if d.get_text(strip=True) == "Product Number":
                product_dict["uuid"] = data[idx + 1].get_text(strip=True)
                continue

            if d.get_text(strip=True) == "CAS RN":
                product_dict["cas"] = data[idx + 1].get_text(strip=True)
                continue

        quantity = self._parse_quantity(product_dict["quantity"])
        # quantity_pattern = re.compile(
        #     (r"(?P<quantity>[0-9,\.x]+)\s?(?P<uom>[gG]allon|gal|k?g|" r"[cmμ][mM]|[mM]?[lL]|[Mm][gG])$")
        # )
        # quantity_matches = quantity_pattern.search(product_dict["quantity"])

        if quantity is not None:
            product_dict.update(quantity)

        # price_pattern = re.compile(r"^(?P<currency>.)(?P<price>\d+\.\d+)$")
        # price_matches = price_pattern.search(product.price)

        # if price_matches:
        #     product.update(price_matches.groupdict())

        self._products.append(product_dict)
