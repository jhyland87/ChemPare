"""SupplierBase module to be inherited by any supplier modules"""

from __future__ import annotations

import json
import logging
import os
from typing import Any
from typing import Dict
from typing import List
from typing import Self
from typing import TypedDict
from urllib.parse import urlparse

from abcplus import ABCMeta
from abcplus import abstractmethod
from abcplus import finalmethod
from curl_cffi import Headers
from curl_cffi import Response
from curl_cffi import requests
from fuzzywuzzy import fuzz

import chempare
from chempare import ClassUtils
from chempare.datatypes import TypeProduct
from chempare.datatypes import TypeSupplier
from chempare.exceptions import CaptchaEncountered
from chempare.exceptions import NoProductsFound


# import chempare
class SupplierBase(ClassUtils, metaclass=ABCMeta):
    """SupplierBase module to be inherited by any supplier modules"""

    _supplier: TypeSupplier

    allow_cas_search: bool = False
    """Determines if the supplier allows CAS searches in addition to name
    searches"""

    language_for_search: Any = None
    """For what language it should use for the search query"""

    # def __init_subclass__(cls, **kwargs):
    #     super().__init_subclass__(**kwargs)

    def __init__(self, query: str, limit: int | None = None, fuzz_ratio: int = 100) -> None:
        self.__init_logging()

        self._fuzz_ratio = fuzz_ratio
        self._limit = limit or 20

        self._products = []
        self._query_results = []
        self._index = 0
        self._query = query
        self._cookies = {}
        self._headers = {}
        self._save_responses = False

        self._debug_curl: bool = False

        DEBUG_ENV = os.getenv('DEBUG', 'false').lower()
        if DEBUG_ENV == 'true' or DEBUG_ENV == '1':
            self._debug_curl = True

        SAVE_RESPONSES = os.getenv('SAVE_RESPONSES', 'false').lower()
        if SAVE_RESPONSES == 'true' or SAVE_RESPONSES == '1':
            self._save_responses = True

        if hasattr(self, "_setup"):
            self._setup(query)

        # Execute the basic product search (logic should be in inheriting class)
        self._query_products(self._query)

        # Execute the method that parses self._query_results to define the
        # product properties
        self._parse_products()

        self._fuzz_filter()

        if len(self._products) == 0:
            raise NoProductsFound(supplier=self._supplier.name, query=self._query)

    @finalmethod
    def _type(self):
        return self.__class__.__name__

    @finalmethod
    def _supplier_dir(self):
        return self.__class__.__module__.split('.')[-1]

    @finalmethod
    def __save_as_mock_data(self, response: Response) -> None:
        """
        Save HTTP response in a way it can be used as mock data for unit tests

        Args:
            response (Response): HTTP response from curl_cffi or requests module
        """

        try:
            # Only permit saving data for mock responses if..
            if (
                # 1) Were supposed to
                self._save_responses is False
                # 2) We aren't already monkeypatching (otherwords were just re-saving mock data)
                or chempare.test_monkeypatching is True
                # 3) We're being called from a mock test (Not sure how critical this one is)
                or chempare.called_from_test is False
            ):
                return

            parsed_url = urlparse(response.url)
            path = parsed_url.path

            # For the tests where mock_data is specified, grab that and use it as the last folder in the path.
            suffix = ''
            if hasattr(response, 'mock_cfg') and hasattr(response.mock_cfg, 'mock_data'):  # type: ignore
                suffix = response.mock_cfg.mock_data  # type: ignore

            save_to = os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__),
                    "../../../",
                    "tests/mock_data",
                    self._supplier_dir(),
                    path.lstrip("/"),
                    suffix,
                )
            )

            keys_to_extract = [
                "content",
                "status_code",
                "reason",
                "ok",
                "headers",
                "cookies",
                "elapsed",
                "default_encoding",
                "redirect_count",
                "redirect_url",
                "http_version",
                "primary_ip",
                "primary_port",
                "local_ip",
                "local_port",
                "infos",
                "encoding",
            ]

            mock_file_json = {}
            for key in keys_to_extract:
                if key in response.__dict__:
                    if hasattr(response.__dict__[key], "__dict__"):
                        mock_file_json[key] = dict(response.__dict__[key])
                    elif isinstance(response.__dict__[key], bytes):
                        mock_file_json[key] = response.__dict__[key].decode(
                            getattr(response, "encoding", "utf-8-sig"), errors="replace"
                        )
                    else:
                        mock_file_json[key] = response.__dict__[key]

            parent_dir = os.path.dirname(save_to)
            os.makedirs(parent_dir, exist_ok=True)

            # Save the response body
            with open(f"{save_to}.json", "w", encoding="utf-8") as file:
                file.write(json.dumps(mock_file_json, indent=4))

        except Exception as e:
            print("Exception in __save_as_mock_data:", e)

    @finalmethod
    def __init_logging(self) -> None:
        """Create the logger specific to this class instance (child)

        Returns:
            None: None

        Note:
            Uses the LOG_LEVEL env var for the log level. Valid values are:
            CRITICAL FATAL ERROR WARNING INFO DEBUG. The default is WARNING
        """

        self._logger = logging.getLogger(str(self.__class__.__name__))
        logging.basicConfig(level=os.environ.get("LOG_LEVEL", "WARNING"))

    @finalmethod
    def _log(self, message: str) -> None:
        """Create a regular log entry

        Args:
            message (str): Message to send to the logs

        Returns:
            None: None
        """

        self._logger.log(logging.INFO, message)

    @finalmethod
    def _debug(self, message: str) -> None:
        """Create a debugger log entry

        Args:
            message (str): Message to send to the logs

        Returns:
            None: None
        """

        self._logger.log(logging.DEBUG, message)

    @finalmethod
    def _error(self, message: str) -> None:
        """Create an error log entry

        Args:
            message (str): Message to send to the logs

        Returns:
            None: None
        """

        self._logger.log(logging.ERROR, message)

    @finalmethod
    def _warn(self, message: str) -> None:
        """Create a warning log entry

        Args:
            message (str): Message to send to the logs

        Returns:
            None: None
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

    @finalmethod
    def _fuzz_filter(self) -> None:
        """Filter products for ones where the title has a partial fuzz ratio of
        90% or more.
        When testing different fuzz methods with string 'sodium borohydride',
        partial_ratio would return 58 for 'sodium amide' and 67 for 'sodium
        triacetoxyborohydride', where as both token_set_ratio and ratio would
        return 67 and 78 respectively. For this reason, I decided that using
        partial_ratio would give more reliable results.
        Fuzz method comparison tests can be found in dev/fuzz-test.py

        Todo: May be worth excluding anything in parenthesis, which would help
              exclude false positives such as:
                Borane - Tetrahydrofuran Complex (8.5% in Tetrahydrofuran,
                ca. 0.9mol/L) (stabilized with Sodium Borohydride) 500mL
        """
        if not self._products or isinstance(self._fuzz_ratio, int) is False or self._is_cas(self._query):
            return

        self._products = [
            product
            for product in self._products
            if (product.name and fuzz.partial_ratio(self._query.lower(), product.name.lower()) >= self._fuzz_ratio)
            or (product.title and fuzz.partial_ratio(self._query.lower(), product.title.lower()) >= self._fuzz_ratio)
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
        path: str | None = None,
        /,
        params: Dict | None = None,
        cookies: Dict | None = None,
        headers: Dict | None = None,
    ) -> Response:
        """Base HTTP getter (not specific to data type).

        Args:
             path: URL Path to get (should not include the self._base_url value)
             params: Dictionary of params to use in request (optional)

         Returns:
             Result from requests.get()
        """

        base_url = self._supplier.base_url
        api_url = self._supplier.api_url or base_url

        if not path:
            path = api_url
        elif api_url not in path:
            path = f"{api_url}/{path}"

        res = requests.get(
            path,
            params=params,
            impersonate="chrome",
            cookies=cookies or self._cookies,
            headers=headers or self._headers,
            debug=self._debug_curl,
        )

        self.__save_as_mock_data(res)

        if res.status_code == 403 and "<title>Just a moment...</title>" in res.text and "cloudflare" in res.text:
            raise CaptchaEncountered(supplier=self._supplier.name, url=res.url, captcha_type="cloudflare")

        return res

    @finalmethod
    def http_post(
        self,
        path: str,
        /,
        params: Dict | None = None,
        data: Any = None,
        json: Dict | List | None = None,
        cookies: Dict | None = None,
        headers: Dict | None = None,
    ) -> Response:
        """Base HTTP poster (not specific to data type).

        Args:
             path: URL Path to post (should not include the self._base_url
                   value)
             params: Dictionary of params to use in request (optional)
             body: Body of data to post (text, json, etc)

         Returns:
             Result from requests.post()
        """

        base_url = self._supplier.base_url
        api_url = self._supplier.api_url or base_url

        if base_url not in path and (api_url is None or api_url not in path):
            path = f"{base_url}/{path}"

        res = requests.post(
            path,
            params=params,
            impersonate="chrome",
            json=json,
            data=data,
            headers=headers or self._headers,
            cookies=cookies or self._cookies,
            debug=self._debug_curl,
        )

        self.__save_as_mock_data(res)

        return res

    @finalmethod
    def http_get_headers(self, *args, **kwargs) -> Headers:
        """Get the response headers for a GET request

        Returns:
            requests.Headers: Header object
        """

        resp = self.http_get(*args, **kwargs)

        return resp.headers

    @finalmethod
    def http_post_json(
        self,
        path: str | None = None,
        /,
        params: Dict | None = None,
        json: Dict | None = None,
        headers: Dict | None = None,
        cookies: Dict | None = None,
    ) -> Dict | List | None:
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

        url = self._supplier.api_url or self._supplier.base_url  # type: ignore

        if path:
            url = f"{url}/{path}"

        req = self.http_post(
            url, params=params, json=json, cookies=cookies or self._cookies, headers=headers or self._headers
        )
        if req is None:
            return None

        return req.json()

    @finalmethod
    def http_get_html(self, path: str | None = None, /, params: Dict | None = None) -> bytes:
        """HTTP getter (for HTML content).

        Args:
            path: URL Path to get (should not include the self._base_url value)
            params: Dictionary of params to use in request (optional)

        Returns:
            HTML content of response object
        """

        base_url = self._supplier.base_url
        api_url = self._supplier.api_url or base_url

        if path and api_url not in path:
            path = f"{api_url}/{path}"

        res = self.http_get(path, params)

        return res.content

    @finalmethod
    def http_get_json(self, path: str | None = None, /, **kwargs) -> List | Dict | None:
        """HTTP getter (for JSON content).

        Args:
            path: URL Path to get (should not include the self._base_url value)
            params: Dictionary of params to use in request (optional)

        Returns:
            JSON object from response body
        """

        res = self.http_get(path, **kwargs)

        if res is None:
            return None

        return res.json()

    def _setup(self, query: str | None = None) -> None:
        """Setup method - Triggered before the query is executed. This is
        useful for when we need to make an initial request to a homepage to get
        headers and stores some cookies
        """

    # @staticmethod
    # def is_in_test():
    #     return chempare.called_from_test

    @abstractmethod
    def _query_products(self, query: str) -> None:
        """Query the website for the products (name or CAS).

        Args:
            query: query string to use

        This should define the self._query_results property with the results
        """

    @abstractmethod
    def _parse_products(self) -> None:
        """Method to set the local properties for the queried product.

        The self._query_results (populated by calling self._query_products())
        is iterated over by this method, which in turn parses each property and
        creates a new TypeProduct object that gets saved to this._products
        """


__disabled__ = True
