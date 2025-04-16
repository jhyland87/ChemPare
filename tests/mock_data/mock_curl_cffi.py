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

from chempare.exceptions import NoMockDataFound


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

    def update(self, data: Dict) -> None:
        self.__dict__.update(data)

    def json(self):
        # return self.json_content
        if self.text is not None:
            return json.loads(self.text)

    @property
    def content(self):

        if self.text is not None:
            if isinstance(self.text, bytes):
                return self.text
            return bytes(str(self.text), encoding="utf-8")  # or ascii?
        # if self.json_content is not None:
        #     return bytes(json.dumps(self.json()), encoding="utf-8")  # or ascii?
        # if self.body is not None:
        #     return bytes(self.body)
        return b""


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
            try:
                data = file.read()
                return json.loads(data)
            except json.JSONDecodeError as e:
                return data
                # return e.doc
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

    alt_data_root = None

    if test_name and os.path.isdir(str(data_root) + os.sep + test_name):
        alt_data_root = Path(str(data_root) + os.sep + test_name)

    header_file = None
    cookie_file = None
    body_file = None
    metadata_file = None

    # Grab the headers if any are present
    if alt_data_root and os.path.exists(str(alt_data_root) + os.sep + "headers.json"):
        header_file = str(alt_data_root) + os.sep + "headers.json"
    elif os.path.exists(str(data_root) + os.sep + "headers.json"):
        header_file = str(data_root) + os.sep + "headers.json"

    # Cookies
    if alt_data_root and os.path.exists(str(alt_data_root) + os.sep + "cookies.json"):
        cookie_file = str(alt_data_root) + os.sep + "cookies.json"
    elif os.path.exists(str(data_root) + os.sep + "cookies.json"):
        cookie_file = str(data_root) + os.sep + "cookies.json"

    # Metadata (http response code, etc)
    if alt_data_root and os.path.exists(str(alt_data_root) + os.sep + "metadata.json"):
        metadata_file = str(alt_data_root) + os.sep + "metadata.json"
    elif os.path.exists(str(data_root) + os.sep + "metadata.json"):
        metadata_file = str(data_root) + os.sep + "metadata.json"

    # Body content (json, html or txt)
    if alt_data_root and os.path.exists(str(alt_data_root) + os.sep + "body.json"):
        body_file = str(alt_data_root) + os.sep + "body.json"
    elif os.path.exists(str(data_root) + os.sep + "body.json"):
        body_file = str(data_root) + os.sep + "body.json"
    elif alt_data_root and os.path.exists(str(alt_data_root) + os.sep + "body.html"):
        body_file = str(alt_data_root) + os.sep + "body.html"
    elif os.path.exists(str(data_root) + os.sep + "body.html"):
        body_file = str(data_root) + os.sep + "body.html"
    elif alt_data_root and os.path.exists(str(alt_data_root) + os.sep + "body.txt"):
        body_file = str(alt_data_root) + os.sep + "body.txt"
    elif os.path.exists(str(data_root) + os.sep + "body.txt"):
        body_file = str(data_root) + os.sep + "body.txt"

    result = {}

    if header_file:
        result['headers'] = read_mock_file(header_file)

    if cookie_file:
        result['cookies'] = read_mock_file(cookie_file)

    if metadata_file:
        result['metadata'] = read_mock_file(metadata_file)

    if body_file:
        # text? Or text?
        result['text'] = read_mock_file(body_file)
        if result['text'] and (isinstance(result['text'], dict) or isinstance(result['text'], list)):
            result['text'] = bytes(json.dumps(result['text']), encoding="utf-8")

    return result


def request(
    method: HttpMethod,
    url: str,
    thread: Optional[ThreadType] = None,
    curl_options: Optional[dict] = None,
    debug: Optional[bool] = None,
    **kwargs: Unpack[RequestParams],
) -> MockResponse:
    mock_cfg = getattr(request, "mock_cfg", None)

    parsed_url = urlparse(url)
    path = parsed_url.path
    if hasattr(mock_cfg, "supplier") is False:
        raise NoMockDataFound(url=url)

    mock_resp = get_mock_response_module(mock_cfg.supplier, path, getattr(mock_cfg, "mock_data", None))

    res = MockResponse(
        url,
        cookies=Cookies(mock_resp.get("cookies", {})),
        headers=Headers(mock_resp.get("headers", {})),
        # text=bytes(json.dumps(mock_resp.get('text', None)), encoding="utf-8")
        text=mock_resp.get("text", b""),
    )

    res.update(mock_resp.get("metadata", {}))

    return res

    # res = MockResponse(url, text="No mock data found")

    # return res


__all__ = ["request"]
