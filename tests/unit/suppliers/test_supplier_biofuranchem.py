"""Biofuran Chem supplier test module"""

from typing import Iterable

import pytest
from pytest_attributes import attributes

from chempare.datatypes import ProductType
from chempare.exceptions import NoProductsFoundError
from chempare.suppliers.supplier_biofuranchem import SupplierBioFuranChem as Supplier


# def test_some_bullshit():
#     assert 1 == 1


@attributes(supplier="supplier_biofuranchem", mock_data="query-water")
def test_name_query():
    results = Supplier("water")

    assert isinstance(results, Iterable) is True, "Expected an iterable result from supplier query"
    assert len(results) > 0, "No product results found"
    # assert isinstance(results[0], ProductType) is True, "Items in resulting array are not ProductTypes"
    assert (
        any(not isinstance(product, ProductType) for product in results) is False
    ), "Items in resulting array are not ProductTypes"

    assert (
        any(not hasattr(product, "supplier") for product in results) is False
    ), "Found items with no supplier attribute"

    assert any(not hasattr(product, "url") for product in results) is False, "Found items with no url attribute"

    assert any(not hasattr(product, "title") for product in results) is False, "Found items with no title attribute"

    assert any(not hasattr(product, "price") for product in results) is False, "Found items with no price attribute"

    assert (
        any(not hasattr(product, "currency") for product in results) is False
    ), "Found items with no currency attribute"

    assert (
        any(not hasattr(product, "currency_code") for product in results) is False
    ), "Found items with no currency code attribute"

    assert (
        any(not hasattr(product, "quantity") for product in results) is False
    ), "Found items with no quantity attribute"

    assert (
        any(not hasattr(product, "uom") for product in results) is False
    ), "Found items with no uom (unit of measurement) attribute"


@attributes(supplier="supplier_biofuranchem", mock_data="query-5949-29-1")
def test_cas_query():
    results = Supplier("5949-29-1")

    assert isinstance(results, Iterable) is True, "Expected an iterable result from supplier query"
    assert len(results) > 0, "No product results found"
    assert isinstance(results[0], ProductType) is True


@attributes(supplier="supplier_biofuranchem", mock_data="query-nonsense")
def test_nonsense_query():
    results = None
    with pytest.raises(NoProductsFoundError) as no_products_found:
        results = Supplier("this_should_return_no_search_result")

    assert no_products_found.errisinstance(NoProductsFoundError) is True, "Expected a NoProductsFoundError error"
    assert results is None, "Results found for nonsense query"


@attributes(supplier="supplier_biofuranchem", mock_data="query-9999-99-9")
def test_invalid_cas_query():
    results = None
    with pytest.raises(NoProductsFoundError) as no_products_found:
        results = Supplier("9999-99-9")

    assert no_products_found.errisinstance(NoProductsFoundError) is True, "Expected a NoProductsFoundError error"
    assert results is None, "Results found for bad CAS query"
