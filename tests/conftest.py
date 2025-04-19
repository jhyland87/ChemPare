from decimal import Decimal

import pytest
import requests
from pytest import MonkeyPatch
from pytest_mock import MockerFixture

import chempare
from tests import mock_request_cache


@pytest.fixture(autouse=True)
def setup_mock_cfg_to_curl_cffi_attrs(attr):
    monkeypatch = MonkeyPatch()
    # setattr(mock_request_cache, 'mock_cfg', attr)
    mock_request_cache.requests = mock_request_cache.set_supplier_cache_session(attr.supplier)

    monkeypatch.setattr(requests, "get", mock_request_cache.requests.get)
    monkeypatch.setattr(requests, "post", mock_request_cache.requests.post)
    monkeypatch.setattr(requests, "head", mock_request_cache.requests.head)
    monkeypatch.setattr(requests, "request", mock_request_cache.requests.request)
    chempare.test_monkeypatching = True
    yield monkeypatch
    monkeypatch.undo()
    chempare.test_monkeypatching = False


def pytest_report_header(config):
    chempare.called_from_test = True
    ret = ["project deps: chempare-0.0"]
    ret.append(f"chempare.called_from_test: {chempare.called_from_test}")
    if config.getoption("verbose") > 0:
        ret.extend([f"info1: Verbosity: {config.getoption('verbose')}"])
    return ret


@pytest.fixture
def mock_exchange_rate(mocker: MockerFixture):
    """Mocks a call to the ExchangeRateAPI, which calls Paikama API
    https://hexarate.paikama.co/api/rates/latest/EUR?target=USD
    """
    mock_get = mocker.patch("currex.ExchangeRateAPI.get_rate")
    mock_get.return_value = Decimal("1.1266")
    return mock_get
