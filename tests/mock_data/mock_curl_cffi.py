import importlib
import inspect
import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from typing import Dict
from typing import MutableMapping
from typing import Optional
from typing import Unpack
from urllib.parse import urlparse

# from curl_cffi.requests import Request
from curl_cffi.requests.cookies import Cookies
from curl_cffi.requests.cookies import CookieTypes
from curl_cffi.requests.headers import Headers
from curl_cffi.requests.headers import HeaderTypes
from curl_cffi.requests.models import Response
from curl_cffi.requests.session import HttpMethod
from curl_cffi.requests.session import RequestParams
from curl_cffi.requests.session import ThreadType

from chempare.exceptions import NoMockDataFound


CWD = os.path.dirname(__file__)


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

# "ok": response.ok,
# "status_code": response.status_code,
# "charset": response.charset,
# "encoding": response.encoding,
# "charset_encoding": response.charset_encoding,
# "default_encoding": response.default_encoding,
# "infos": response.infos,
# "reason": response.reason,
# "text": str(response.text),
# "headers": dict(response.headers),
# "cookies": dict(response.cookies),


class MockResponse:
    # Must return: url, content, text, status_code, reason, ok, headers, cookies,
    # url: str
    # text: str | None = None
    # status_code: int = 200
    # request:Request|None = None
    # reason: str = "OK"
    # ok: bool = True
    # headers: HeaderTypes = Headers()
    # cookies: CookieTypes = Cookies()
    # encoding: str | None = None
    # charset: str | None = None
    # default_encoding: str | None = None
    # charset_encoding: str | None = None
    # infos: dict[str, Any] = {}
    def __init__(self, url: str, response: dict[str, Any]) -> None:
        # self.request = request
        self.url = url
        self.content = bytes(response.get("content", ""), encoding="utf-8")
        self.status_code = response.get("status_code", 200)
        self.reason = response.get("reason", "OK")
        self.ok = response.get("ok", True)
        self.headers = Headers(response.get("headers", {}))
        self.cookies = Cookies(response.get("cookies", {}))
        self.elapsed = 0.0
        self.default_encoding = response.get("default_encoding", "utf-8")
        self.encoding = response.get("encoding", "utf-8")
        self.redirect_count = 0
        self.redirect_url = ""
        self.http_version = 0
        self.primary_ip: str = ""
        self.primary_port: int = 0
        self.local_ip: str = ""
        self.local_port: int = 0
        self.history: list[dict[str, Any]] = []
        self.infos: dict[str, Any] = response.get("infos", {})

    # def update(self, data: dict[str, Any]) -> None:
    #     self.__dict__.update(data)

    def setdefault(self, key: str, val: Any) -> None:
        """Set the default value of a property"""
        self.__dict__.setdefault(key, val)

    def json(self) -> dict[str, Any] | None:
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
                self._text = ""
            else:
                self._text = self._decode(self.content)
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
            # try:
            #     data = file.read()
            #     return json.loads(data)
            # except json.JSONDecodeError as e:
            #     return data
            # return e.doc
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in: {file_path}")
        return None


def get_mock_response_module(supplier: str, req_path: str, test_name: str | None):
    # ["ok","status_code","charset","charset_encoding","default_encoding","encoding","infos","reason"]

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

    # # Cookies
    # if alt_data_root and os.path.exists(str(alt_data_root) + os.sep + "cookies.json"):
    #     cookie_file = str(alt_data_root) + os.sep + "cookies.json"
    # elif os.path.exists(str(data_root) + os.sep + "cookies.json"):
    #     cookie_file = str(data_root) + os.sep + "cookies.json"

    # # Metadata (http response code, etc)
    # if alt_data_root and os.path.exists(str(alt_data_root) + os.sep + "metadata.json"):
    #     metadata_file = str(alt_data_root) + os.sep + "metadata.json"
    # elif os.path.exists(str(data_root) + os.sep + "metadata.json"):
    #     metadata_file = str(data_root) + os.sep + "metadata.json"

    # # Body content (json, html or txt)
    # if alt_data_root and os.path.exists(str(alt_data_root) + os.sep + "body.json"):
    #     body_file = str(alt_data_root) + os.sep + "body.json"
    # elif os.path.exists(str(data_root) + os.sep + "body.json"):
    #     body_file = str(data_root) + os.sep + "body.json"
    # elif alt_data_root and os.path.exists(str(alt_data_root) + os.sep + "body.html"):
    #     body_file = str(alt_data_root) + os.sep + "body.html"
    # elif os.path.exists(str(data_root) + os.sep + "body.html"):
    #     body_file = str(data_root) + os.sep + "body.html"
    # elif alt_data_root and os.path.exists(str(alt_data_root) + os.sep + "body.txt"):
    #     body_file = str(alt_data_root) + os.sep + "body.txt"
    # elif os.path.exists(str(data_root) + os.sep + "body.txt"):
    #     body_file = str(data_root) + os.sep + "body.txt"

    mock_json = read_mock_file(data_file)

    return mock_json
    # result = {}

    # if header_file:
    #     result['headers'] = read_mock_file(header_file)

    # if cookie_file:
    #     result['cookies'] = read_mock_file(cookie_file)

    # if metadata_file:
    #     result['metadata'] = read_mock_file(metadata_file)

    # if body_file:
    #     # text? Or text?
    #     result['text'] = read_mock_file(body_file)
    #     if result['text'] and (isinstance(result['text'], dict) or isinstance(result['text'], list)):
    #         result['text'] = bytes(json.dumps(result['text']), encoding="utf-8")

    # return result


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

    # res = MockResponse(
    #     url,
    #     cookies=Cookies(mock_resp.get("cookies", {})),
    #     headers=Headers(mock_resp.get("headers", {})),
    #     # text=bytes(json.dumps(mock_resp.get('text', None)), encoding="utf-8")
    #     text=mock_resp.get("text", b""),
    # )

    # res.update(mock_resp.get("metadata", {}))

    res = MockResponse(
        url,
        response=mock_resp,
        # cookies=Cookies(mock_resp.get("cookies", {})),
        # headers=Cookies(mock_resp.get("headers", {})),
        # text=mock_resp.get("text", b""),
    )

    # res.amend(mock_resp)

    return res

    # res = MockResponse(url, text="No mock data found")

    # return res


__all__ = ["request"]
