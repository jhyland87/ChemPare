from collections.abc import Iterable

import pytest
from pytest_attributes import attributes

from chempare.datatypes import TypeProduct
from chempare.exceptions import NoProductsFound
from chempare.suppliers.supplier_ftfscientific import SupplierFtfScientific as Supplier


@attributes(supplier="supplier_ftfscientific", mock_data="query-water")
def test_name_query():
    results = Supplier("water")

    assert isinstance(results, Iterable) is True, "Expected an iterable result from supplier query"
    assert len(results) > 0, "No product results found"
    assert isinstance(results[0], TypeProduct) is True


@attributes(supplier="supplier_ftfscientific", mock_data="query-cas-95-50-1")
def test_cas_query():
    results = Supplier("95-50-1")

    assert isinstance(results, Iterable) is True, "Expected an iterable result from supplier query"
    assert len(results) > 0, "No product results found"
    assert isinstance(results[0], TypeProduct) is True


@attributes(supplier="supplier_ftfscientific", mock_data="query-nonsense")
def test_nonsense_query():
    results = None
    with pytest.raises(NoProductsFound) as no_products_found:
        results = Supplier("This_should_return_no_results")

    assert no_products_found.errisinstance(NoProductsFound) is True, "Expected a NoProductsFound error"
    assert results is None, "Results found for nonsense query"


@attributes(supplier="supplier_ftfscientific", mock_data="query-cas-7782-77-6")
def test_invalid_cas_query():
    results = None
    with pytest.raises(NoProductsFound) as no_products_found:
        results = Supplier("7782-77-6")

    assert no_products_found.errisinstance(NoProductsFound) is True, "Expected a NoProductsFound error"
    assert results is None, "Results found for nonsense query"
