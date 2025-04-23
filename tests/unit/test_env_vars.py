# pylint: disable=unused-import
# pylint: disable=unused-wildcard-import
# pylint: disable=wildcard-import
# pylint: disable=missing-function-docstring
# pylint: disable=unused-argument
from __future__ import annotations

import os

import pytest
import chempare.utils as utils


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
