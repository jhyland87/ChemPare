"""Chemsavers supplier test module"""

# from unittest.mock import MagicMock
# from unittest.mock import patch

import pytest
from pytest_attributes import attributes

from chempare.datatypes import TypeProduct
from chempare.suppliers.supplier_chemsavers import SupplierChemsavers as Supplier


# from tests.mock_data.supplier_chemsavers.chemsavers_mocker import curl_cffi as mock_curl_cffi


# curl_cffi_post = MagicMock(wraps=mock_curl_cffi.post)

#
# Base test class


@attributes(supplier="supplier_chemsavers", mock_data="query-water")
def test_name_query():
    try:
        results = Supplier("water")
    except Exception as e:
        results = e

    assert isinstance(results, Exception) is False, "query returned an exception"


@attributes(supplier="supplier_chemsavers", mock_data="query-cas-7664-93-9")
def test_cas_query():
    try:
        results = Supplier("7664-93-9")
    except Exception as e:
        results = e

    assert isinstance(results, Exception) is False, "query returned an exception"


@attributes(supplier="supplier_chemsavers", mock_data="query-nonsense")
def test_nonsense_query():
    try:
        results = Supplier("this_should_return_no_search_result")
    except Exception as e:
        results = e

    assert isinstance(results, Exception) is False, "query returned an exception"


@attributes(supplier="supplier_chemsavers", mock_data="query-cas-9999-99-99")
def test_invalid_cas_query():
    try:
        results = Supplier("9999-99-99")
    except Exception as e:
        results = e

    assert isinstance(results, Exception) is False, "query returned an exception"


# class TestClass:
#     _query = "water"
#     _results = None

#     @classmethod
#     def setup_class(cls):
#         """setup any state specific to the execution of the given class (which
#         usually contains tests).
#         """
#         print("[TestClass] This is a setup!")

#     @pytest.fixture
#     def results(self):
#         if not self._results:
#             try:
#                 self._results = Supplier(self._query)
#             except Exception as e:
#                 self._results = e

#         return self._results


# # Test cases for a valid search for this supplier


# # @pytest.mark.usefixtures('setup_mock_curl_cffi')


# # @pytest.mark.usefixtures('setup_mock_curl_cffi')


# class TestValidSearch(TestClass):
#     _results = None

#     @classmethod
#     def setup_class(cls):
#         """setup any state specific to the execution of the given class (which
#         usually contains tests).
#         """
#         print("[TestValidSearch] This is a setup!")

#     @classmethod
#     def teardown_class(cls):
#         """setup any state specific to the execution of the given class (which
#         usually contains tests).
#         """
#         print("[TestValidSearch] teardown_class!")

#     # @attributes(supplier="chemsavers", response="test_valid_search")
#     @attributes(supplier="chemsavers", response="test_valid_search")
#     def test_query(self, results):
#         assert isinstance(results, Exception) is False
#         assert hasattr(results, "__iter__") is True
#         assert hasattr(results, "products") is True
#         assert isinstance(results.products, list) is True, "Return data is not instance of TypeProduct"

#     def test_results(self, results):
#         assert len(results) > 0, "No product results found"
#         assert isinstance(results.products[0], TypeProduct) is True


# # Test cases for invalid searches for this supplier


# # @pytest.mark.usefixtures('setup_mock_curl_cffi')
# @attributes(supplier="chemsavers", response="test_invalid_search")
# class TestInvalidSearch(TestClass):
#     _query = "This_should_return_no_results"
#     _results = None

#     # @pytest.mark.usefixtures('setup_mock_curl_cffi')
#     # @attributes(supplier="chemsavers", response="test_invalid_search")
#     # @pytest.mark.usefixtures('setup_mock_curl_cffi')
#     @attributes(supplier="chemsavers", response="test_invalid_search")
#     def test_query(self, results):
#         assert isinstance(results, Exception) is False
#         assert hasattr(results, "__iter__") is True
#         assert hasattr(results, "products") is True
#         assert isinstance(results.products, list) is True, "Return data is not instance of TypeProduct"

#     def test_results(self, results):
#         assert len(results) == 0


# # Test cases for a valid CAS search for this supplier
# # @pytest.mark.usefixtures('setup_mock_curl_cffi')
# class TestValidCASSearch(TestClass):
#     _query = "7664-93-9"
#     _results = None

#     # @attributes(supplier="chemsavers", response="test_valid_cas_search")
#     # @pytest.mark.usefixtures('setup_mock_curl_cffi')
#     @attributes(supplier="chemsavers", response="test_valid_cas_search")
#     def test_query(self, results):
#         assert isinstance(results, Exception) is False
#         assert hasattr(results, "__iter__") is True
#         assert hasattr(results, "products") is True
#         assert isinstance(results.products, list) is True, "Return data is not instance of TypeProduct"

#     # @pytest.mark.usefixtures('setup_mock_curl_cffi')
#     # @attributes(supplier="chemsavers", response="this_should_not_fire")
#     def test_results(self, results):
#         assert len(results) > 0, "No product results found"
#         assert isinstance(results.products[0], TypeProduct) is True
