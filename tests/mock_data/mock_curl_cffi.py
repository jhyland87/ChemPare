import inspect
import json
import os
from pathlib import Path
from typing import Any
from typing import Optional
from typing import Unpack
from urllib.parse import urlparse

# from curl_cffi.requests import Request
from curl_cffi.requests.cookies import Cookies
from curl_cffi.requests.cookies import CookieTypes
from curl_cffi.requests.headers import Headers
from curl_cffi.requests.headers import HeaderTypes

# from curl_cffi.requests.models import Response
from curl_cffi.requests.session import HttpMethod
from curl_cffi.requests.session import RequestParams
from curl_cffi.requests.session import ThreadType

from chempare.exceptions import NoMockDataFound


CWD = os.path.dirname(__file__)


class MockResponse:
    # url: url used in the request.
    # content: response body in bytes.
    # text: response body in str.
    # status_code: http status code.
    # reason: http response reason, such as OK, Not Found.
    # ok: is status_code in [200, 400)?
    # headers: response headers.
    # cookies: response cookies.
    # elapsed: how many seconds the request cost.
    # encoding: http body encoding.
    # charset: alias for encoding.
    # primary_ip: primary ip of the server.
    # primary_port: primary port of the server.
    # local_ip: local ip used in this connection.
    # local_port: local port used in this connection.
    # charset_encoding: encoding specified by the Content-Type header.
    # default_encoding: encoding for decoding response content if charset is not found
    #     in headers. Defaults to "utf-8". Can be set to a callable for automatic
    #     detection.
    # redirect_count: how many redirects happened.
    # redirect_url: the final redirected url.
    # http_version: http version used.
    # history: history redirections, only headers are available.

    def __init__(self, url: str, response: dict[str, Any]) -> None:
        # self.request = request
        self.url: str = url
        self.update(response)

    def update(self, response: dict[str, Any]) -> None:
        """Populate the response values"""
        self.encoding: str = response.get("encoding", "utf-8")
        self.content: bytes = bytes(response.get("content", ""), encoding=self.encoding)
        self.status_code: int = response.get("status_code", 200)
        self.reason: str = response.get("reason", "OK")
        self.ok: bool = response.get("ok", True)
        self.headers: HeaderTypes = Headers(response.get("headers", {}))
        self.cookies: CookieTypes = Cookies(response.get("cookies", {}))
        self.elapsed: float = response.get("elapsed", 0.0)
        self.default_encoding: str = response.get("default_encoding", "utf-8")
        self.redirect_count: int = response.get("redirect_count", 0)
        self.redirect_url: str = response.get("redirect_url", "")
        self.http_version: int = response.get("http_version", 0)
        self.primary_ip: str = response.get("primary_ip", "")
        self.primary_port: int = response.get("primary_port", 0)
        self.local_ip: str = response.get("local_ip", "")
        self.local_port: int = response.get("local_port", 0)
        self.history: list[dict[str, Any]] = response.get("history", [])
        self.infos: dict[str, Any] = response.get("infos", {})

    def setdefault(self, key: str, val: Any) -> None:
        """Set the default value of a property"""
        self.__dict__.setdefault(key, val)

    def json(self) -> dict[str, Any] | None:
        """Return json value of content, if it's in json format"""
        # return self.json_content
        try:
            return json.loads(self.text)
        except json.JSONDecodeError:
            return None

    def _decode(self, content: bytes) -> str:
        try:
            return content.decode(self.encoding, errors="replace")
        except (UnicodeDecodeError, LookupError):
            return content.decode("utf-8-sig")

    @property
    def text(self) -> str:
        if not hasattr(self, "_text"):
            if not self.content:
                self._text = ""  # pylint: disable=attribute-defined-outside-init
            else:
                self._text = self._decode(self.content)  # pylint: disable=attribute-defined-outside-init
        return self._text


MockResponse.__name__ = "Response"


def determine_calling_supplier():
    stack = inspect.stack()
    return next(
        (
            s[0].f_locals['self'].__class__.__name__
            for s in stack
            if "self" in s[0].f_locals and s[0].f_locals['self'].__class__.__name__ != "MagicMock"
        ),
        None,
    )


def read_mock_file(file_path):
    """
    Reads a JSON file and returns the data as a Python dictionary.

    Args:
      file_path: The path to the JSON file.

    Returns:
      A Python dictionary representing the JSON data, or None if an error occurs.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = None
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in: {file_path}")
        return None


def get_mock_response_module(supplier: str, req_path: str, test_name: str | None):
    # [
    #   "ok","status_code","charset","charset_encoding",
    #   "default_encoding","encoding","infos","reason"
    # ]

    cwd = os.path.dirname(os.path.abspath(__file__))
    data_root = Path(cwd + os.sep + supplier + req_path)
    if not os.path.isdir(data_root):
        return None

    data_file = f"{data_root}.json"
    alt_data_file = f"{data_root}{os.sep}{test_name}.json"

    # Does the alt data file exist? (the {path}/{test_name}.json), if so, use that
    if test_name and os.path.exists(alt_data_file):
        data_file = Path(alt_data_file)
    # Does the default data file not exist at {path}.json? If so, early falsey return
    elif not os.path.exists(data_file):
        return None

    return read_mock_file(data_file)


def request(
    method: HttpMethod,
    url: str,
    thread: Optional[ThreadType] = None,
    curl_options: Optional[dict] = None,
    debug: Optional[bool] = None,
    **kwargs: Unpack[RequestParams],
) -> MockResponse:
    # print("self.__class__.__module__", self.__class__.__module__)
    mock_cfg = getattr(request, "mock_cfg", None)

    parsed_url = urlparse(url)
    path = parsed_url.path
    if hasattr(mock_cfg, "supplier") is False:
        raise NoMockDataFound(url=url, details="No supplier provided in request.mock_cfg")

    mock_resp = get_mock_response_module(mock_cfg.supplier, path, getattr(mock_cfg, "mock_data", None))

    if not mock_resp:
        raise NoMockDataFound(url=url, supplier=mock_cfg.supplier, details="Mock data file not found or failed to load")

    res = MockResponse(url, response=mock_resp)

    return res


__all__ = ["request"]
