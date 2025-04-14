"""Chemsavers supplier test module"""

# from unittest.mock import MagicMock
# from unittest.mock import patch

import pytest
from pytest_attributes import attributes

from chempare.datatypes import TypeProduct
from chempare.suppliers.supplier_laballey import SupplierLaballey as Supplier


# from tests.mock_data.supplier_chemsavers.chemsavers_mocker import curl_cffi as mock_curl_cffi


# curl_cffi_post = MagicMock(wraps=mock_curl_cffi.post)

#
# Base test class


@attributes(supplier="laballey", json_content="query_acid")
def test_name_query():
    try:
        results = Supplier("acid")
    except Exception as e:
        results = e

    assert isinstance(results, Exception) is False, "query returned an exception"


@attributes(supplier="laballey", json_content="query_cas_sulfuric_acid")
def test_cas_query():
    try:
        results = Supplier("7664-93-9")
    except Exception as e:
        results = e

    assert isinstance(results, Exception) is False, "query returned an exception"


@attributes(supplier="laballey", json_content="query_nonsense")
def test_nonsense_query():
    try:
        results = Supplier("this_should_return_no_search_result")
    except Exception as e:
        results = e

    assert isinstance(results, Exception) is False, "query returned an exception"


@attributes(supplier="laballey", json_content="query_cas_9999_99_99")
def test_invalid_cas_query():
    try:
        results = Supplier("9999-99-99")
    except Exception as e:
        results = e

    assert isinstance(results, Exception) is False, "query returned an exception"
