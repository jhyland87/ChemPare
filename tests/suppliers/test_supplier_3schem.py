import pytest

from chempare.datatypes import TypeProduct
from chempare.suppliers import Supplier3SChem as Supplier  # type: ignore


# from base_test import SupplierBaseTest


# Base test class


@pytest.mark.skip(reason="Trying to fix it")
@pytest.mark.supplier
class TestClass:
    _query = "clean"
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

    def test_query(self, results):
        assert isinstance(results, Exception) is False
        assert hasattr(results, "__iter__") is True
        assert hasattr(results, "products") is True
        assert (
            isinstance(results.products, list) is True
        ), "Return data is not instance of TypeProduct"

    def test_results(self, results):
        assert len(results) > 0, "No product results found"
        assert (
            isinstance(results.products[0], TypeProduct) is True
        ), "Return data is not instance of TypeProduct"


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
