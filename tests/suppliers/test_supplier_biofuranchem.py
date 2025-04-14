"""Chemsavers supplier test module"""

# from unittest.mock import MagicMock
# from unittest.mock import patch

import pytest
from pytest_attributes import attributes

from chempare.datatypes import TypeProduct
from chempare.suppliers.supplier_biofuranchem import SupplierBioFuranChem as Supplier


# from tests.mock_data.supplier_chemsavers.chemsavers_mocker import curl_cffi as mock_curl_cffi


# curl_cffi_post = MagicMock(wraps=mock_curl_cffi.post)

#
# Base test class


@attributes(supplier="biofuranchem", json_content="query_water")
def test_name_query():
    try:
        results = Supplier("water")
    except Exception as e:
        results = e

    assert isinstance(results, Exception) is False, "query returned an exception"


@attributes(supplier="biofuranchem", json_content="query_5949_29_1")
def test_cas_query():
    try:
        results = Supplier("5949-29-1")
    except Exception as e:
        results = e

    assert isinstance(results, Exception) is False, "query returned an exception"


@attributes(supplier="biofuranchem", json_content="query_nonsense")
def test_nonsense_query():
    try:
        results = Supplier("this_should_return_no_search_result")
    except Exception as e:
        results = e

    assert isinstance(results, Exception) is False, "query returned an exception"


@attributes(supplier="biofuranchem", json_content="query_9999_99_99")
def test_invalid_cas_query():
    try:
        results = Supplier("9999-99-99")
    except Exception as e:
        results = e

    assert isinstance(results, Exception) is False, "query returned an exception"
