from types import NoneType
import pytest
from datatypes import Undefined
from unittest.mock import patch
from decimal import Decimal
from chempare import utils


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


@pytest.mark.parametrize(
    ("symbol", "expected_result"),
    [("$", "USD"), ("CA$", "CAD"), ("€", "EUR"), ("£", "GBP"), ("¥", "JPY")],
    ids=[
        "util.get_currency_code_from_symbol('$') -> 'USD'",
        "util.get_currency_code_from_symbol('CA$') -> 'CAD'",
        "util.get_currency_code_from_symbol('€') -> 'EUR'",
        "util.get_currency_code_from_symbol('£') -> 'GBP'",
        "util.get_currency_code_from_symbol('¥') -> 'JYP'",
    ],
)
def test_get_currency_code_from_symbol(symbol, expected_result):
    result = utils.get_currency_code_from_symbol(symbol)
    assert result == expected_result, f"Expected '{symbol}' to return '{expected_result}'; found '{result}' instead"


@pytest.mark.parametrize(
    ("currency", "expected_result"),
    [("USD", "$"), ("CAD", "CA$"), ("EUR", "€"), ("GBP", "£"), ("JPY", "¥")],
    ids=[
        "util.get_currency_symbol_from_code('USD') -> '$'",
        "util.get_currency_symbol_from_code('CAD') -> 'CA$'",
        "util.get_currency_symbol_from_code('EUR') -> '€'",
        "util.get_currency_symbol_from_code('GBP') -> '£'",
        "util.get_currency_symbol_from_code('JYP') -> '¥'",
    ],
)
def test_get_currency_symbol_from_code(currency, expected_result):
    result = utils.get_currency_symbol_from_code(currency)
    assert result == expected_result, f"Expected '{currency}' to return '{expected_result}'; found '{result}' instead"


@pytest.mark.parametrize(
    ("value", "return_type", "price", "currency_symbol", "currency"),
    [
        ("$123.45", dict, 123.45, "$", "USD"),
        ("$12,345.45", dict, 12345.45, "$", "USD"),
        # ("$123.45 USD", dict, 123.45, "$", "USD"),
        ("CA$123.45", dict, 123.45, "CA$", "CAD"),
        ("€1,1234.5", dict, 11234.50, "€", "EUR"),
        ("£123", dict, 123, "£", "GBP"),
        ("674 ¥", dict, 674, "¥", "JPY"),
        ("ZAR123", dict, 123, "ZAR", "ZAR"),
        ("ZAR 456", dict, 456, "ZAR", "ZAR"),
        ("ZAR", NoneType, None, None, None),
        ("FOO", NoneType, None, None, None),
    ],
    ids=[
        "_parse_price: '$123.45' -> $123.45 USD",
        "_parse_price: '$12,345.45' -> $12,345.45 USD",
        # "_parse_price: '$123.45 USD' -> $123.45 USD",
        "_parse_price: 'CA$123.45' -> $123.45 CAD",
        "_parse_price: '€1,1234.5' -> €1,1234.50 EUR",
        "_parse_price: '£123' -> £123 GBP",
        "_parse_price: '674 ¥' -> 674 ¥ JPY",
        "_parse_price: 'ZAR123' -> 123 ZAR",
        "_parse_price: 'ZAR 456' -> 456 ZAR",
        "_parse_price: No value (ZAR)",
        "_parse_price: Invalid currency (FOO)",
    ],
)
def test_parse_price(value, return_type, price, currency_symbol, currency):
    result = utils.parse_price(value)
    assert type(result) is return_type, f"result type '{type(result)} and return_type '{return_type}' are not the same"


@pytest.mark.parametrize(
    ("value", "from_currency", "expected_output"),
    [
        (Decimal('100'), "EUR", 112.66),
        # ("€100", None, "EUR", Decimal('100'), 112.66),
        (Decimal('100234.10'), "EUR", 112923.74),
        (Decimal('321'), "GBP", 361.64),
        (Decimal('321346.64'), "GBP", 362029.12),
        (Decimal('123'), "JPY", 138.57),
        (Decimal('456'), "AUD", 513.73),
        (Decimal('123234.12'), "CAD", 138835.56),
        # ("XXXXX123,234.12", "CAD", "CAD", Decimal('123234.12'), 138835.56),
        # ("XXXXX123,234.12", None, None, Decimal('123234.12'), None),
        # (123.35, None, None, None, None),
        # (Decimal("678.9"), None, None, None, None),
        # ("Invalid Value", None, None, None, None),
        # ("¥123", "JPY", float),
        # ("AU$123", "AUD", float),
        # ("CA$123,234.12", "CAD", float),
        # ("FOO123", None, type(None)),
    ],
    ids=[
        "€100 to USD",
        # "€100 (EUR) to USD",
        "€100.234,10 (EUR) to USD",
        "£321 (GBP) to USD",
        "£321.346,64 (GBP) to USD",
        "¥321 (JPY) to USD",
        "AU$123 (AUD) to USD",
        "CA$123,234.12 (CAD) to USD",
        # "XXXXX$123,234.12 (CAD, specified) to USD",
        # "XXXXX123,234.12 [str] No currency found/provided",
        # "123.35 [float] No currency found/provided",
        # "678.9 [Decimal] No currency found/provided",
        # "Invalid value",
    ],
)
@patch("currex.ExchangeRateAPI.get_rate", lambda *argv: Decimal("1.1266"))
def test_to_usd(
    # mock_exchange_rate,
    value: Decimal,
    from_currency: str,
    expected_output: Decimal | None,
):
    result = utils.to_usd(amount=value, from_currency=from_currency)
    assert result is not None, f"{value} {from_currency} returned None"
    assert isinstance(result, Decimal), "result not of type Decimal"
    assert float(result) == float(expected_output), f"result does not match expected output"
