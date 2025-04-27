from __future__ import annotations

import functools
import math
import time
from ctypes import util
from decimal import Decimal
from types import NoneType
from typing import Literal
from unittest.mock import patch

from chempare.utils import _cas, _html, _quantity, _general, _currency
import pytest
from datatypes import PriceType
from datatypes import QuantityType
from price_parser.parser import Price


@pytest.mark.parametrize(
    ("value", "expected_type", "quantity", "uom"),
    [
        ("1 ounce", dict, "1", "oz"),
        ("43 ounces", dict, "43", "oz"),
        ("1 lb", dict, "1", "lb"),
        ("4 lbs", dict, "4", "lb"),
        ("5 g", dict, "5", "g"),
        ("10 gal", dict, "10", "gal"),
        ("43.56 qt", dict, "43.56", "qt"),
        ("10L", dict, "10", "L"),
        ("5 l", dict, "5", "L"),
        ("123.45mm", dict, "123.45", "mm"),
        ("100 millimeters", dict, "100", "mm"),
        ("1234ml", dict, "1234", "mL"),
        ("foobar", NoneType, None, None),
    ],
    ids=[
        "_quantity.parse_quantity: '1 ounce' -> 1 ounce",
        "_quantity.parse_quantity: '43 ounces' -> 43 ounces",
        "_quantity.parse_quantity: '1 lb' -> 1 lb",
        "_quantity.parse_quantity: '4 lbs' -> 4 lbs",
        "_quantity.parse_quantity: '5 g' -> 5 g",
        "_quantity.parse_quantity: '10 gal' -> 10 gal",
        "_quantity.parse_quantity: '43.56 qt' -> 43.56 qt",
        "_quantity.parse_quantity: '10L' -> 10 L",
        "_quantity.parse_quantity: '5 l' -> 5 L",
        "_quantity.parse_quantity: '123.45mm' -> 123.45 mm",
        "_quantity.parse_quantity: '100 millimeters' -> 100 millimeters",
        "_quantity.parse_quantity: '1234ml' -> 1234 mL",
        "_quantity.parse_quantity: 'foobar' -> None",
    ],
)
def test_parse_quantity(value, expected_type, quantity, uom):
    result = _quantity.parse_quantity(value)

    assert (
        type(result) is expected_type
    ), f"Expected {value} to return type {expected_type.__name__}, but received {type(result)}"

    if expected_type is NoneType:
        return
    # assert isinstance(
    #     result, expected_type
    # ), f"Expected {value} to return type {expected_type.__name__}, but received {type(value)}"

    assert "quantity" in result, "Result does not have 'quantity' attribute"

    if "quantity" in result:
        assert result["quantity"] == quantity, f"Result quantity {result["quantity"]} is not {quantity}"

    assert "uom" in result, "Result does not have 'uom' attribute"

    if "uom" in result:
        assert result["uom"] == uom, f"Result uom {result["uom"]} is not {uom}"
