import json
import os
from dataclasses import dataclass
from typing import Dict


@dataclass
class CannedCurlResp(Dict):
    _json_file: str

    def __init__(self, json_file):
        self._json_file = json_file
        self._mock_data_dir = os.path.dirname(os.path.abspath(__file__))
        self._json_path = f"{self._mock_data_dir}/{self._json_file}"
        self.parse_json()

    def parse_json(self) -> None:
        try:
            with open(self._json_path, 'r') as fh:
                self._json = json.load(fh)
        except FileNotFoundError:
            print(f"Error: File not found: {self._json_path}")
            return None
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in: {self._json_path}")
            return None

    def json(self) -> Dict:
        return self._json


class curl_cffi:
    @staticmethod
    def post(path, *args, **kwargs):
        if not path.endswith('/multi_search') or 'json' not in kwargs or "searches" not in kwargs["json"]:
            return None
        return CannedCurlResp(json_file='response_data/POST__multi_search__response.json')

    @staticmethod
    def get(path, *args, **kwargs):
        pass
