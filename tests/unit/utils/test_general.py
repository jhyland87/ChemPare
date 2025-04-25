from __future__ import annotations

import functools
import math
import time
from ctypes import util
from decimal import Decimal
from typing import Literal
from unittest.mock import patch

import chempare.utils as utils
import pytest
from datatypes import PriceType
from datatypes import QuantityType
from datatypes import Undefined
from datatypes import undefined
from datatypes import UndefinedType
from price_parser.parser import Price


@pytest.mark.parametrize(
    ("value", "expected_result"),
    [({"foo": 123, "bar": 555}, {"bar": 555}), ({"foo": 999999, "bar": 123}, {"foo": 999999})],
    ids=["Pulling bar from object", "Pulling foo from object"],
)
def test_filter_highest_item_value(value, expected_result):
    result = utils.filter_highest_item_value(value)
    assert result == expected_result


@pytest.mark.parametrize(
    ("phrases", "expected_result"),
    [
        (
            [
                "oxidane",
                "WATER",
                "Atomic oxygen",
                "Monooxygen",
                "Oxygen(sup 3P)",
                "Oxygen, atomic",
                "Photooxygen",
                "Singlet oxygen",
                "acqua",
                "agua",
                "aqua",
                "H2O",
                "HYD",
                "HYDROXY GROUP",
                "BOUND OXYGEN",
            ],
            {("atomic",): 2, ("oxygen",): 4},
        )
    ],
    ids=["Parse array of phrases"],
)
def test_get_common_phrases(phrases, expected_result):
    result = utils.get_common_phrases(phrases)
    assert isinstance(result, dict) is True
    assert result == expected_result


@pytest.mark.parametrize(
    ("values", "element", "expected_result"),
    [
        ({(1, 2): "a", (2, 3): "b", (3, 4): "c", "hello": "d", (2, 5, 6): "e"}, 1, ["a"]),
        ({(1, 2): "a", (2, 3): "b", (3, 4): "c", "hello": "d", (2, 5, 6): "e"}, 2, ["a", "b", "e"]),
        ({(1, 2): "a", (2, 3): "b", (3, 4): "c", "hello": "d", (2, 5, 6): "e"}, "hello", ["d"]),
        ({(1, 2): "a", (2, 3): "b", (3, 4): "c", "hello": "d", (2, 5, 6): "e"}, "test", []),
    ],
    ids=[
        "Search for element with one result",
        "Search for element with multiple results",
        "Search for key instead of element",
        "Search for element/key that does not exist",
    ],
)
def test_find_values_with_element(values, element, expected_result):
    res = utils.find_values_with_element(values, element)
    assert res is not None
    assert type(res) is type(expected_result)
    assert res == expected_result


@pytest.mark.parametrize(
    ("value", "expected_result"),
    [
        ("foo", "foo"),
        ("123", 123),
        ("123.4", 123.4),
        ("123.4500", 123.45),
        ("None", None),
        ("null", None),
        ("true", True),
        ("FALSE", False),
        ("  false  ", False),
        ("  321  ", 321),
    ],
    ids=[
        "Not casting alpha string",
        "Casting '123' to int: 123",
        "Casting '123.4' to float: 123.4",
        "Casting '123.4500' to float: 123.45",
        "Casting 'None' to NoneType: None",
        "Casting 'null' to NoneType: None",
        "Casting 'true' to bool: True",
        "Casting 'FALSE' to bool: False",
        "Casting '  false  ' to bool: False",
        "Casting '  321  ' to int: 321",
    ],
)
def test_cast_strings(value, expected_result):
    result = utils.cast(value)
    assert (
        type(result) is type(expected_result)
    ) is True, f"Returned type '{type(value).__name__}' instead of '{type(expected_result).__name__}'"
    assert result == expected_result, f"Expected '{result}' to equal '{expected_result}'"


@pytest.mark.parametrize(
    ("value", "expected_result"),
    [
        (True, ValueError),
        (False, ValueError),
        (None, ValueError),
        (123, ValueError),
        (list(), ValueError),
        (dict(), ValueError),
    ],
    ids=[
        "Casting True (bool) should raise ValueError",
        "Casting False (bool) should raise ValueError",
        "Casting None (NoneType) should raise ValueError",
        "Casting 123 (int) should raise ValueError",
        "Casting list should raise ValueError",
        "Casting dict should raise ValueError",
    ],
)
def test_cast_uncastables(value, expected_result):
    with pytest.raises(ValueError) as value_error:
        utils.cast(value)
    assert value_error.errisinstance(expected_result) is True, f"Expected a '{type(expected_result).__name__}' error"

    assert str(value_error.value) == f"Unable to cast value type '{type(value).__name__}' - Must be a string"


