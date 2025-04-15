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
from curl_cffi.requests.headers import Headers
from curl_cffi.requests.headers import HeaderTypes
from curl_cffi.requests.session import HttpMethod
from curl_cffi.requests.session import RequestParams
from curl_cffi.requests.session import ThreadType


CWD = os.path.dirname(__file__)


@dataclass
class MockResponse:
    # Must return: url, content, text, status_code, reason, ok, headers, cookies,
    url: str
    text: str | None = None
    json_content: Any = None
    status_code: int = 200
    reason: str = "OK"
    ok: bool = True
    headers: HeaderTypes | None = None
    cookies: CookieTypes | None = None

    def json(self):
        # return self.json_content
        if self.text is not None:
            return json.load(self.text)

    @property
    def content(self):
        if self.text is not None:
            return bytes(self.text, encoding="utf-8")  # or ascii?
        # if self.json_content is not None:
        #     return bytes(json.dumps(self.json()), encoding="utf-8")  # or ascii?
        # if self.body is not None:
        #     return bytes(self.body)


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
            # if file_path.endswith('.json'):
            #     data = json.load(file)
            # else:
            #     data = file.read()
            data = file.read()
            return data
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in: {file_path}")
        return None


def get_mock_response_module(supplier: str, req_path: str, test_name: str | None):
    cwd = os.path.dirname(os.path.abspath(__file__))
    data_root = Path(f"{cwd}/{supplier}{req_path}")
    if not os.path.isdir(data_root):
        return None

    alt_data_root = None

    if test_name and os.path.isdir(f"{str(data_root)}/{test_name}"):
        alt_data_root = Path(f"{str(data_root)}/{test_name}")

    header_file = None
    cookie_file = None
    body_file = None

    if alt_data_root and os.path.exists(f"{str(alt_data_root)}/headers.json"):
        header_file = f"{str(alt_data_root)}/headers.json"
    elif os.path.exists(f"{str(data_root)}/headers.json"):
        header_file = f"{str(data_root)}/headers.json"

    if alt_data_root and os.path.exists(f"{str(alt_data_root)}/cookies.json"):
        cookie_file = f"{str(alt_data_root)}/cookies.json"
    elif os.path.exists(f"{str(data_root)}/cookies.json"):
        cookie_file = f"{str(data_root)}/cookies.json"

    if alt_data_root and os.path.exists(f"{str(alt_data_root)}/body.json"):
        body_file = f"{str(alt_data_root)}/body.json"
    elif os.path.exists(f"{str(data_root)}/body.json"):
        body_file = f"{str(data_root)}/body.json"
    elif alt_data_root and os.path.exists(f"{str(alt_data_root)}/body.html"):
        body_file = f"{str(alt_data_root)}/body.html"
    elif os.path.exists(f"{str(data_root)}/body.html"):
        body_file = f"{str(data_root)}/body.html"

    result = {}

    if header_file:
        result['headers'] = read_mock_file(header_file)

    if cookie_file:
        result['cookies'] = read_mock_file(cookie_file)

    if body_file:
        result['text'] = read_mock_file(body_file)

    return result
    # mock_data_module_file = Path(f"{supplier}{req_path}.py")
    # mock_data_module_name = str(mock_data_module_file.with_suffix('')).replace(os.sep, '.')
    # mock_data_abs_file = os.path.dirname(os.path.abspath(__file__)) + "/" + str(mock_data_module_file)

    # module_spec = importlib.util.spec_from_file_location(mock_data_module_name, mock_data_abs_file)
    # mock_module = importlib.util.module_from_spec(module_spec)
    # sys.modules[mock_data_module_name] = mock_module
    # module_spec.loader.exec_module(mock_module)

    # return mock_module


def request(
    method: HttpMethod,
    url: str,
    thread: Optional[ThreadType] = None,
    curl_options: Optional[dict] = None,
    debug: Optional[bool] = None,
    **kwargs: Unpack[RequestParams],
) -> MockResponse:
    mock_cfg = getattr(request, 'mock_cfg', None)

    parsed_url = urlparse(url)
    path = parsed_url.path
    if hasattr(mock_cfg, 'supplier'):
        mock_resp = get_mock_response_module(mock_cfg.supplier, path, getattr(mock_cfg, 'mock_data', None))

        return MockResponse(
            url,
            cookies=Cookies(mock_resp.get('cookies', {})),
            headers=Headers(mock_resp.get('headers', {})),
            text=mock_resp.get('text', {}),
        )

    res = MockResponse(url, text="No mock data found")

    return res


__all__ = ["request"]
