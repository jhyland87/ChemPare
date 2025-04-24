from __future__ import annotations

import functools
import math
import time
from ctypes import util
from decimal import Decimal
from typing import Literal
from unittest.mock import patch

import pytest
import chempare.utils as utils
from chempare.utils import ClassUtils
from datatypes import PriceType
from datatypes import QuantityType
from price_parser.parser import Price

# pylint: disable=unused-import
# pylint: disable=unused-wildcard-import
# pylint: disable=wildcard-import
# pylint: disable=missing-function-docstring
# pylint: disable=unused-argument


class TestClass(ClassUtils):

    @pytest.mark.parametrize(
        ("value", "expected_instance", "quantity", "uom"),
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
        ],
        ids=[
            "_parse_quantity: '1 ounce' -> 1 ounce",
            "_parse_quantity: '43 ounces' -> 43 ounces",
            "_parse_quantity: '1 lb' -> 1 lb",
            "_parse_quantity: '4 lbs' -> 4 lbs",
            "_parse_quantity: '5 g' -> 5 g",
            "_parse_quantity: '10 gal' -> 10 gal",
            "_parse_quantity: '43.56 qt' -> 43.56 qt",
            "_parse_quantity: '10L' -> 10 L",
            "_parse_quantity: '5 l' -> 5 L",
            "_parse_quantity: '123.45mm' -> 123.45 mm",
            "_parse_quantity: '100 millimeters' -> 100 millimeters",
            "_parse_quantity: '1234ml' -> 1234 mL",
        ],
    )
    def test_parse_quantity(self, value, expected_instance, quantity, uom):
        result = self._parse_quantity(value)

        if expected_instance is None:
            assert result == expected_instance, f"Result {result} incorrect, needs to be {expected_instance}"
            return

        assert isinstance(
            result, expected_instance
        ), f"Expected {value} to return type {expected_instance.__name__}, but received {type(value)}"

        assert "quantity" in result, "Result does not have 'quantity' attribute"

        if "quantity" in result:
            assert result["quantity"] == quantity, f"Result quantity {result["quantity"]} is not {quantity}"

        assert "uom" in result, "Result does not have 'uom' attribute"

        if "uom" in result:
            assert result["uom"] == uom, f"Result uom {result["uom"]} is not {uom}"

    @pytest.mark.parametrize(
        ("cas", "valid_cas"),
        [("7732-18-5", True), ("7664-93-9", True), ("123-34-34", False), ("321-2-1", False), ("a-1-333", False)],
        ids=[
            "_is_cas('7732-18-5') is True",
            "_is_cas('7664-93-9') is True",
            "_is_cas('123-34-34') is False",
            "_is_cas('321-2-1') is False",
            "_is_cas('a-1-333') is False",
        ],
    )
    def test_is_cas(self, cas, valid_cas):
        result = self._is_cas(cas)
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
            "_find_cas: Extract 7732-18-5 from string",
            "_find_cas: Extract 7664-93-9 from string",
            "_find_cas: No cas in string",
            "_find_cas: Invalid cas in string",
        ],
    )
    def test_find_cas(self, string, expected_result):
        result = self._find_cas(string)
        assert type(result) is type(expected_result)
        assert result == expected_result

    # @pytest.mark.parametrize(
    #     ("code", "expected_result"),
    #     [("USD", "$"), ("RUB", "₽"), ("EUR", "€"), ("GBP", "£"), ("JPY", "¥"), ("ABCD", None)],
    #     ids=["USD is $", "RUB is ₽", "EUR is €", "GBP is £", "JPY is ¥", "ABCD is None"],
    # )
    # def test_currency_symbol_from_code(self, code, expected_result):
    #     result = self._currency_symbol_from_code(code)
    #     assert type(result) is type(expected_result)
    #     if expected_result is None:
    #         assert result is None
    #     else:
    #         assert result == expected_result

    @pytest.mark.parametrize(
        ("value", "expected_result"),
        [({"foo": 123, "bar": 555}, {"bar": 555}), ({"foo": 999999, "bar": 123}, {"foo": 999999})],
        ids=["Pulling bar from object", "Pulling foo from object"],
    )
    def test_filter_highest_item_value(self, value, expected_result):
        result = self._filter_highest_item_value(value)
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
    def test_get_common_phrases(self, phrases, expected_result):
        result = self._get_common_phrases(phrases)
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
    def test_find_values_with_element(self, values, element, expected_result):
        res = self._find_values_with_element(values, element)
        assert res is not None
        assert type(res) is type(expected_result)
        assert res == expected_result

    # @pytest.mark.parametrize(
    #     ("content", "search", "expected_result"),
    #     [
    #         ("sodium borohydride", "sodium borohydride", True),
    #         ("SODIUM BOROHYDRIDE", "sodium borohydride", True),
    #         ("Pure sodium borohydride, 100%", "sodium borohydride", True),
    #         ("Technical SODIUM BOROHYDRIDE..", "sodium borohydride", True),
    #         (
    #             "Pure triacetoxyborohydride borohydride, 100%",
    #             "sodium borohydride",
    #             False,
    #         ),
    #     ],
    #     ids=[
    #         "'sodium borohydride' contains 'sodium borohydride'",
    #         "'SODIUM BOROHYDRIDE' contains 'sodium borohydride'",
    #         "'Pure sodium borohydride, 100%' contains 'sodium borohydride'",
    #         "'Technical SODIUM BOROHYDRIDE..' contains 'sodium borohydride'",
    #         (
    #             "'Pure triacetoxyborohydride borohydride, 100%' "
    #             "does not contain 'sodium borohydride'"
    #         ),
    #     ],
    # )
    # def test_contains_exact_match(self, content, search, expected_result):
    #     result = self._contains_exact_match(content, search)
    #     assert isinstance(result, bool) is True
    #     assert result == expected_result