@pytest.mark.parametrize(
    ("dataobject", "path", "default", "expected_result"),
    [
        #
        ({"foo": {"bar": "baz"}}, "foo.bar", None, "baz"),
        ({"foo": {"bar": "baz"}}, "foo.qux", None, None),
    ],
    ids=[
        #
        "'foo.bar' should find 'baz' in {foo:{bar:baz}}",
        "'foo.qux' shoudl default to None in {foo:{bar:baz}}",
    ],
)
def test_get_nested(dataobject, path, default, expected_result):
    paths = path.split(".")
    assert utils.get_nested(dataobject, *paths, default=default) == expected_result


@pytest.mark.parametrize(
    ("length", "include_special"),
    [(None, None), (5, None), (100, None), (10, True)],
    ids=[
        "utils.random_string: None -> return unique 10 character alphanumeric string",
        "utils.random_string: 5 -> return unique 5 character alphanumeric string",
        "utils.random_string: 100 -> return unique 100 character alphanumeric string",
        "utils.random_string: 10 (include_special) -> return unique 10 character alphanumeric+special string",
    ],
)
def test_random_string(length, include_special):
    result_a = utils.random_string(length, include_special)
    result_b = utils.random_string(length, include_special)

    assert isinstance(result_a, str) is True
    assert isinstance(result_b, str) is True

    assert len(result_a) == length or 10
    assert len(result_b) == length or 10
    # All results should be ascii..
    assert str(result_a).isascii() is True
    assert str(result_b).isascii() is True
    # assert str.isascii(result_a) is True
    # assert str.isascii(result_b) is True

    # If were including special chars then isalnum should be
    # False (inverse of include_special)
    # assert str.isalnum(result_a) is not include_special
    # assert str.isalnum(result_b) is not include_special
    assert str(result_a).isalnum() is not include_special
    assert str(result_b).isalnum() is not include_special

    # Obviously they should never be the same value
    assert result_a != result_b


@pytest.mark.parametrize(
    ("array", "expected_result"),
    [
        (["Variant", "500 g", "CAS", "1762-95-4"], [["Variant", "500 g"], ["CAS", "1762-95-4"]]),
        (["name", "23", "address"], [["name", "23"], ["address"]]),
    ],
)
def test_split_array_into_groups(array, expected_result):
    result = utils.split_array_into_groups(array)

    if type(result) is not type(expected_result):
        pytest.fail(f"Expected type '{type(expected_result)}' for result, but got '{type(result)}'")

    assert result == expected_result


@pytest.mark.parametrize(
    ("array", "expected_result"),
    [
        # ([["a", "b"]], {"a": "b"}),
        ([["c", "d"], ["e", "f"]], {"c": "d", "e": "f"}),
        ([["foo"]], None),
    ],
    ids=[
        # "[[a,b]] to {a:b}",
        "[[c,d],[e,123]] to {c:d,e:123}",
        "[[foo]] should return None",
    ],
)
def test_nested_arr_to_dict(array, expected_result):
    result = utils.nested_arr_to_dict(array)

    if expected_result is None:
        assert result is None
    else:
        assert result == expected_result
        assert isinstance(result, dict) is True


@pytest.mark.parametrize(
    ("value", "param_name", "expected_result"),
    [
        ("http://google.com?foo=bar&product_id=12345", None, {"foo": "bar", "product_id": "12345"}),
        ("http://google.com?foo=bar&product_id=12345", "product_id", "12345"),
    ],
    ids=["no param_name", "with param_name"],
)
def test_get_param_from_url(
    value: Literal["http://google.com?foo=bar&product_id=12345"],
    param_name: None | Literal["product_id"],
    expected_result: dict[str, str] | Literal["12345"],
):
    result = utils.get_param_from_url(value, param_name)

    if type(result) is not type(expected_result):
        pytest.fail(f"type of result ({type(result)}) does not match expected result type ({type(expected_result)})")
    elif result != expected_result:
        pytest.fail("result is not identical to expected reslt")


def test_epoch():
    now = math.floor(time.time() * 1000) - 1
    result = utils.epoch()
    assert isinstance(result, int) is True
    assert result > now
