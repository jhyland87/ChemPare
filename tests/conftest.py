# from chempare import suppliers
# import os

from decimal import Decimal

import curl_cffi.requests

# import curl_cffi
import pytest
from mock_data import mock_curl_cffi

# from price_parser import Price
from pytest_mock import MockerFixture

import chempare


# from unittest.mock import MagicMock
# from unittest.mock import patch


# curl_cffi_post = MagicMock(wraps=mock_curl_cffi)


# @pytest.fixture(autouse=True)
# def setup_mock_curl_cffi_attrs(attr):
#     setattr(mock_curl_cffi.request, 'mock_cfg', attr)
#     yield
#     delattr(mock_curl_cffi.request, 'mock_cfg')


@pytest.fixture(autouse=True)
def setup_mock_cfg_to_curl_cffi_attrs(attr):
    setattr(mock_curl_cffi.request, 'mock_cfg', attr)
    setattr(curl_cffi.requests.Response, 'mock_cfg', attr)
    yield
    delattr(mock_curl_cffi.request, 'mock_cfg')
    delattr(curl_cffi.requests.Response, 'mock_cfg')


@pytest.fixture(autouse=True, scope="session", name="function requests mocker")
def monkeypatch_session():
    from _pytest.monkeypatch import MonkeyPatch

    monkeypatch = MonkeyPatch()
    monkeypatch.setattr(curl_cffi.requests, "request", mock_curl_cffi.request)
    chempare.test_monkeypatching = True
    yield monkeypatch
    monkeypatch.undo()
    monkeypatch.delattr(curl_cffi.requests, "request")
    chempare.test_monkeypatching = False


# @pytest.fixture(autouse=True, scope="function", name="requests mocker")
# @pytest.fixture(scope="session", name="function requests mocker")
# @pytest.fixture(autouse=True)
# def setup_mock_curl_cffi(monkeypatch):
#     monkeypatch.setattr(curl_cffi.requests, "request", mock_curl_cffi.request)
#     print("\n\n\nSetup setup_teardown\n\n\n")
#     yield
#     print("\n\n\nTeardown setup_teardown\n\n\n")
#     monkeypatch.delattr(curl_cffi.requests, "request")


# import webbrowser

# from pytest.fixtures import fixture


# def pytest_sessionfinish(session, exitstatus):
#     print("\n--- Test session finished ---")
#     print(f"Exit status: {exitstatus}")
#     # Add your custom actions here, e.g.,
#     # - Generating a summary report
#     # - Closing database connections
#     # - Cleaning up temporary files


# # Literal["session", "package", "module", "class", "function"]
# @fixture(autouse=True, scope='session')
# def my_session_fixture():
#     print("\n--- Test session setup ---")
#     yield
#     print("\n--- Test session teardown ---")


# @fixture(autouse=True, scope='function')
# def my_function_fixture():
#     print("\n--- Test function setup ---")
#     yield
#     print("\n--- Test function teardown ---")


# @fixture(autouse=True, scope='package')
# def my_package_fixture():
#     print("\n--- Test package setup ---")
#     yield
#     print("\n--- Test package teardown ---")


# @fixture(autouse=True, scope='class')
# def my_class_fixture():
#     print("\n--- Test class setup ---")
#     yield
#     print("\n--- Test class teardown ---")


# @fixture(autouse=True, scope='module')
# def my_module_fixture():
#     print("\n--- Test module setup ---")
#     yield
#     print("\n--- Test module teardown ---")


# def pytest_sessionfinish(session, exitstatus):
#     if os.environ.get('PYTEST_COV') == 'true':
#         # Code to run after all tests, specifically when coverage was measured
#         print("")
#         coverage_results = os.path.abspath("coverage-html/index.html")
#         print(f"Opening coerage file: {coverage_results}")

#         # try:
#         #     webbrowser.get("macosx").open(
#         #         f'file://{coverage_results}', new=0, autoraise=False
#         #     )  # "brave" might need adjustment based on OS and setup
#         # except webbrowser.Error:
#         #     print("Brave browser could not be found or opened.")
#         #     webbrowser.open(f'file://{coverage_results}', new=0, autoraise=False)
#         # # webbrowser.get('brave').open(f'file://{coverage_results}', new=0)


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


# def my_decorator(func):
#     def wrapper(*args, **kwargs):
#         # Do something before calling the function
#         print("Before calling function.")
#         result = func(*args, **kwargs)
#         # Do something after the function
#         print("After calling function.")
#         return result
#     return wrapper


# class _ParametrizeMarkDecorator(MarkDecorator):
#     def __call__(  # type: ignore[override]
#         self,
#         argnames: Union[str, Sequence[str]],
#         argvalues: Iterable[Union[ParameterSet, Sequence[object], object]],
#         *,
#         indirect: Union[bool, Sequence[str]] = ...,
#         ids: Optional[] = ...
#         ) -> MarkDecorator: ...
