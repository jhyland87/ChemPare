import pytest
from pytest_attributes import attributes

from chempare.datatypes import TypeProduct
from chempare.suppliers.supplier_base import NoProductsFound
from chempare.suppliers.supplier_laboratoriumdiscounter import SupplierLaboratoriumDiscounter as Supplier


@attributes(supplier="laboratoriumdiscounter", mock_data="query-acid")
def test_name_query():
    try:
        results = Supplier("acid")
        assert isinstance(results, Exception) is False
        assert hasattr(results, "__iter__") is True
        assert hasattr(results, "products") is True
        assert isinstance(results.products, list) is True, "Return data is not instance of TypeProduct"
    except Exception as e:
        results = e

    assert isinstance(results, Exception) is False, "query returned an exception"


@attributes(supplier="laboratoriumdiscounter", mock_data="query-7664-93-9")
def test_cas_query():
    try:
        results = Supplier("7664-93-9")
        assert isinstance(results, Exception) is False
        assert hasattr(results, "__iter__") is True
        assert hasattr(results, "products") is True
        assert isinstance(results.products, list) is True, "Return data is not instance of TypeProduct"
    except Exception as e:
        results = e

    assert isinstance(results, Exception) is False, "query returned an exception"


@attributes(supplier="laboratoriumdiscounter", mock_data="query-nonsense")
def test_nonsense_query():
    results = None
    try:
        with pytest.raises(NoProductsFound) as notfound_error:
            results = Supplier("this_should_return_no_search_result")

        assert (
            str(notfound_error.value)
            == f"No products found at supplier {Supplier._supplier.name} for 'this_should_return_no_search_result"
        )
    except Exception as e:
        results = e

    # assert isinstance(results, Exception) is False, "query returned an exception"


@attributes(supplier="laboratoriumdiscounter", mock_data="query-9999-99-9")
def test_invalid_cas_query():
    results = None
    try:
        with pytest.raises(NoProductsFound) as notfound_error:
            results = Supplier("9999-99-9")

        assert str(notfound_error.value) == f"No products found at supplier {Supplier._supplier.name} for '9999-99-9'"
    except Exception as e:
        results = e


"""
# Base test class
@pytest.mark.supplier
class TestClass:
    _query = "Camphorsulfonyl"
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
    _query = "75-15-0"  # Carbon Disulfide
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

"""
