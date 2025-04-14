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

from curl_cffi.requests.cookies import Cookies
from curl_cffi.requests.cookies import CookieTypes
from curl_cffi.requests.headers import HeaderTypes

# from curl_cffi.requests.session import Response
from curl_cffi.requests.session import Headers
from curl_cffi.requests.session import HttpMethod
from curl_cffi.requests.session import RequestParams
from curl_cffi.requests.session import ThreadType
from curl_request_mocker import CurlRequestMocker
from curl_request_mocker import get_nested_value
from curl_request_mocker import query_to_filename


# HeaderType = MutableMapping[str, Optional[str]]
# CookieType = MutableMapping[str, str]


CWD = os.path.dirname(__file__)


@dataclass
class MockResponse:
    # Must return: url, content, text, status_code, reason, ok, headers, cookies,
    url: str
    # content: bytes = b""
    text: str | None = None
    json_content: Any = None
    status_code: int = 200
    reason: str = "OK"
    ok: bool = True
    headers: HeaderTypes | None = None
    cookies: CookieTypes | None = None

    def json(self):
        return self.json_content

    @property
    def content(self):
        return bytes(json.dumps(self.json_content), encoding="utf-8")


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


def get_mock_response_module(supplier: str, req_path: str):
    mock_data_module_file = Path(f"{supplier}{req_path}.py")
    mock_data_module_name = str(mock_data_module_file.with_suffix('')).replace(os.sep, '.')
    mock_data_abs_file = os.path.dirname(os.path.abspath(__file__)) + "/" + str(mock_data_module_file)

    module_spec = importlib.util.spec_from_file_location(mock_data_module_name, mock_data_abs_file)
    mock_module = importlib.util.module_from_spec(module_spec)
    sys.modules[mock_data_module_name] = mock_module
    module_spec.loader.exec_module(mock_module)

    return mock_module


def request(
    method: HttpMethod,
    url: str,
    thread: Optional[ThreadType] = None,
    curl_options: Optional[dict] = None,
    debug: Optional[bool] = None,
    **kwargs: Unpack[RequestParams],
) -> MockResponse:
    mock_cfg = getattr(request, 'mock_data', None)
    if mock_cfg:
        print(f"Running the CURL request for {mock_cfg=}")

    print(f"Calling request - {method=}, {url=}, {thread=}, {curl_options=}, {debug=}, {kwargs=}")

    parsed_url = urlparse(url)
    path = parsed_url.path
    if hasattr(mock_cfg, 'supplier'):
        mock_resp = get_mock_response_module(mock_cfg.supplier, path)

        cookies_attr = 'cookies'
        headers_attr = 'headers'
        json_content_attr = 'json_content'

        if hasattr(mock_cfg, json_content_attr) and hasattr(mock_resp, getattr(mock_cfg, json_content_attr)):
            json_content_attr = getattr(mock_cfg, json_content_attr)

        # # Are there any overrides configured for this test?
        # cookies_attr = getattr(mock_cfg, 'cookies', 'cookies')
        # headers_attr = getattr(mock_cfg, 'headers', 'headers')
        # json_content_attr = getattr(mock_cfg, 'json_content', 'json_content')

        # Do the overrie(s) exist? If not, go back to the defaults
        # if not hasattr(mock_resp, json_content_attr):
        #     json_content_attr = 'json_content'

        return MockResponse(
            url,
            cookies=Cookies(getattr(mock_resp, cookies_attr, None)),
            headers=Headers(getattr(mock_resp, headers_attr, None)),
            json_content=getattr(mock_resp, json_content_attr, None),
        )

    res = MockResponse(url, content=b"FOOO")

    return res

    # Must return: url, content, text, status_code, reason, ok, headers, cookies,


# def request(*args, **kwargs) -> Response:
#     calling_supplier = determine_calling_supplier()
#     print(f"{calling_supplier=}")
#     print(f"Calling request - {args=}, {kwargs=}")


def post(path, *args, **kwargs):
    calling_supplier = determine_calling_supplier()
    print(f"{calling_supplier=}")
    if not path.endswith('/multi_search') or 'json' not in kwargs or "searches" not in kwargs["json"]:
        return None

    query = get_nested_value(kwargs, ["json", "searches", 0, "q"])

    if not query:
        return None

    fname = query_to_filename(query)

    mock_response_file = f"supplier_chemsavers/response_data/POST__multi_search__{fname}.json"

    return CurlRequestMocker(file=mock_response_file)


def get(path, *args, **kwargs):
    pass


__all__ = ["get", "post", "request"]
