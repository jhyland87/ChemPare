from __future__ import annotations

from decimal import Decimal
from types import NoneType
from unittest.mock import patch
from typing import Literal
import pytest
import chempare.utils as utils
from datatypes import Undefined
import math

import time


@pytest.mark.parametrize(
    ("value", "expected_result", "expected_instance"),
    [
        ("123", "123.00", Decimal),
        (123, "123.00", Decimal),
        ("123.0", "123.00", Decimal),
        (123.0, "123.00", Decimal),
        ("123.45", "123.45", Decimal),
        (123.45, "123.45", Decimal),
        ("123.45678", "123.46", Decimal),
        (123.45678, "123.46", Decimal),
        ("123.4511", "123.45", Decimal),
        (123.4511, "123.45", Decimal),
    ],
    ids=[
        "str('123') to '123.00'",
        "int(123) to '123.00'",
        "str('123.0') to '123.00'",
        "int(123.0) to '123.00'",
        "str('123.45') to '123.45'",
        "int(123.45) to '123.45'",
        "str('123.45678') to '123.46'",
        "int(123.45678) to '123.46'",
        "str('123.4511') to '123.45'",
        "int(123.4511) to '123.45'",
    ],
)
def test_to_hundreths(value, expected_result, expected_instance):
    output = utils.to_hundreths(value)

    assert isinstance(output, expected_instance) is True, "Unexpected instance type returned from utils.to_hundreths"

    assert str(output) == str(expected_result), "Output does not match expected result"


@pytest.mark.parametrize(
    ("symbol", "expected_result"),
    [("$", "USD"), ("CA$", "CAD"), ("€", "EUR"), ("£", "GBP"), ("¥", "JPY")],
    ids=[
        "utils.get_currency_code_from_symbol('$') -> 'USD'",
        "utils.get_currency_code_from_symbol('CA$') -> 'CAD'",
        "utils.get_currency_code_from_symbol('€') -> 'EUR'",
        "utils.get_currency_code_from_symbol('£') -> 'GBP'",
        "utils.get_currency_code_from_symbol('¥') -> 'JYP'",
    ],
)
def test_get_currency_code_from_symbol(symbol, expected_result):
    result = utils.get_currency_code_from_symbol(symbol)
    assert result == expected_result, f"Expected '{symbol}' to return '{expected_result}'; found '{result}' instead"


@pytest.mark.parametrize(
    ("currency", "expected_result"),
    [("USD", "$"), ("CAD", "CA$"), ("EUR", "€"), ("GBP", "£"), ("JPY", "¥")],
    ids=[
        "utils.get_currency_symbol_from_code('USD') -> '$'",
        "utils.get_currency_symbol_from_code('CAD') -> 'CA$'",
        "utils.get_currency_symbol_from_code('EUR') -> '€'",
        "utils.get_currency_symbol_from_code('GBP') -> '£'",
        "utils.get_currency_symbol_from_code('JYP') -> '¥'",
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
        "utils.parse_price: '$123.45' -> $123.45 USD",
        "utils.parse_price: '$12,345.45' -> $12,345.45 USD",
        # "utils.parse_price: '$123.45 USD' -> $123.45 USD",
        "utils.parse_price: 'CA$123.45' -> $123.45 CAD",
        "utils.parse_price: '€1,1234.5' -> €1,1234.50 EUR",
        "utils.parse_price: '£123' -> £123 GBP",
        "utils.parse_price: '674 ¥' -> 674 ¥ JPY",
        "utils.parse_price: 'ZAR123' -> 123 ZAR",
        "utils.parse_price: 'ZAR 456' -> 456 ZAR",
        "utils.parse_price: No value (ZAR)",
        "utils.parse_price: Invalid currency (FOO)",
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


@pytest.mark.parametrize(
    ("char", "is_currency"),
    [("$", True), ("¥", True), ("£", True), ("€", True), ("₽", True), ("A", False), ("Test", False)],
    ids=[
        "utils.is_currency_symbol('$') is True",
        "utils.is_currency_symbol('¥') is True",
        "utils.is_currency_symbol('£') is True",
        "utils.is_currency_symbol('€') is True",
        "utils.is_currency_symbol('₽') is True",
        "utils.is_currency_symbol('A') is False",
        "utils.is_currency_symbol('Test') is False",
    ],
)
def test_is_currency_symbol(char, is_currency):
    result = utils.is_currency_symbol(char)
    assert isinstance(result, bool) is True
    assert result is is_currency
