"""Supplier Base Cass"""
from typing import List, Dict, Any, Union, NoReturn, Self
from curl_cffi import requests
from abcplus import ABCMeta, abstractmethod, finalmethod
from chempare import ClassUtils

# Todo: this should be automatic
# from chempare.datatypes.product import TypeProduct
# from chempare.datatypes.supplier import TypeSupplier
from chempare.datatypes import TypeProduct, TypeSupplier

# File: /suppliers/supplier_base.py
class SupplierBase(ClassUtils, metaclass=ABCMeta):
    """Supplier Base Cass"""

    allow_cas_search: bool = False
    """Determines if the supplier allows CAS searches in addition to name
    searches"""

    language_for_search: Any = None
    """For what language it should use for the search query"""

    #_limit = 20
    _supplier: TypeSupplier = None

    def __init__(self, query: str, limit: int = None) -> NoReturn:

        self._limit = limit or 20

        self._products = []
        self._query_results = []
        self._index = 0
        self._query = query
        self._cookies = {}
        self._headers = {}

        self._init_logging()

        self._setup()

        # Execute the basic product search (logic should be in inheriting class)
        self._query_products(self._query)

        # Execute the method that parses self._query_results to define the
        # product properties
        self._parse_products()

    def __len__(self) -> int:
        """len() magic method for getting number of products

        Returns:
            int: Number of entries in self._products array
        """

        return len(self._products)

    def __iter__(self) -> Self:
        """Iterable magic method

        Returns:
            Self: Supplier instance
        """

        return self

    def __next__(self) -> TypeProduct:
        """next magic method

        Raises:
            StopIteration: When the iteration needs to be stopped

        Returns:
            TypeProduct: Next value in line
        """

        if self._index >= len(self._products):
            raise StopIteration

        value = self._products[self._index]
        self._index += 1

        return value

    @property
    @finalmethod
    def products(self) -> List[TypeProduct]:
        """Product title getter

        Returns:
            List[TypeProduct]: List of products
        """

        return self._products

    @finalmethod
    def http_get(
        self,
        path: str = None,
        params: Dict = None,
        cookies: Dict = None,
        headers: Dict = None,
    ) -> requests:
        """Base HTTP getter (not specific to data type).

        Args:
             path: URL Path to get (should not include the self._base_url value)
             params: Dictionary of params to use in request (optional)

         Returns:
             Result from requests.get()
        """

        base_url = self._supplier.get("base_url", None)
        api_url = self._supplier.get("api_url", base_url)

        if not path:
            path = api_url
        elif api_url not in path:
            path = f"{api_url}/{path}"

        return requests.get(
            path,
            params=params,
            impersonate="chrome",
            cookies=cookies or self._cookies,
            headers=headers or self._headers,
        )

    @finalmethod
    def http_post(
        self,
        path: str,
        params: Dict = None,
        data: Any = None,
        json: Union[Dict, List] = None,
        cookies: Dict = None,
        headers: Dict = None,
    ) -> requests:
        """Base HTTP poster (not specific to data type).

        Args:
             path: URL Path to post (should not include the self._base_url
                   value)
             params: Dictionary of params to use in request (optional)
             body: Body of data to post (text, json, etc)

         Returns:
             Result from requests.post()
        """

        api_url = self._supplier.get("api_url", None)
        base_url = self._supplier.get("base_url", None)

        if base_url not in path and (api_url is None or api_url not in path):
            path = f"{base_url}/{path}"

        return requests.post(
            path,
            params=params,
            impersonate="chrome",
            json=json,
            data=data,
            headers=headers or self._headers,
            cookies=cookies or self._cookies,
        )

    @finalmethod
    def http_get_headers(self, **kwargs) -> requests.Headers:
        """Get the response headers for a GET request

        Returns:
            requests.Headers: Header object
        """

        resp = self.http_get(**kwargs)

        return resp.headers

    @finalmethod
    def http_post_json(
        self,
        path: str = None,
        params: Dict = None,
        json: Dict = None,
        headers: Dict = None,
        cookies: Dict = None,
    ) -> Union[Dict, List]:
        """Post a JSON request and get a JSON response

        Args:
            path (str, optional): Path to post to. Defaults to None.
            params (Dict, optional): params object. Defaults to None.
            json (Dict, optional): json body. Defaults to None.
            headers (Dict, optional): override headers. Defaults to None.
            cookies (Dict, optional): override cookies. Defaults to None.

        Returns:
            Union[Dict, List]: JSON response, if there was one
        """

        url = self._supplier.get("api_url", None)

        if path:
            url = f"{url}/{path}"

        req = self.http_post(
            url,
            params=params,
            json=json,
            cookies=cookies or self._cookies,
            headers=headers or self._headers,
        )
        if req is None:
            return None

        return req.json()

    @finalmethod
    def http_get_html(self, path: str = None, params: Dict = None) -> str:
        """HTTP getter (for HTML content).

        Args:
            path: URL Path to get (should not include the self._base_url value)
            params: Dictionary of params to use in request (optional)

        Returns:
            HTML content of response object
        """

        base_url = self._supplier.get("base_url", None)
        api_url = self._supplier.get("api_url", base_url)

        if path and api_url not in path:
            path = f"{api_url}/{path}"

        res = self.http_get(path, params)

        return res.content

    @finalmethod
    def http_get_json(self, path: str = None, **kwargs) -> Union[List, Dict]:
        """HTTP getter (for JSON content).

        Args:
            path: URL Path to get (should not include the self._base_url value)
            params: Dictionary of params to use in request (optional)

        Returns:
            JSON object from response body
        """

        res = self.http_get(path, **kwargs)

        if not res:
            return None

        return res.json()

    def _setup(self, query: str = None) -> NoReturn:
        """Setup method - Triggered before the query is executed. This is
        useful for when we need to make an initial request to a homepage to get
        headers and stores some cookies
        """

    @abstractmethod
    def _query_products(self, query: str) -> NoReturn:
        """Query the website for the products (name or CAS).

        Args:
            query: query string to use

        This should define the self._query_results property with the results
        """

    @abstractmethod
    def _parse_products(self) -> NoReturn:
        """Method to set the local properties for the queried product.

        The self._query_results (populated by calling self._query_products())
        is iterated over by this method, which in turn parses each property and
        creates a new TypeProduct object that gets saved to this._products
        """


if __package__ == "suppliers":
    __disabled__ = True
