import asyncio
from decimal import Decimal

import pytest
import requests
from pytest import MonkeyPatch
from pytest_mock import MockerFixture

import chempare
from tests import mock_request_cache


# stats = [0, 0]

# full_stats = {}

# current_test_group = None
# current_test_module = None
# current_setup_group = None
# current_setup_module = None


# @pytest.hookimpl(hookwrapper=True)
# def pytest_runtest_setup(item):
#     global current_setup_group
#     global current_setup_module
#     print("Setting up", item.name)

#     current_setup_group = item.name
#     current_setup_module = item.module.__name__
#     outcome = yield
#     print("Tearing down", item.name)


# def pytest_itemcollected(item):
#     global current_test_group
#     global current_test_module
#     current_test_group = item.name
#     current_test_module = item.module.__name__
#     print('Inside pytest_itemcollected')
#     print(f"[pytest_itemcollected] {current_test_module=}, {current_test_group=}")


# def pytest_assertrepr_compare(config, op, left, right):
#     global stats
#     global current_test_group
#     global current_test_module

#     print(f"[pytest_assertrepr_compare] {current_test_module=}, {current_test_group=}")
#     # global full_stats
#     # if config.name not in full_stats:
#     #     full_stats[config.name] = [0, 0]
#     # full_stats[config.name][0] += 1
#     stats[0] += 1


# def pytest_assertion_pass(item, lineno, orig, expl):
#     global stats
#     global full_stats

#     global current_test_group
#     global current_test_module

#     passed_test_group = item.name
#     passed_test_module = item.module.__name__

#     print(f"[pytest_assertrepr_compare] {current_test_module=}, {current_test_group=}")
#     print(f"   {passed_test_group=}, {passed_test_module=}")
#     # full_stats[item.name][1] += 1
#     stats[1] += 1


# def pytest_runtest_teardown(item):
#     print(f"[pytest_runtest_teardown AA] {item=}, {stats=}")
#     outcome = yield
#     print(f"[pytest_runtest_teardown BB] {item=}, {stats=}")


# def pytest_runtest_call(item):
#     print(f"[pytest_runtest_call AA] {item=}, {stats=}")
#     outcome = yield
#     print(f"[pytest_runtest_call BB] {item=}, {stats=}")


# def pytest_terminal_summary(terminalreporter, exitstatus, config):
#     global stats
#     terminalreporter.ensure_newline()
#     terminalreporter.section("assert statistics", sep="=")
#     terminalreporter.line(f"total asserts : {full_stats=}")
#     if stats[0] > 0:
#         terminalreporter.line(f"passed asserts: {stats[1]} ({int(100*stats[1]/stats[0])}%)")
#         terminalreporter.line(f"failed asserts: {stats[0] - stats[1]} ({int(100*(stats[0] - stats[1])/stats[0])}%)")


# hookimpl definition: pytest_assertion_pass(session, assertionreport)
# Argument(s) {'assertionreport', 'session'} are declared in the hookimpl but can not be found in the hookspec
# monkeypatch = MonkeyPatch()


# @pytest.fixture(scope="session", autouse=True)
# def event_loop():
#     """Overrides pytest default function scoped event loop"""
#     policy = asyncio.get_event_loop_policy()
#     loop = policy.new_event_loop()
#     yield loop
#     loop.close()


# @pytest.fixture(scope="function", autouse=True)
# def setup_mock_cfg_to_curl_cffi_attrs(attr, monkeypatch):

#     # monkeypatch.setenv("TEST_MONKEYPATCHING", "true")
#     # monkeypatch.setenv("CALLED_FROM_TEST", "true")

#     # # setattr(mock_request_cache, 'mock_cfg', attr)
#     # mock_request_cache.requests = mock_request_cache.set_supplier_cache_session(getattr(attr, "supplier", "default"))

#     # monkeypatch.setattr(requests, "get", mock_request_cache.requests.get)
#     # monkeypatch.setattr(requests, "post", mock_request_cache.requests.post)
#     # monkeypatch.setattr(requests, "head", mock_request_cache.requests.head)
#     # monkeypatch.setattr(requests, "request", mock_request_cache.requests.request)
#     # chempare.test_monkeypatching = True
#     yield monkeypatch
#     # monkeypatch.delenv("TEST_MONKEYPATCHING")
#     # monkeypatch.delenv("CALLED_FROM_TEST")
#     monkeypatch.undo()
#     # chempare.test_monkeypatching = False


# def pytest_report_header(config):
#     chempare.called_from_test = True
#     ret = ["project deps: chempare-0.0"]
#     ret.append(f"chempare.called_from_test: {chempare.called_from_test}")
#     if config.getoption("verbose") > 0:
#         ret.extend([f"info1: Verbosity: {config.getoption('verbose')}"])
#     return ret


# @pytest.fixture
# def mock_exchange_rate(mocker: MockerFixture):
#     """Mocks a call to the ExchangeRateAPI, which calls Paikama API
#     https://hexarate.paikama.co/api/rates/latest/EUR?target=USD
#     """
#     mock_get = mocker.patch("currex.ExchangeRateAPI.get_rate")
#     mock_get.return_value = Decimal("1.1266")
#     return mock_get
