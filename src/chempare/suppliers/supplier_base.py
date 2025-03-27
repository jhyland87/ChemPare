"""SupplierBase module to be inherited by any supplier modules"""

import logging
import os
from typing import Any
from typing import Dict
from typing import List
from typing import NoReturn
from typing import Self
from typing import Union

from abcplus import ABCMeta
from abcplus import abstractmethod
from abcplus import finalmethod
from curl_cffi import requests

from chempare import ClassUtils
from chempare.datatypes import TypeProduct


class SupplierBase(ClassUtils, metaclass=ABCMeta):
    """SupplierBase module to be inherited by any supplier modules"""

    allow_cas_search: bool = False
    """Determines if the supplier allows CAS searches in addition to name
    searches"""

    language_for_search: Any = None
    """For what language it should use for the search query"""

    def __init__(
        self, query: str, limit: int = None, exact: bool = False
    ) -> NoReturn:
        self.__init_logging()

        self._exact_match = exact
        self._limit = limit or 20

        self._products = []
        self._query_results = []
        self._index = 0
        self._query = query
        self._cookies = {}
        self._headers = {}

        if hasattr(self, "_setup"):
            self._setup(query)

        # Execute the basic product search (logic should be in inheriting class)
        self._query_products(self._query)

        # Execute the method that parses self._query_results to define the
        # product properties
        self._parse_products()

        self._filter_exact()

    def __init_logging(self) -> NoReturn:
        """Create the logger specific to this class instance (child)

        Returns:
            NoReturn: None

        Note:
            Uses the LOG_LEVEL env var for the log level. Valid values are:
            CRITICAL FATAL ERROR WARNING INFO DEBUG. The default is WARNING
        """

        self._logger = logging.getLogger(str(self.__class__.__name__))
        logging.basicConfig(level=os.environ.get("LOG_LEVEL", "WARNING"))

    def _log(self, message: str) -> NoReturn:
        """Create a regular log entry

        Args:
            message (str): Message to send to the logs

        Returns:
            NoReturn: None
        """

        self._logger.log(logging.INFO, message)

    def _debug(self, message: str) -> NoReturn:
        """Create a debugger log entry

        Args:
            message (str): Message to send to the logs

        Returns:
            NoReturn: None
        """

        self._logger.log(logging.DEBUG, message)

    def _error(self, message: str) -> NoReturn:
        """Create an error log entry

        Args:
            message (str): Message to send to the logs

        Returns:
            NoReturn: None
        """

        self._logger.log(logging.ERROR, message)

    def _warn(self, message: str) -> NoReturn:
        """Create a warning log entry

        Args:
            message (str): Message to send to the logs

        Returns:
            NoReturn: None
        """

        self._logger.log(logging.WARN, message)

        # CRITICAL = 50
        # FATAL = CRITICAL
        # ERROR = 40
        # WARNING = 30
        # WARN = WARNING
        # INFO = 20
        # DEBUG = 10
        # NOTSET = 0

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

    def _filter_exact(self) -> NoReturn:
        """Filter products for exact query match

        Todo: May be worth excluding anything in parenthesis, which would help
              exclude false positives such as:
                Borane - Tetrahydrofuran Complex (8.5% in Tetrahydrofuran,
                ca. 0.9mol/L) (stabilized with Sodium Borohydride) 500mL
        """
        if (
            not self._products
            or self._exact_match is False
            or self._is_cas(self._query)
        ):
            return

        self._products = [
            product
            for product in self._products
            if self._contains_exact_match(product.name, self._query)
        ]

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
