from suppliers.supplier_base import SupplierBase, TypeProduct, TypeSupplier
from typing import Dict, NoReturn
from bs4 import BeautifulSoup


# File: /suppliers/supplier_ftfscientific.py
class SupplierFtfScientific(SupplierBase):

    _supplier: TypeSupplier = dict(
        name="FTF Scientific",
        location=None,
        base_url="https://www.ftfscientific.com",
        api_url="https://www.ftfscientific.com",
        # api_key = '8B7o0X1o7c'
    )
    """Supplier specific data"""

    allow_cas_search: bool = True
    """Determines if the supplier allows CAS searches in addition to name searches"""

    # If any extra init logic needs to be called... uncmment the below and add changes
    # def __init__(self, query, limit=123):
    #     super().__init__(id, query, limit)
    # Do extra stuff here

    def _setup(self, query: str = None) -> NoReturn:
        headers = self.http_get_headers()
        cookies = list(v for k, v in headers.multi_items() if k == "set-cookie") or None

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

        self._headers["authorization"] = auth["apps"][
            "1484cb44-49cd-5b39-9681-75188ab429de"
        ]["instance"]

        # Not sure if any of this is needed, keeping it here for now though
        # self._headers['cache-control']='no-cache'
        # self._headers['X-Wix-Client-Artifact-Id']='wix-thunderbolt'
        # self._headers['Referer']='https://www.ftfscientific.com/_partials/wix-thunderbolt/dist/clientWorker.2323647d.bundle.min.js'
        # self._headers['x-wix-brand']='wix'
        # self._headers['commonConfig']='%7B%22brand%22%3A%22wix%22%2C%22host%22%3A%22VIEWER%22%2C%22BSI%22%3A%22%22%2C%22siteRevision%22%3A%22316%22%2C%22renderingFlow%22%3A%22NONE%22%2C%22language%22%3A%22en%22%2C%22locale%22%3A%22en-us%22%7D'
        # self._headers['x-wix-search-bi-correlation-id']='5c4da737-0647-42a5-6bcb-ea87a4718a8b'

    def _query_products(self, query: str) -> NoReturn:
        """Query products from supplier

        Args:
            query (str): Query string to use

        Todo:
            - It looks like FTF will return more results than expected when searching via CAS.
              For example, if you search for 598-21-0, you will get Bromoacetybromide as the
              first result along with 224 products that do not have the same CAS. It might be
              a good idea to add some logic to the FTF module that will _only_ return the item(s)
              with the matching CAS if a CAS search was used.
        """

        # Example request url for FTF
        # https://www.ftfscientific.com/_api/search-services-sitesearch/v1/search
        #
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
                "description",
                "title",
                "id",
                "currency",
                "discountedPrice",
                "inStock",
            ],
        }

        search_result = self.http_post_json(
            path="_api/search-services-sitesearch/v1/search", json=body
        )

        if not search_result:
            return

        self._query_results = search_result["documents"]

    # Method iterates over the product query results stored at self._query_results and
    # returns a list of TypeProduct objects.
    def _parse_products(self) -> NoReturn:
        for product_obj in self._query_results:

            # Add each product to the self._products list in the form of a TypeProduct
            # object.
            product = self._parse_product(product_obj)

            # If the search was CAS specific, then verify this result has the correect CAS
            if self._is_cas(self._query):
                if not product.cas or product.cas != self._query:
                    continue

            self._products.append(product)

    def _parse_product(self, product_obj: Dict) -> TypeProduct:
        """Parse single product and return single TypeProduct object

        Args:
            product_obj (Dict): Single product object from JSON body

        Returns:
            TypeProduct: Instance of TypeProduct

        Todo:
            - It looks like each product has a shopify_variants array that stores data
              about the same product but in different quantities. This could maybe be
              included?
        """

        product = TypeProduct(
            uuid=product_obj["id"],
            name=product_obj["title"],
            title=product_obj["title"],
            description=product_obj["description"],
            price=product_obj["discountedPrice"],
            url="{0}{1}".format(self._supplier["base_url"], product_obj["url"]),
            supplier=self._supplier["name"],
            currency=product_obj["currency"],
            cas=self._find_cas(str(product_obj)),
        )

        product_info = self.__query_product_page(product_obj["url"])
        if product_info:
            product.update(product_info)

        price_obj = self._parse_price(product.price)
        if price_obj:
            product.update(price_obj)

        return product

    def __query_product_page(self, url: str) -> Dict:
        """Query a specific product page and parse the HTML for the cas or other info that's not present in
        the initial search result page

        Args:
            url (str): URL for product

        Returns:
            Dict: Just more data (eg: cas)
        """

        product_page_html = self.http_get_html(url)
        product_soup = BeautifulSoup(product_page_html, "html.parser")
        product_container = product_soup.find("div", {"data-hook": "product-page"})
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


if __package__ == "suppliers":
    __disabled__ = False
