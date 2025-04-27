"""Biofuran Chem supplier test module"""
from __future__ import annotations

from collections.abc import Iterable

from requests import get

import chempare.suppliers
import pytest
import requests
import requests_cache
from chempare.exceptions import NoProductsFoundError
from chempare.search_factory import SearchFactory
from pytest import MonkeyPatch
from requests_cache import CacheDirectives

from tests import mock_request_cache


monkeypatch = MonkeyPatch()


# pylint: disable=missing-class-docstring

import requests_cache
from requests_cache import CacheDirectives


# Hack to work around requests_cache not paying attention to the cache_control setting.
def clear_no_cache(func):
    def wrapper(cls, headers):
        if "Cache-Control" in headers:
            headers["Cache-Control"] = False
        result = func(headers)
        return result

    return wrapper


original_method = requests_cache.CacheDirectives.from_headers
decorated_method = clear_no_cache(original_method)


# @dataclass
class BaseTestClass:
    results = {}
    supplier = None
    positive_query = None
    negative_query = None
    query_limit = 5

    @classmethod
    def setup_class(cls):
        if cls.supplier != 'search_factory':
            if not (mod := getattr(chempare.suppliers, str(cls.supplier), None)):
                raise ImportError(f"Supplier module {cls.supplier} not found")

            if getattr(mod, "__disabled__", False) is True:
                pytest.skip(reason="Supplier module is disabled")

        monkeypatch.setenv("TEST_MONKEYPATCHING", "true")
        monkeypatch.setenv("CALLED_FROM_TEST", "true")

        # Strip the cache-control from any headers
        monkeypatch.setattr(CacheDirectives, "from_headers", classmethod(decorated_method))

        mock_request_cache.requests = mock_request_cache.set_supplier_cache_session(str(cls.supplier))
        if cls.supplier == 'search_factory':
            setattr(chempare.suppliers, 'SearchFactory', SearchFactory)

        monkeypatch.setattr(requests, "get", mock_request_cache.requests.get)  # type: ignore
        monkeypatch.setattr(requests, "post", mock_request_cache.requests.post)  # type: ignore
        monkeypatch.setattr(requests, "head", mock_request_cache.requests.head)  # type: ignore
        monkeypatch.setattr(requests, "request", mock_request_cache.requests.request)  # type: ignore

        # Get the supplier class name from the executing test class (eg: TestSupplierFoo would be SupplierFoo)
        supplier_class = cls.__name__.replace('Test', '', 1)

        supplier_module = getattr(chempare.suppliers, supplier_class)
        cls.results["positive_query"] = supplier_module(cls.positive_query, cls.query_limit)

        with pytest.raises(NoProductsFoundError) as no_products_found:
            supplier_module(cls.negative_query, cls.query_limit)
        cls.results["negative_query"] = no_products_found

    @classmethod
    def teardown_class(cls):
        monkeypatch.undo()
        cls.results = {}
        cls.supplier = None
        cls.positive_query = None
        cls.negative_query = None
        cls.query_limit = 5

    def test_result_type(self):
        assert (
            isinstance(self.results["positive_query"], Iterable) is True
        ), "Expected an iterable result from supplier query"

        assert len(self.results["positive_query"]) > 0, "No product results found"

    @pytest.mark.parametrize(
        ("attribute"),
        [("supplier"), ("url"), ("title"), ("price"), ("currency"), ("quantity"), ("uom")],
        ids=[
            "'supplier' attribute check",
            "'url' attribute check",
            "'title' attribute check",
            "'price' attribute check",
            "'currency' attribute check",
            "'quantity' attribute check",
            "'uom' attribute check",
        ],
    )
    def test_product_attributes(self, attribute):
        assert all(
            attribute in product for product in self.results["positive_query"]
        ), f"Found items with no {attribute} attribute"

        assert all(
            product.get(attribute) not in [None, "None", ""] for product in self.results["positive_query"]
        ), f"Found items with empty/invalid {attribute} attribute"

    def test_nonsense_query_results(self):
        assert (
            self.results["negative_query"].errisinstance(NoProductsFoundError) is True
        ), "Expected a NoProductsFoundError error"
        assert "ExceptionInfo NoProductsFoundError" in self.results["negative_query"].__str__()


class TestSupplierBioFuranChem(BaseTestClass):
    results = {}
    supplier = "supplier_biofuranchem"
    positive_query = "acid"
    negative_query = "this_should_not_exist"


class TestSupplierFtfScientific(BaseTestClass):
    results = {}
    supplier = "supplier_ftfscientific"
    positive_query = "acid"
    negative_query = "this_should_not_exist"


class TestSupplierChemsavers(BaseTestClass):
    results = {}
    supplier = "supplier_chemsavers"
    positive_query = "acid"
    negative_query = "this_should_not_exist"


class TestSupplier3SChem(BaseTestClass):
    results = {}
    supplier = "supplier_3schem"
    positive_query = "clean"
    negative_query = "this_should_not_exist"


class TestSupplierEsDrei(BaseTestClass):
    results = {}
    supplier = "supplier_esdrei"
    positive_query = "Wasser"
    negative_query = "this_should_not_exist"


class TestSupplierLaballey(BaseTestClass):
    results = {}
    supplier = "supplier_laballey"
    positive_query = "acid"
    negative_query = "this_should_not_exist"

class TestSupplierLaboratoriumDiscounter(BaseTestClass):
    results = {}
    supplier = "supplier_laboratoriumdiscounter"
    positive_query = "acid"
    negative_query = "this_should_not_exist"


class TestSupplierLoudwolf(BaseTestClass):
    results = {}
    supplier = "supplier_loudwolf"
    positive_query = "acid"
    negative_query = "this_should_not_exist"


class TestSupplierOnyxmet(BaseTestClass):
    results = {}
    supplier = "supplier_onyxmet"
    positive_query = "rhodium"
    negative_query = "this_should_not_exist"


class TestSupplierSynthetika(BaseTestClass):
    results = {}
    supplier = "supplier_synthetika"
    positive_query = "Tartaric Acid"
    negative_query = "this_should_not_exist"


class TestSupplierTciChemicals(BaseTestClass):
    results = {}
    supplier = "supplier_tcichemicals"
    positive_query = "acetamide"
    negative_query = "this_should_not_exist"


class TestSupplierWarchem(BaseTestClass):
    results = {}
    supplier = "supplier_warchem"
    positive_query = "WODA"
    negative_query = "this_should_not_exist"


class TestSupplierLabchemDe(BaseTestClass):
    results = {}
    supplier = "supplier_labchemde"
    positive_query = "acet"
    negative_query = "this_should_not_exist"


class TestSupplierBunmurraLabs(BaseTestClass):
    results = {}
    supplier = "supplier_bunmurralabs"
    positive_query = "sodium"
    negative_query = "this_should_not_exist"


class TestSupplierHbarSci(BaseTestClass):
    results = {}
    supplier = "supplier_hbarsci"
    positive_query = "acid"
    negative_query = "this_should_not_exist"


class TestSupplierCarolinaChemical(BaseTestClass):
    results = {}
    supplier = "supplier_carolinachemical"
    positive_query = "acid"
    negative_query = "this_should_not_exist"


class TestSearchFactory(BaseTestClass):
    results = {}
    supplier = "search_factory"
    positive_query = "acid"
    negative_query = "this_should_not_exist"
