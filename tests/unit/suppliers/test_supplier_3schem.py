"""3S Chem supplier test module"""

from typing import Iterable

import pytest
from pytest_attributes import attributes

from chempare.datatypes import ProductType
from chempare.exceptions import NoProductsFoundError

# from chempare.datatypes import ProductType
from chempare.suppliers.supplier_3schem import Supplier3SChem as Supplier


@attributes(supplier="supplier_3schem", mock_data="query-clean")
def test_name_query():
    results = Supplier("clean")

    assert isinstance(results, Iterable) is True, "Expected an iterable result from supplier query"
    assert len(results) > 0, "No product results found"
    assert isinstance(results[0], ProductType) is True


@attributes(supplier="supplier_3schem", mock_data="query-nonsense")
def test_nonsense_query():
    results = None
    with pytest.raises(NoProductsFoundError) as no_products_found:
        results = Supplier("this_should_return_no_search_result")

    assert no_products_found.errisinstance(NoProductsFoundError) is True, "Expected a NoProductsFoundError error"
    assert results is None, "Results found for nonsense query"
