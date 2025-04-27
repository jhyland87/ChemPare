from __future__ import annotations

from chempare.utils import _cas, _html, _quantity, _general, _currency
import pytest


@pytest.mark.parametrize(
    ("value", "valid_cas"),
    [
        ("7732-18-5", True),
        ("7664-93-9", True),
        ("123-34-34", False),
        ("321-2-1", False),
        ("a-1-333", False),
        (123, False),
        ("000-00-0", False),
    ],
    ids=[
        "_cas.is_cas('7732-18-5') is True",
        "_cas.is_cas('7664-93-9') is True",
        "_cas.is_cas('123-34-34') is False",
        "_cas.is_cas('321-2-1') is False",
        "_cas.is_cas('a-1-333') is False",
        "_cas.is_cas(123) is False",
        "_cas.is_cas('000-00-0') is False",
    ],
)
def test_is_cas(value, valid_cas):
    result = _cas.is_cas(value)
    assert isinstance(result, bool) is True
    assert result is valid_cas


@pytest.mark.parametrize(
    ("string", "expected_result"),
    [
        ("The cas is 7732-18-5..", "7732-18-5"),
        ("First cas is 7664-93-9, then 7732-18-5", "7664-93-9"),
        ("No cas here", None),
        ("Invalid cas: 7732-18-4", None),
    ],
    ids=[
        "_cas.find_cas: Extract 7732-18-5 from string",
        "_cas.find_cas: Extract 7664-93-9 from string",
        "_cas.find_cas: No cas in string",
        "_cas.find_cas: Invalid cas in string",
    ],
)
def test_find_cas(string, expected_result):
    result = _cas.find_cas(string)
    assert type(result) is type(expected_result)
    assert result == expected_result
