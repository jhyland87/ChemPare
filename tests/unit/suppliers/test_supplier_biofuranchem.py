"""Biofuran Chem supplier test module"""

from typing import Iterable

import pytest
from pytest_attributes import attributes

from chempare.datatypes import TypeProduct
from chempare.exceptions import NoProductsFound

# from chempare.datatypes import TypeProduct
from chempare.suppliers.supplier_biofuranchem import SupplierBioFuranChem as Supplier


# from unittest.mock import MagicMock
# from unittest.mock import patch


# from tests.mock_data.supplier_chemsavers.chemsavers_mocker import curl_cffi as mock_curl_cffi


# curl_cffi_post = MagicMock(wraps=mock_curl_cffi.post)

#
# Base test class


@attributes(supplier="supplier_biofuranchem", mock_data="query-water")
def test_name_query():
    results = Supplier("water")

    assert isinstance(results, Iterable) is True, "Expected an iterable result from supplier query"
    assert len(results) > 0, "No product results found"
    assert isinstance(results[0], TypeProduct) is True


@attributes(supplier="supplier_biofuranchem", mock_data="query-5949-29-1")
def test_cas_query():
    results = Supplier("5949-29-1")

    assert isinstance(results, Iterable) is True, "Expected an iterable result from supplier query"
    assert len(results) > 0, "No product results found"
    assert isinstance(results[0], TypeProduct) is True


@attributes(supplier="supplier_biofuranchem", mock_data="query-nonsense")
def test_nonsense_query():
    results = None
    with pytest.raises(NoProductsFound) as no_products_found:
        results = Supplier("this_should_return_no_search_result")

    assert no_products_found.errisinstance(NoProductsFound) is True, "Expected a NoProductsFound error"
    assert results is None, "Results found for nonsense query"


@attributes(supplier="supplier_biofuranchem", mock_data="query-9999-99-9")
def test_invalid_cas_query():
    results = None
    with pytest.raises(NoProductsFound) as no_products_found:
        results = Supplier("9999-99-9")

    assert no_products_found.errisinstance(NoProductsFound) is True, "Expected a NoProductsFound error"
    assert results is None, "Results found for bad CAS query"
