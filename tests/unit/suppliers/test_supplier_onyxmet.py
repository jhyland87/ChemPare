"""OnyxMet supplier test module"""

from typing import Iterable

import pytest
from pytest_attributes import attributes

from chempare.datatypes import ProductType
from chempare.exceptions import NoProductsFoundError
from chempare.suppliers.supplier_onyxmet import SupplierOnyxmet as Supplier


@attributes(supplier="supplier_onyxmet", mock_data="query-rhodium")
def test_name_query():
    results = Supplier("rhodium")

    assert isinstance(results, Iterable) is True, "Expected an iterable result from supplier query"
    assert len(results) > 0, "No product results found"
    assert isinstance(results[0], ProductType) is True


@attributes(supplier="supplier_onyxmet", mock_data="query-nonsense")
def test_nonsense_query():
    results = None
    with pytest.raises(NoProductsFoundError) as no_products_found:
        results = Supplier("this_should_return_no_search_result")

    assert no_products_found.errisinstance(NoProductsFoundError) is True, "Expected a NoProductsFoundError error"
    assert results is None, "Results found for nonsense query"


# import pytest

# from chempare.datatypes import ProductType
# from chempare.suppliers import SupplierOnyxmet as Supplier


# # Base test class
# @pytest.mark.supplier
# class TestClass:
#     _query = "carbonate"
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
#         ), "Return data is not instance of ProductType"

#     def test_results(self, results):
#         assert len(results) > 0, "No product results found"
#         assert isinstance(results.products[0], ProductType) is True


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
#         ), "Return data is not instance of ProductType"

#     def test_results(self, results):
#         assert len(results) == 0


# # Test cases for a valid CAS search for this supplier
# class TestValidCASSearch(TestClass):
#     _query = "7440-23-5"  # Sodium
#     _results = None

#     def test_query(self, results):
#         assert isinstance(results, Exception) is False
#         assert hasattr(results, "__iter__") is True
#         assert hasattr(results, "products") is True
#         assert (
#             isinstance(results.products, list) is True
#         ), "Return data is not instance of ProductType"

#     def test_results(self, results):
#         assert len(results) > 0, "No product results found"
#         assert isinstance(results.products[0], ProductType) is True


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
#         ), "Return data is not instance of ProductType"

#     def test_results(self, results):
#         assert len(results) == 0
