import pytest
from pytest_attributes import attributes

from chempare.datatypes import TypeProduct
from chempare.exceptions import NoProductsFound
from chempare.suppliers.supplier_loudwolf import SupplierLoudwolf as Supplier


#
# Base test class


@attributes(supplier="supplier_loudwolf", mock_data="query-acid")
def test_name_query():
    try:
        results = Supplier("acid")
    except Exception as e:
        results = e

    assert isinstance(results, Exception) is False, "query returned an exception"
    assert isinstance(results, Supplier) is True, "Improper object type returned"
    assert hasattr(results, 'products') is True, "No products attribute in results"
    assert isinstance(results.products, list) is True, "Non-list type returned"
    assert len(results.products) > 0, "Empty results list returned"
    assert isinstance(results.products[0], TypeProduct) is True, "First product is not of type TypeProduct"


@attributes(supplier="supplier_loudwolf", mock_data="query-cas-532-32-1")
def test_cas_query():
    try:
        results = Supplier("532-32-1")
    except Exception as e:
        results = e

    assert isinstance(results, Exception) is False, "query returned an exception"


@attributes(supplier="supplier_loudwolf", mock_data="query-nonsense")
def test_nonsense_query():
    results = None
    with pytest.raises(NoProductsFound) as no_products_found:
        results = Supplier("this_should_return_no_search_result")

    assert no_products_found.errisinstance(NoProductsFound) is True, "Expected a NoProductsFound error"
    assert results is None, "Results found for bad CAS search"


@attributes(supplier="supplier_loudwolf", mock_data="query-cas-9999-99-9")
def test_invalid_cas_query():
    results = None
    with pytest.raises(NoProductsFound) as no_products_found:
        results = Supplier("9999-99-9")

    assert no_products_found.errisinstance(NoProductsFound) is True, "Expected a NoProductsFound error"
    assert results is None, "Results found for bad CAS search"


# # Base test class
# @pytest.mark.supplier
# class TestClass:
#     _query = "water"
#     _results = None

#     @pytest.fixture
#     def results(self):
#         if not self._results:
#             try:
#                 self._results = Supplier(self._query)
#             except Exception as e:
#                 self._results = e

#         return self._results


# # Test cases for a valid search for this supplier
# class TestValidSearch(TestClass):
#     _results = None

#     def test_query(self, results):
#         assert isinstance(results, Exception) is False
#         assert hasattr(results, "__iter__") is True
#         assert hasattr(results, "products") is True
#         assert (
#             isinstance(results.products, list) is True
#         ), "Return data is not instance of TypeProduct"

#     def test_results(self, results):
#         assert len(results) > 0, "No product results found"
#         assert isinstance(results.products[0], TypeProduct) is True


# # Test cases for invalid searches for this supplier
# class TestInvalidSearch(TestClass):
#     _query = "This_should_return_no_results"
#     _results = None

#     def test_query(self, results):
#         assert isinstance(results, Exception) is False
#         assert hasattr(results, "__iter__") is True
#         assert hasattr(results, "products") is True
#         assert (
#             isinstance(results.products, list) is True
#         ), "Return data is not instance of TypeProduct"

#     def test_results(self, results):
#         assert len(results) == 0


# # Test cases for a valid CAS search for this supplier
# class TestValidCASSearch(TestClass):
#     _query = "7440-44-0"  # Activated carbon
#     _results = None

#     def test_query(self, results):
#         assert isinstance(results, Exception) is False
#         assert hasattr(results, "__iter__") is True
#         assert hasattr(results, "products") is True
#         assert (
#             isinstance(results.products, list) is True
#         ), "Return data is not instance of TypeProduct"

#     def test_results(self, results):
#         assert len(results) > 0, "No product results found"
#         assert isinstance(results.products[0], TypeProduct) is True


# # Test cases for an invalid CAS search for this supplier
# class TestInvalidCASSearch(TestClass):
#     _query = "7782-77-6"  # Nitrous acid, too stable to be sold
#     _results = None

#     def test_query(self, results):
#         assert isinstance(results, Exception) is False
#         assert hasattr(results, "__iter__") is True
#         assert hasattr(results, "products") is True
#         assert (
#             isinstance(results.products, list) is True
#         ), "Return data is not instance of TypeProduct"

#     def test_results(self, results):
#         assert len(results) == 0
