"""Biofuran Chem supplier test module"""

from dataclasses import dataclass
from typing import Iterable
from typing import override

import pytest
import requests
from pytest import MonkeyPatch
from pytest_attributes import attributes

import chempare.suppliers
from chempare.datatypes import ProductType
from chempare.exceptions import NoProductsFoundError
from chempare.search_factory import SearchFactory
from tests import mock_request_cache


monkeypatch = MonkeyPatch()


# pylint: disable=missing-class-docstring


# @dataclass
class BaseTestClass:
    results = {}
    supplier = None
    positive_query = None
    negative_query = None
    supplier_class = None
    query_limit = 5

    @classmethod
    def setup_class(cls):
        monkeypatch.setenv("TEST_MONKEYPATCHING", "true")
        monkeypatch.setenv("CALLED_FROM_TEST", "true")

        mock_request_cache.requests = mock_request_cache.set_supplier_cache_session(str(cls.supplier))

        monkeypatch.setattr(requests, "get", mock_request_cache.requests.get)
        monkeypatch.setattr(requests, "post", mock_request_cache.requests.post)
        monkeypatch.setattr(requests, "head", mock_request_cache.requests.head)
        monkeypatch.setattr(requests, "request", mock_request_cache.requests.request)

        supplier_module = getattr(chempare.suppliers, str(cls.supplier_class))
        cls.results["positive_query"] = supplier_module(cls.positive_query, cls.query_limit)

        with pytest.raises(NoProductsFoundError) as no_products_found:
            cls.results["negative_query"] = supplier_module(cls.negative_query, cls.query_limit)
        cls.results["negative_query"] = no_products_found

    @classmethod
    def teardown_class(cls):
        monkeypatch.undo()
        cls.results = {}
        cls.supplier = None
        cls.positive_query = None
        cls.negative_query = None
        cls.supplier_class = None
        cls.query_limit = 5

    def test_result_type(self):
        assert (
            isinstance(self.results["positive_query"], Iterable) is True
        ), "Expected an iterable result from supplier query"

        assert all(
            isinstance(product, ProductType) for product in self.results["positive_query"]
        ), "Items in resulting array are not ProductTypes"

        assert len(self.results["positive_query"]) > 0, "No product results found"

    # def setup_method(self, method):
    #     print(f"Setting up method: {method.__name__}")

    # def teardown_method(self, method):
    #     print(f"Tearing down method: {method.__name__}")

    @pytest.mark.parametrize(
        ("attribute"),
        [("supplier"), ("url"), ("title"), ("price"), ("currency"), ("currency_code"), ("quantity"), ("uom")],
        ids=[
            "'supplier' attribute check",
            "'url' attribute check",
            "'title' attribute check",
            "'price' attribute check",
            "'currency' attribute check",
            "'currency_code' attribute check",
            "'quantity' attribute check",
            "'uom' attribute check",
        ],
    )
    def test_product_attributes(self, attribute):
        assert all(
            hasattr(product, attribute) for product in self.results["positive_query"]
        ), f"Found items with no {attribute} attribute"

        assert all(
            getattr(product, attribute) not in [None, "None", ""] for product in self.results["positive_query"]
        ), f"Found items with empty/invalid {attribute} attribute"

    def test_nonsense_query_results(self):
        assert (
            self.results["negative_query"].errisinstance(NoProductsFoundError) is True
        ), "Expected a NoProductsFoundError error"


class TestSupplierBioFuranChem(BaseTestClass):
    results = {}
    supplier_class = "SupplierBioFuranChem"
    supplier = "supplier_biofuranchem"
    positive_query = "water"
    negative_query = "this_should_not_exist"


class TestSupplierFtfScientific(BaseTestClass):
    results = {}
    supplier = "supplier_ftfscientific"
    supplier_class = "SupplierFtfScientific"
    positive_query = "acid"
    negative_query = "this_should_not_exist"


class TestSupplierChemsavers(BaseTestClass):
    results = {}
    supplier = "supplier_chemsavers"
    supplier_class = "SupplierChemsavers"
    positive_query = "water"
    negative_query = "this_should_not_exist"


class TestSupplier3SChem(BaseTestClass):
    results = {}
    supplier = "supplier_3SChem"
    supplier_class = "Supplier3SChem"
    positive_query = "clean"
    negative_query = "this_should_not_exist"


class TestSupplierEsDrei(BaseTestClass):
    results = {}
    supplier = "supplier_esdrei"
    supplier_class = "SupplierEsDrei"
    positive_query = "Wasser"
    negative_query = "this_should_not_exist"


class TestSupplierLaballey(BaseTestClass):
    results = {}
    supplier = "supplier_laballey"
    supplier_class = "SupplierLaballey"
    positive_query = "acid"
    negative_query = "this_should_not_exist"


class TestSupplierLabchem(BaseTestClass):
    results = {}
    supplier = "supplier_lachem"
    supplier_class = "SupplierLabchem"
    positive_query = "acid"
    negative_query = "this_should_not_exist"


class TestSupplierLaboratoriumDiscounter(BaseTestClass):
    results = {}
    supplier = "supplier_laboratoriumdiscounter"
    supplier_class = "SupplierLaboratoriumDiscounter"
    positive_query = "acid"
    negative_query = "this_should_not_exist"


class TestSupplierLoudwolf(BaseTestClass):
    results = {}
    supplier = "supplier_loudwolf"
    supplier_class = "SupplierLoudwolf"
    positive_query = "acid"
    negative_query = "this_should_not_exist"


class TestSupplierOnyxmet(BaseTestClass):
    results = {}
    supplier = "supplier_onyxmet"
    supplier_class = "SupplierOnyxmet"
    positive_query = "rhodium"
    negative_query = "this_should_not_exist"


class TestSupplierSynthetika(BaseTestClass):
    results = {}
    supplier = "supplier_synthetika"
    supplier_class = "SupplierSynthetika"
    positive_query = "Tartaric Acid"
    negative_query = "this_should_not_exist"


class TestSupplierTciChemicals(BaseTestClass):
    results = {}
    supplier = "supplier_tcichemicals"
    supplier_class = "SupplierTciChemicals"
    positive_query = "acetamide"
    negative_query = "this_should_not_exist"


class TestSupplierWarchem(BaseTestClass):
    results = {}
    supplier = "supplier_warchem"
    supplier_class = "SupplierWarchem"
    positive_query = "WODA"
    negative_query = "this_should_not_exist"
