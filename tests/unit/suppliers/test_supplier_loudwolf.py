from typing import Iterable

import pytest
from pytest_attributes import attributes

from chempare.datatypes import ProductType
from chempare.exceptions import NoProductsFoundError
from chempare.suppliers.supplier_loudwolf import SupplierLoudwolf as Supplier


#
# Base test class


@attributes(supplier="supplier_loudwolf", mock_data="query-acid")
def test_name_query():
    results = Supplier("acid")

    assert isinstance(results, Iterable) is True, "Expected an iterable result from supplier query"
    assert len(results) > 0, "No product results found"
    assert isinstance(results[0], ProductType) is True


@attributes(supplier="supplier_loudwolf", mock_data="query-cas-532-32-1")
def test_cas_query():
    results = Supplier("532-32-1")

    assert isinstance(results, Iterable) is True, "Expected an iterable result from supplier query"
    assert len(results) > 0, "No product results found"
    assert isinstance(results[0], ProductType) is True


@attributes(supplier="supplier_loudwolf", mock_data="query-nonsense")
def test_nonsense_query():
    results = None
    with pytest.raises(NoProductsFoundError) as no_products_found:
        results = Supplier("this_should_return_no_search_result")

    assert no_products_found.errisinstance(NoProductsFoundError) is True, "Expected a NoProductsFoundError error"
    assert results is None, "Results found for bad CAS search"


@attributes(supplier="supplier_loudwolf", mock_data="query-cas-9999-99-9")
def test_invalid_cas_query():
    results = None
    with pytest.raises(NoProductsFoundError) as no_products_found:
        results = Supplier("9999-99-9")

    assert no_products_found.errisinstance(NoProductsFoundError) is True, "Expected a NoProductsFoundError error"
    assert results is None, "Results found for bad CAS search"
