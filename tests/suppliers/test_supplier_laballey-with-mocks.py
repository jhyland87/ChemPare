# pylint: disable=unused-import
# pylint: disable=unused-wildcard-import
# pylint: disable=wildcard-import
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=unused-argument
# pylint: disable=broad-exception-caught
import os

# import mock
import pytest

# import requests_mock
# from curl_cffi import requests
from pytest_mock import MockerFixture

from chempare.datatypes import TypeProduct
from chempare.suppliers import SupplierLaballey as Supplier  # type: ignore
from definitions import mock_data_dir


# from decimal import Decimal


# from curl_cffi import requests


# with open('tests/mock_data/laballey-get-getwidgets.json', 'r') as file:
#     # mock_json = json.load(file)
#     mock_json = file.read()
#     print(mock_json)

# session = requests.Session()
# adapter = requests_mock.Adapter()
# session.mount('mock://', adapter)
# adapter.register_uri('GET', 'mock://searchserverapi.com', text='{"foo":"bar"}')
# with requests_mock.Mocker() as m:
#     r = m.get('https://searchserverapi.com', text='{"foo":"bar"}')
#     print("r.txt:", r.txt)


# @requests_mock.Mocker()
# def test_func(m):
#     m.get('https://searchserverapi.com', text='data')
#     return requests.get('https://searchserverapi.com').text


@pytest.fixture
def mock_object_property(mocker: MockerFixture):
    mock_get = mocker.patch("curl_cffi.requests.get")
    filepath = os.path.join(mock_data_dir, "laballey-get-getwidgets.json")
    # 'tests/mock_data/laballey-get-getwidgets.json',
    with open(file=filepath, mode='r', encoding="utf-8") as file:
        # mock_json = json.load(file)
        mock_json = file.read()
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = mock_json
    return mock_get


# Base test class
@pytest.mark.supplier
class TestClass:
    _query = "acid"
    _results = None

    @pytest.fixture
    def results(self):
        if not self._results:
            try:
                self._results = Supplier(self._query)
            except Exception as e:
                self._results = e

        return self._results


# Test cases for a valid search for this supplier
class TestValidSearch(TestClass):
    _results = None

    # @mock_http(url="https://searchserverapi.com/getwidgets", params={}, response={})
    def test_query(self, mock_object_property, results):
        assert isinstance(results, Exception) is False
        assert hasattr(results, "__iter__") is True
        assert hasattr(results, "products") is True
        assert (
            isinstance(results.products, list) is True
        ), "Return data is not instance of TypeProduct"

        mock_object_property.assert_called_once_with(
            "https://searchserverapi.com/getwidgets",
            params={
                'api_key': '8B7o0X1o7c',
                'q': 'acid',
                'maxResults': 6,
                'startIndex': 0,
                'items': True,
                'pages': False,
                'facets': False,
                'categories': True,
                'suggestions': True,
                'vendors': False,
                'tags': False,
                'pageStartIndex': 0,
                'pagesMaxResults': 10,
                'categoryStartIndex': 0,
                'categoriesMaxResults': 3,
                'suggestionsMaxResults': 4,
                'vendorsMaxResults': 3,
                'tagsMaxResults': 3,
                'output': 'json',
                '_': 1234567890,
            },
            impersonate='chrome',
            cookies={},
            headers={},
        )

    def test_results(self, results):
        # assert results == "test"
        assert len(results) > 0, "No product results found"
        assert isinstance(results.products[0], TypeProduct) is True


# Test cases for invalid searches for this supplier
class TestInvalidSearch(TestClass):
    _query = "This_should_return_no_results"
    _results = None

    def test_query(self, results):
        assert isinstance(results, Exception) is False
        assert hasattr(results, "__iter__") is True
        assert hasattr(results, "products") is True
        assert (
            isinstance(results.products, list) is True
        ), "Return data is not instance of TypeProduct"

    def test_results(self, results):
        assert len(results) == 0


# Test cases for a valid CAS search for this supplier
class TestValidCASSearch(TestClass):
    _query = "7732-18-5"
    _results = None

    def test_query(self, results):
        assert isinstance(results, Exception) is False
        assert hasattr(results, "__iter__") is True
        assert hasattr(results, "products") is True
        assert (
            isinstance(results.products, list) is True
        ), "Return data is not instance of TypeProduct"

    def test_results(self, results):
        assert len(results) > 0, "No product results found"
        assert isinstance(results.products[0], TypeProduct) is True


# Test cases for an invalid CAS search for this supplier
class TestInvalidCASSearch(TestClass):
    _query = "7782-77-6"  # Nitrous acid, too stable to be sold
    _results = None

    def test_query(self, results):
        assert isinstance(results, Exception) is False
        assert hasattr(results, "__iter__") is True
        assert hasattr(results, "products") is True
        assert (
            isinstance(results.products, list) is True
        ), "Return data is not instance of TypeProduct"

    def test_results(self, results):
        assert len(results) == 0
