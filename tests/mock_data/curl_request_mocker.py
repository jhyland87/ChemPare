import json
import os
from dataclasses import dataclass
from typing import Dict
import inflection

def query_to_filename(query:str) -> str:
    query = query.replace("_","-")
    fname = inflection.parameterize(query)
    return fname


def get_nested_value(obj, keys):
    try:
        value = obj
        for key in keys:
            #value = getattr(value, key)
            if isinstance(value, list):
                if len(value) == 0:
                    return None

                if isinstance(key, int):
                    value = value[key]

            elif isinstance(value, dict):
                value = value.get(key)
            else:
                value = getattr(value, key)
        return value
    except (AttributeError, TypeError):
        return None

@dataclass
class CurlRequestMocker(Dict):
    """Simple http reply mocker"""

    _mock_file: str
    """Location of the mock file (txt, json, html, etc)"""

    _json :str|None
    """Loaded JSON content (only called if self.json() is triggered)"""

    _mock_file_content :str|None
    """Raw file content"""

    def __init__(self, file:str):
        self._mock_file = file
        self._mock_data_dir = os.path.dirname(os.path.abspath(__file__))
        self._mock_file_path = f"{self._mock_data_dir}/{self._mock_file}"
        self._json = None
        self._mock_file_content = None
        self._read_mock_file()

    def _read_mock_file(self):
        if not os.path.exists(self._mock_file_path):
            raise FileNotFoundError(f"No mock file found at {self._mock_file_path}")

        with open(self._mock_file_path, "r", encoding="utf-8") as fh:
            self._mock_file_content = fh.read()
            try:
                self._json = json.loads(self._mock_file_content)
            except json.JSONDecodeError:
                pass

    @property
    def content(self):
        if not self._mock_file_content:
            return None
        return self._mock_file_content

    def json(self):
        if not self._json:
            return None
        return self._json



__all__ = ['query_to_filename','get_nested_value','CurlRequestMocker']
