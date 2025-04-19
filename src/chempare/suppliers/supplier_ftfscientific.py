"""FTF Scientific Supplier Module"""

from typing import Dict

from bs4 import BeautifulSoup

from chempare.datatypes import TypeProduct
from chempare.datatypes import TypeSupplier
from chempare.suppliers.supplier_base import SupplierBase


# File: /suppliers/supplier_ftfscientific.py
class SupplierFtfScientific(SupplierBase):
    """FTF Scientific Supplier Class"""

    _supplier: TypeSupplier = TypeSupplier(
        name="FTF Scientific",
        location=None,
        base_url="https://www.ftfscientific.com",
        api_url="https://www.ftfscientific.com",
        # api_key = '8B7o0X1o7c'
    )
    """Supplier specific data"""

    allow_cas_search: bool = True
    """Determines if the supplier allows CAS searches in addition to name
    searches"""

    # If any extra init logic needs to be called... uncmment the below and add
    # changes
    # def __init__(self, query, limit=123):
    #     super().__init__(id, query, limit)
    # Do extra stuff here

    def _setup(self, query: str | None = None) -> None:
        headers = self.http_get_headers()
        cookies = (
            list(v for k, v in headers.multi_items() if k == "set-cookie")
            or None
        )

        auth_cookies = {}
        auth_headers = {}

        for cookie in cookies:
            segs = cookie.split("=")
            name = segs[0]
            val = "=".join(segs[1:-1])

            if name == "ssr-caching" or name == "server-session-bind":
                auth_cookies[name] = val.split(";")[0]
                continue

            if name == "client-session-bind":
                auth_headers["client-binding"] = val.split(";")[0]
                continue

        auth = self.http_get_json(
            "_api/v1/access-tokens", cookies=auth_cookies, headers=auth_headers
        )

        # What can this be used for?
        # https://www.ftfscientific.com/_api/v2/dynamicmodel

        self._headers["authorization"] = auth["apps"][
            "1484cb44-49cd-5b39-9681-75188ab429de"
        ]["instance"]

    def _query_products(self, query: str) -> None:
        """Query products from supplier

        Args:
            query (str): Query string to use

        Todo:
            - It looks like FTF will return more results than expected when
              searching via CAS. For example, if you search for 598-21-0, you
              will get Bromoacetybromide as the first result along with 224
              products that do not have the same CAS. It might be a good idea
              to add some logic to the FTF module that will _only_ return the
              item(s) with the matching CAS if a CAS search was used.
        """

        body = {
            "documentType": "public/stores/products",
            "query": query,
            "paging": {"skip": 0, "limit": 12},
            "includeSeoHidden": False,
            "facets": {
                "clauses": [
                    {
                        "aggregation": {
                            "name": "discountedPriceNumeric",
                            "aggregation": "MIN",
                        }
                    },
                    {
                        "aggregation": {
                            "name": "discountedPriceNumeric",
                            "aggregation": "MAX",
                        }
                    },
                    {"term": {"name": "collections", "limit": 999}},
                ]
            },
            "ordering": {"ordering": []},
            "language": "en",
            "properties": [],
            "fuzzy": True,
            "fields": [
                "id",
                "title",
                "description",
                "currency",
                "discountedPrice",
                "discountedPriceNumeric",
                "inStock",
                "sku",
                "infoSections",
                "collections",
                "onSale",
            ],
        }

        search_result = self.http_post_json(
            "_api/search-services-sitesearch/v1/search", json=body
        )

        if not search_result:
            return

        self._query_results = search_result["documents"]

    # Method iterates over the product query results stored at
    # self._query_results and returns a list of TypeProduct objects.
    def _parse_products(self) -> None:
        for product_obj in self._query_results:

            # Add each product to the self._products list in the form of a
            # TypeProduct object.
            product = self._parse_product(product_obj)

            if not product:
                continue

            # If the search was CAS specific, then verify this result has the
            # correect CAS
            if self._is_cas(self._query):
                if not product.cas or product.cas != self._query:
                    continue

            self._products.append(product)

    def _parse_product(self, product_obj: Dict) -> TypeProduct | None:
        """Parse single product and return single TypeProduct object

        Args:
            product_obj (Dict): Single product object from JSON body

        Returns:
            TypeProduct: Instance of TypeProduct

        Todo:
            - It looks like each product has a shopify_variants array that
              stores data about the same product but in different quantities.
              This could maybe be included?
        """

        # Try to get the CAS from the description (not always there)
        product_cas = self._find_cas(product_obj["description"])

        # If the cas is still not found, then try looking through the Product Info Infosection
        if not product_cas:
            last_info_section = None
            for info_section in product_obj["infoSections"]:
                if not last_info_section:
                    last_info_section = info_section
                    continue

                if last_info_section != 'Product Info':
                    last_info_section = None
                    continue

                product_cas = self._find_cas(info_section)
                break

        if self._is_cas(self._query):
            if not product_cas or product_cas != self._query:
                return

        product = TypeProduct(
            uuid=product_obj["id"],
            name=product_obj["title"],
            title=product_obj["title"],
            description=product_obj["description"],
            price=product_obj["discountedPrice"],
            url=f"{self._supplier.base_url}{product_obj["url"]}",
            supplier=self._supplier.name,
            currency=product_obj["currency"],
            cas=product_cas,
        )

        # product_info = self.__query_product_page(product_obj["url"])
        # if product_info:
        #     product.update(product_info)

        price_obj = self._parse_price(str(product.price))

        # if price_obj:
        #     product.update(price_obj)

        return product

    def __query_product_page(self, url: str) -> Dict:
        """Query a specific product page and parse the HTML for the cas or
        other info that's not present in the initial search result page

        Args:
            url (str): URL for product

        Returns:
            Dict: Just more data (eg: cas)
        """

        product_page_html = self.http_get_html(url)
        product_soup = BeautifulSoup(product_page_html, "html.parser")
        product_container = product_soup.find(
            "div", {"data-hook": "product-page"}
        )
        product_info = {}

        product_info["price"] = product_container.find(
            "span", {"data-hook": "formatted-primary-price"}
        ).get_text(strip=True)

        description = product_soup.find(
            "div", {"data-hook": "info-section-description"}
        )

        bullet_points = description.find_all("li")

        for desc_item in bullet_points:
            txt = desc_item.get_text(strip=True)
            if txt.startswith("CAS No"):
                product_info["cas"] = self._find_cas(txt)
                break

        return product_info

__supplier_class = SupplierFtfScientific
