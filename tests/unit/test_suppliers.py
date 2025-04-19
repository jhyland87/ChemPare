"""Biofuran Chem supplier test module"""

from dataclasses import dataclass
from typing import Iterable
from typing import override

import pytest
from pytest_attributes import attributes

from chempare.datatypes import ProductType
from chempare.exceptions import NoProductsFoundError
from chempare.suppliers.supplier_biofuranchem import SupplierBioFuranChem
from chempare.suppliers.supplier_chemsavers import SupplierChemsavers
from chempare.suppliers.supplier_ftfscientific import SupplierFtfScientific


# def test_some_bullshit():
#     assert 1 == 1


# @dataclass
class BaseTestClass:
    results = None

    # @classmethod
    # def setup_class(cls):
    #     cls.results = SupplierBioFuranChem("water")

    def test_result_type(self):
        assert isinstance(self.results, Iterable) is True, "Expected an iterable result from supplier query"

        assert all(
            isinstance(product, ProductType) for product in self.results  # type: ignore
        ), "Items in resulting array are not ProductTypes"

        assert len(self.results) > 0, "No product results found"  # type: ignore

    # @classmethod
    # def teardown_class(cls):
    #     print("Tearing down class")

    # def setup_method(self, method):
    #     print(f"Setting up method: {method.__name__}")

    # def teardown_method(self, method):
    #     print(f"Tearing down method: {method.__name__}")

    @pytest.mark.parametrize(
        ("attribute"),
        [("supplier"), ("url"), ("title"), ("price"), ("currency"), ("currency_code"), ("quantity"), ("uom")],
        ids=[
            "supplier attribute check",
            "url attribute check",
            "title attribute check",
            "price attribute check",
            "currency attribute check",
            "currency_code attribute check",
            "quantity attribute check",
            "uom attribute check",
        ],
    )
    def test_product_attributes(self, attribute):
        assert all(
            hasattr(product, attribute) for product in self.results
        ), f"Found items with no {attribute} attribute"

        assert all(
            getattr(product, attribute) not in [None, "None", ""] for product in self.results
        ), f"Found items with empty/invalid {attribute} attribute"


class TestSupplierBioFuranChem(BaseTestClass):
    results = None

    # @override
    @classmethod
    def setup_class(cls):
        cls.results = SupplierBioFuranChem("water")


class TestSupplierFtfScientific(BaseTestClass):
    results = None

    # @override
    @classmethod
    def setup_class(cls):
        cls.results = SupplierFtfScientific("water")


class TestSupplierChemsavers(BaseTestClass):
    results = None

    # @override
    @classmethod
    def setup_class(cls):
        cls.results = SupplierChemsavers("water")


# @attributes(supplier="supplier_biofuranchem", mock_data="query-water")
# def test_name_query():
#     results = Supplier("water")

#     assert isinstance(results, Iterable) is True, "Expected an iterable result from supplier query"

#     assert len(results) > 0, "No product results found"
#     # assert isinstance(results[0], ProductType) is True, "Items in resulting array are not ProductTypes"

#     assert all(isinstance(product, ProductType) for product in results), "Items in resulting array are not ProductTypes"
#     assert all(not hasattr(product, "supplier") for product in results), "Found items with no supplier attribute"
#     assert all(not hasattr(product, "url") for product in results), "Found items with no url attribute"
#     assert all(not hasattr(product, "title") for product in results), "Found items with no title attribute"
#     assert all(not hasattr(product, "price") for product in results), "Found items with no price attribute"
#     assert all(not hasattr(product, "currency") for product in results), "Found items with no currency attribute"
#     assert all(not hasattr(product, "currency_code") for product in results), "Found items with no currency code"
#     assert all(not hasattr(product, "quantity") for product in results), "Found items with no quantity attribute"
#     assert all(not hasattr(product, "uom") for product in results), "Found items with no unit of measurement attribute"


"""
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
"""
