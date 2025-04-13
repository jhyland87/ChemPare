import pytest

from chempare.datatypes import TypeProduct
from chempare.suppliers.supplier_chemsavers import SupplierChemsavers as Supplier
from unittest.mock import patch, MagicMock

from tests.mock_data.supplier_chemsavers.chemsavers_mocker import curl_cffi as mock_curl_cffi

curl_cffi_post = MagicMock(wraps=mock_curl_cffi.post)

# Base test class
@pytest.mark.supplier
class TestClass:
    _query = "water"
    _results = None

    @pytest.fixture
    @patch(target='curl_cffi.requests.post', new=curl_cffi_post)
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
    _query = "7664-93-9"
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
