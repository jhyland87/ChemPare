"""3S Chem supplier test module"""

# from unittest.mock import MagicMock
# from unittest.mock import patch

import pytest
from pytest_attributes import attributes

from chempare.exceptions import NoProductsFound

# from chempare.datatypes import TypeProduct
from chempare.suppliers.supplier_3schem import Supplier3SChem as Supplier


# from tests.mock_data.supplier_chemsavers.chemsavers_mocker import curl_cffi as mock_curl_cffi


# curl_cffi_post = MagicMock(wraps=mock_curl_cffi.post)

#
# Base test class


@attributes(supplier="supplier_3schem", mock_data="query-clean")
def test_name_query():
    results = Supplier("clean")
    print("results", results)
    assert isinstance(results, Exception) is False
    assert hasattr(results, "__iter__") is True
    assert hasattr(results, "products") is True
    assert isinstance(results.products, list) is True, "Return data is not instance of TypeProduct"


@attributes(supplier="supplier_3schem", mock_data="query-nonsense")
def test_nonsense_query():
    results = None
    with pytest.raises(NoProductsFound) as no_products_found:
        results = Supplier("this_should_return_no_search_result")

    assert no_products_found.errisinstance(NoProductsFound) is True, "Expected a NoProductsFound error"
    assert results is None, "Results found for nonsense query"
