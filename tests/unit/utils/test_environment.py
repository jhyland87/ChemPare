# pylint: disable=unused-import
# pylint: disable=unused-wildcard-import
# pylint: disable=wildcard-import
# pylint: disable=missing-function-docstring
# pylint: disable=unused-argument
from __future__ import annotations

import os
import sys
from chempare.exceptions import UnsupportedPlatformError

import chempare.utils as utils
import pytest
from datatypes import Undefined
from datatypes import undefined
from pathlib import Path


# def get_environment_variable(name):
#     # value = os.getenv(name)
#     value = utils.getenv(name)
#     if value is None:
#         raise ValueError(f"Environment variable '{name}' not set.")
#     return value


def test_set_environment_variable(monkeypatch):
    monkeypatch.setenv("MY_VARIABLE", "test_value")
    assert utils.getenv("MY_VARIABLE") == "test_value"
    monkeypatch.undo()


def test_environment_variable_not_set(monkeypatch):
    with pytest.raises(ValueError) as excinfo:
        utils.getenv("NON_EXISTENT_VARIABLE")
    assert str(excinfo.value) == "Environment variable 'NON_EXISTENT_VARIABLE' not set."
    monkeypatch.undo()


def test_override_environment_variable(monkeypatch):
    os.environ["MY_VARIABLE"] = "original_value"
    monkeypatch.setenv("MY_VARIABLE", "override_value")
    assert utils.getenv("MY_VARIABLE") == "override_value"
    monkeypatch.undo()


@pytest.mark.parametrize(
    ("name", "value", "default", "typecast", "expected_result"),
    [
        #
        ("foo", "bar", None, None, "bar"),
        ("foo", "bar", "baz", None, "bar"),
        ("foo", Undefined, "baz", None, "baz"),
        ("foo", Undefined, None, None, None),
        ("foo", "123", None, False, "123"),
        ("foo", "123.4", None, False, "123.4"),
        ("foo", "123", None, True, 123),
        ("foo", "123.4", None, True, 123.4),
    ],
    ids=[
        #
        "Env var 'foo' set to 'bar'",
        "Env var 'foo' set to 'bar' (ignoring default)",
        "Env var 'foo' defaulted to 'baz'",
        "Env var 'foo' defaulted to 'None'",
        "Env var 'foo' set to '123'",
        "Env var 'foo' set to '123.4'",
        "Env var 'foo' set to 123",
        "Env var 'foo' set to 123.4",
    ],
)
def test_getenv(name, value, default, typecast, expected_result, monkeypatch):
    if value is not Undefined:
        monkeypatch.setenv(name, value)
    assert utils.getenv(name, default=default, typecast=typecast) == expected_result


import platform


@pytest.mark.skipif(sys.platform != "darwin", reason=f"does not run on {sys.platform}")
def test_get_default_browser(monkeypatch: pytest.MonkeyPatch):
    # Test brave on mac
    default_browser = utils.get_default_browser()
    assert default_browser == "brave", "get_default_browser did not return brave"

    # Test with no http or https LSHandlerURLScheme search results
    monkeypatch.setattr(utils, "find_first", lambda a, b: None)
    result = utils.get_default_browser()
    assert result is None, f"Returned '{type(result)}' even with no http(s) in LSHandlerURLScheme search results"

    # # Test a bad path to the com.apple.launchservices.secure.plist file
    monkeypatch.setattr(Path, "home", lambda: "/foo/bar")
    result = utils.get_default_browser()
    assert result is None, "Invalid path to launchservices did not return None"

    # # Test an unsupported system
    monkeypatch.setattr(platform, "system", lambda: "winblows")
    with pytest.raises(UnsupportedPlatformError) as unsupported_platform_error:
        utils.get_default_browser()
    assert "ERROR: No logic on getting the default browser for your platform: winblows" in str(
        unsupported_platform_error
    ), "No 'UnsupportedPlatformError' exception raised for Winblows"

    monkeypatch.undo()
