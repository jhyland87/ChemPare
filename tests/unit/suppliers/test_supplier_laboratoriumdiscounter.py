from typing import Iterable

import pytest
from pytest_attributes import attributes

from chempare.datatypes import ProductType
from chempare.suppliers.supplier_base import NoProductsFoundError
from chempare.suppliers.supplier_laboratoriumdiscounter import SupplierLaboratoriumDiscounter as Supplier


@attributes(supplier="supplier_laboratoriumdiscounter", mock_data="query-acid")
def test_name_query():
    results = Supplier("acid")

    assert isinstance(results, Iterable) is True, "Expected an iterable result from supplier query"
    assert len(results) > 0, "No product results found"
    assert isinstance(results[0], ProductType) is True


@attributes(supplier="supplier_laboratoriumdiscounter", mock_data="query-7664-93-9")
def test_cas_query():
    results = Supplier("7664-93-9")

    assert isinstance(results, Iterable) is True, "Expected an iterable result from supplier query"
    assert len(results) > 0, "No product results found"
    assert isinstance(results[0], ProductType) is True


@attributes(supplier="supplier_laboratoriumdiscounter", mock_data="query-nonsense")
def test_nonsense_query():
    results = None
    with pytest.raises(NoProductsFoundError) as notfound_error:
        results = Supplier("this_should_return_no_search_result")

    assert (
        notfound_error.errisinstance(NoProductsFoundError) is True
    ), "Did not trigger expected NoProductsFoundError error"
    assert results is None, "Unexpected products found"
    assert (
        str(notfound_error.value)
        == f"No products found at supplier {Supplier._supplier.name} for 'this_should_return_no_search_result'"
    )

    # assert isinstance(results, Exception) is False, "query returned an exception"


@attributes(supplier="supplier_laboratoriumdiscounter", mock_data="query-9999-99-9")
def test_invalid_cas_query():
    results = None
    with pytest.raises(NoProductsFoundError) as notfound_error:
        results = Supplier("9999-99-9")

    assert (
        notfound_error.errisinstance(NoProductsFoundError) is True
    ), "Did not counter expected NoProductsFoundError error"
    assert str(notfound_error.value) == f"No products found at supplier {Supplier._supplier.name} for '9999-99-9'"
    assert results is None, "Unexpected products returned"
