"""SupplierBase module to be inherited by any supplier modules"""

from __future__ import annotations

import json
import logging
import os
from collections.abc import Iterable
from typing import Any
from typing import Dict
from typing import List
from typing import Self
from typing import TypedDict
from urllib.parse import urlparse

# from curl_cffi import Headers
# from curl_cffi import Response
# from curl_cffi import requests
import requests
from abcplus import ABCMeta
from abcplus import abstractmethod
from abcplus import finalmethod
from fuzzywuzzy import fuzz

import chempare
from chempare import ClassUtils
from chempare.datatypes import TypeProduct
from chempare.datatypes import TypeSupplier
from chempare.exceptions import CaptchaEncountered
from chempare.exceptions import NoProductsFound
from chempare.utils import dict_hash
from chempare.utils import replace_dict_values_by_value


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
    _headers = {}

    def __init__(self, query: str, limit: int | None = None, fuzz_ratio: int = 100) -> None:
        self.__init_logging()

        self._fuzz_ratio = fuzz_ratio
        self._limit = limit or 20

        self._products = []
        self._query_results = []
        self._index = 0
        self._query = query
        self._cookies = {}
        # self._headers = {}
        self._save_responses = False

        self._debug_curl: bool = False

        DEBUG_ENV = os.getenv("DEBUG", "false").lower()
        if DEBUG_ENV == "true" or DEBUG_ENV == "1":
            self._debug_curl = True

        SAVE_RESPONSES = os.getenv("SAVE_RESPONSES", "false").lower()
        if SAVE_RESPONSES == "true" or SAVE_RESPONSES == "1":
            self._save_responses = True

        self._request_timeout = int(os.getenv("TIMEOUT", "2000"))

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
        return self.__class__.__module__.split(".")[-1]

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

        x = [
            product
            for product in self._products
            if (product.name and fuzz.partial_ratio(self._query.lower(), product.name.lower()) >= self._fuzz_ratio)
            or (product.title and fuzz.partial_ratio(self._query.lower(), product.title.lower()) >= self._fuzz_ratio)
        ]

        self._products = x

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
    def products(self) -> Iterable[TypeProduct]:
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
        params: dict | None = None,
        cookies: dict | None = None,
        headers: dict | None = None,
    ):
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

        # request-cache seems to have issues if the parameters contain dictionaries or lists.
        # Look for any and convert them to json strings
        if isinstance(params, dict):
            params = replace_dict_values_by_value(params, True, 'true')
            params = replace_dict_values_by_value(params, False, 'false')
            params = replace_dict_values_by_value(params, None, 'null')

            for k, v in params.items():
                if isinstance(v, list) or isinstance(v, dict):
                    params[k] = json.dumps(v)

        args = dict(headers=headers or self._headers, cookies=cookies or self._cookies, timeout=self._request_timeout)
        if requests.get.__module__.split(".", maxsplit=1)[0] == 'requests_cache':
            # if chempare.test_monkeypatching and chempare.called_from_test:
            args["only_if_cached"] = True

        res = requests.get(
            path,
            params,
            **args,
            # impersonate="chrome",
            # cookies=cookies or self._cookies,
            # headers=headers or self._headers,
            # timeout=self._request_timeout,
            # debug=self._debug_curl,
        )

        if res.status_code == 403 and "<title>Just a moment...</title>" in res.text and "cloudflare" in res.text:
            raise CaptchaEncountered(supplier=self._supplier.name, url=res.url, captcha_type="cloudflare")

        return res

    @finalmethod
    def http_post(
        self,
        path: str,
        /,
        params: dict | None = None,
        data: Any = None,
        json: Iterable | None = None,
        cookies: dict | None = None,
        headers: dict | None = None,
    ):
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

        # chempare.test_monkeypatching chempare.called_from_test
        args = dict(
            json=json,
            data=data,
            headers=headers or self._headers,
            cookies=cookies or self._cookies,
            timeout=self._request_timeout,
        )
        if requests.get.__module__.split(".", maxsplit=1)[0] == 'requests_cache':
            args["only_if_cached"] = True

        res = requests.post(
            path,
            params=params,
            **args,
            # impersonate="chrome",
            # json=json,
            # data=data,
            # headers=headers or self._headers,
            # cookies=cookies or self._cookies,
            # timeout=self._request_timeout,
            # debug=self._debug_curl,
        )

        return res

    @finalmethod
    def http_get_headers(self, path: str | None = None, **kwargs):
        """Get the response headers for a GET request

        Returns:
            requests.Headers: Header object
        """

        url = self._supplier.api_url or self._supplier.base_url  # type: ignore

        if path:
            url = f"{url}/{path}"

        args = dict()

        if requests.get.__module__.split(".", maxsplit=1)[0] == 'requests_cache':
            args["only_if_cached"] = True

        # resp = self.http_get(*args, **kwargs)
        resp = requests.head(url, timeout=self._request_timeout, **args, **kwargs)

        return resp.headers

    @finalmethod
    def http_post_json(
        self,
        path: str | None = None,
        /,
        params: dict | None = None,
        json: dict | None = None,
        headers: dict | None = None,
        cookies: dict | None = None,
    ) -> Dict | dict | None:
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
    def http_get_html(self, path: str | None, /, **kwargs) -> bytes:
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

        res = self.http_get(path, **kwargs)

        return res.content

    @finalmethod
    def http_get_json(self, path: str, /, params: dict | None = None, **kwargs) -> dict | None:
        """HTTP getter (for JSON content).

        Args:
            path: URL Path to get (should not include the self._base_url value)
            params: Dictionary of params to use in request (optional)

        Returns:
            JSON object from response body
        """

        res = self.http_get(path, params=params, **kwargs)

        if res is None:
            return None

        return res.json()

    def _setup(self, query: str | None = None) -> None:
        """Setup method - Triggered before the query is executed. This is
        useful for when we need to make an initial request to a homepage to get
        headers and stores some cookies
        """

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
