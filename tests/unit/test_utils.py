import pytest
from datatypes import Undefined

from chempare import utils


# import chempare.utils as utils


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
    ("name", "value", "default", "expected_result"),
    [
        #
        ("foo", "bar", None, "bar"),
        ("foo", "bar", "baz", "bar"),
        ("foo", Undefined, "baz", "baz"),
        ("foo", Undefined, None, None),
    ],
    ids=[
        #
        "Env var 'foo' set to 'bar'",
        "Env var 'foo' set to 'bar' (ignoring default)",
        "Env var 'foo' defaulted to 'baz'",
        "Env var 'foo' defaulted to 'None'",
    ],
)
def test_getenv(name, value, default, expected_result, monkeypatch):
    if value is not Undefined:
        monkeypatch.setenv(name, value)
    assert utils.getenv(name, default=default) == expected_result


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
