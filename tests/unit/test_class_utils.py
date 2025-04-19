import functools
import math
import time
from decimal import Decimal
from typing import Literal
from unittest.mock import patch

import pytest
from datatypes import PriceType
from datatypes import QuantityType
from price_parser.parser import Price

from chempare.utils import ClassUtils


# pylint: disable=unused-import
# pylint: disable=unused-wildcard-import
# pylint: disable=wildcard-import
# pylint: disable=missing-function-docstring
# pylint: disable=unused-argument


class TestClass(ClassUtils, object):
    @pytest.mark.parametrize(
        ("value", "return_type", "price", "currency", "currency_code"),
        [
            ("$123.45", PriceType, 123.45, "$", "USD"),
            ("$12,345.45", PriceType, 12345.45, "$", "USD"),
            ("$123.45 USD", PriceType, 123.45, "$", "USD"),
            ("CA$123.45", PriceType, 123.45, "CA$", "CAD"),
            ("€1,1234.5", PriceType, 11234.50, "€", "EUR"),
            ("£123", PriceType, 123, "£", "GBP"),
            ("674 ¥", PriceType, 674, "¥", "JPY"),
            ("ZAR123", PriceType, 123, "ZAR", "ZAR"),
            ("ZAR 456", PriceType, 456, "ZAR", "ZAR"),
            ("ZAR", None, None, None, None),
            ("FOO", None, None, None, None),
        ],
        ids=[
            "_parse_price: '$123.45' -> $123.45 USD",
            "_parse_price: '$12,345.45' -> $12,345.45 USD",
            "_parse_price: '$123.45 USD' -> $123.45 USD",
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
    def test_parse_price(self, value, return_type, price, currency, currency_code):
        result = self._parse_price(value)

        if return_type is None:
            assert result is None
            return

        assert isinstance(
            result, return_type
        ), f"Expected result instance of {return_type.__name__}, but was {type(result).__name__}"

        assert hasattr(result, "price"), "No 'price' found in result"

        assert hasattr(result, "currency_code"), "No 'currency_code' found in result"

        if hasattr(result, "currency_code"):
            assert (
                result.currency_code == currency_code
            ), f"Received currency code {result.currency}, expected {currency_code}"

        assert hasattr(result, "currency"), "No 'currency' found in result"

        if result.currency_code != "USD":
            # If the currency code is not the same as the currency (symbol), then we should have a USD conversion
            if result.currency_code != result.currency:
                assert hasattr(result, "usd") is True, f"No USD conversion found for {result.currency} conversion"
            else:
                # If there was no currency code/symbol found, then there likely won't be a way
                # to convert it to usd, so verify that wasn't done
                assert (
                    hasattr(result, "usd") is False or result.usd is None
                ), f"Found unexpected USD conversion in result ({result.usd})"

        if price:
            assert result.price == price

        if currency:
            assert result.currency == currency

        if price:
            assert result.currency_code == currency_code

    @pytest.mark.parametrize(
        ("value", "from_currency_param", "expected_currency", "from_amount", "expected_output"),
        [
            ("€100", None, "EUR", Decimal('100'), 112.66),
            # ("€100", None, "EUR", Decimal('100'), 112.66),
            ("€100.234,10", None, "EUR", Decimal('100234.10'), 112923.74),
            ("£321", None, "GBP", Decimal('321'), 361.64),
            ("£321.346,64", None, "GBP", Decimal('321346.64'), 362029.12),
            ("¥123", None, "JPY", Decimal('123'), 138.57),
            ("AU$456", None, "AUD", Decimal('456'), 513.73),
            ("CA$123,234.12", None, "CAD", Decimal('123234.12'), 138835.56),
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
    class FakeConn:
        def logTime(self, begin, end):
            print(begin, end)

    @patch("currex.ExchangeRateAPI.get_rate", Decimal("1.1266"))
    def test_to_usd(
        self,
        # mock_exchange_rate,
        value: str,
        from_currency_param: str | None,
        expected_currency: str | None,
        from_amount: Decimal | None,
        expected_output: Decimal | None,
    ):
        amnt_convert = Price.fromstring(value)
        converted_from_symbol = self._currency_code_from_symbol(str(amnt_convert.currency))
        if converted_from_symbol:
            assert converted_from_symbol == expected_currency
        assert amnt_convert.amount == from_amount
        # assert amnt_convert == "asfd"
        # Price(amount=Decimal('100'), currency='€')
        # b'{"status_code":200,"data":{"base":"EUR","target":"USD","mid":1.1266,"unit":1,"timestamp":"2025-04-11T00:02:59.806Z"}}'
        result = self._to_usd(amount=value, from_currency=from_currency_param)

        # if expected_currency:
        #     mock_exchange_rate.assert_called_with(expected_currency, "USD")

        if expected_output:
            assert result == expected_output, f"Conversion to USD from {expected_currency} incorrect"

        assert type(result) is type(
            expected_output
        ), f"Result type of {type(result)} was expected to be {type(expected_output)}"

    # _to_hundreths
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
    def test_to_hundreths(self, value, expected_result, expected_instance):
        output = self._to_hundreths(value)

        assert (
            isinstance(output, expected_instance) is True
        ), "Unexpected instance type returned from self._to_hundreths"

        assert str(output) == str(expected_result), "Output does not match expected result"

    @pytest.mark.parametrize(
        ("value", "expected_instance", "quantity", "uom"),
        [
            ("1 ounce", QuantityType, "1", "oz"),
            ("43 ounces", QuantityType, "43", "oz"),
            ("1 lb", QuantityType, "1", "lb"),
            ("4 lbs", QuantityType, "4", "lb"),
            ("5 g", QuantityType, "5", "g"),
            ("10 gal", QuantityType, "10", "gal"),
            ("43.56 qt", QuantityType, "43.56", "qt"),
            ("10L", QuantityType, "10", "L"),
            ("5 l", QuantityType, "5", "L"),
            ("123.45mm", QuantityType, "123.45", "mm"),
            ("100 millimeters", QuantityType, "100", "mm"),
            ("1234ml", QuantityType, "1234", "mL"),
            ("abcd", None, None, None),
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
            "error",
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

        assert hasattr(result, "quantity"), f"Result does not have 'quantity' attribute"

        if hasattr(result, "quantity"):
            assert result.quantity == quantity, f"Result quantity {result.quantity} is not {quantity}"

        assert hasattr(result, "uom"), f"Result does not have 'uom' attribute"

        if hasattr(result, "uom"):
            assert result.uom == uom, f"Result uom {result.uom} is not {uom}"

    @pytest.mark.parametrize(
        ("value", "param_name", "expected_result"),
        [
            ("http://google.com?foo=bar&product_id=12345", None, {"foo": "bar", "product_id": "12345"}),
            ("http://google.com?foo=bar&product_id=12345", "product_id", "12345"),
        ],
        ids=["no param_name", "with param_name"],
    )
    def test_get_param_from_url(
        self,
        value: Literal["http://google.com?foo=bar&product_id=12345"],
        param_name: None | Literal["product_id"],
        expected_result: dict[str, str] | Literal["12345"],
    ):
        result = self._get_param_from_url(value, param_name)

        if type(result) is not type(expected_result):
            pytest.fail(
                f"type of result ({type(result)}) does not match expected result type ({type(expected_result)})"
            )
        elif result != expected_result:
            pytest.fail("result is not identical to expected reslt")

    @pytest.mark.parametrize(
        ("array", "expected_result"),
        [
            (["Variant", "500 g", "CAS", "1762-95-4"], [["Variant", "500 g"], ["CAS", "1762-95-4"]]),
            (["name", "23", "address"], [["name", "23"], ["address"]]),
        ],
    )
    def test_split_array_into_groups(self, array, expected_result):
        result = self._split_array_into_groups(array)

        if type(result) is not type(expected_result):
            pytest.fail(f"Expected type '{type(expected_result)}' for result, but got '{type(result)}'")

        assert result == expected_result
        # if len(result) != 2:
        #     pytest.fail(f"length of result ({len(result)}) is not equal to 2")

        # if len(result[0]) != 2:
        #     pytest.fail(f"length of result[0] ({len(result[0])}) is not equal to 2")

        # if len(result[1]) != 2:
        #     pytest.fail(f"length of result[1] ({len(result[1])}) is not equal to 2")

        # if result[0][0] != "Variant":
        #     pytest.fail(
        #         f'expected to find "Variant" at result[0][0], found "{result[0][0]}'
        #     )

        # if result[0][1] != "500 g":
        #     pytest.fail(
        #         f'expected to find "500 g" at result[0][1], found "{result[0][1]}'
        #     )

        # if result[1][0] != "CAS":
        #     pytest.fail(
        #         f'expected to find "CAS" at result[1][0], found "{result[1][0]}'
        #     )

        # if result[1][1] != "1762-95-4":
        #     pytest.fail(
        #         f'expected to find "1762-95-4" at result[1][1], found "{result[1][1]}'
        #     )

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
    def test_nested_arr_to_dict(self, array, expected_result):
        result = self._nested_arr_to_dict(array)

        if expected_result is None:
            assert result is None
        else:
            assert result == expected_result
            assert isinstance(result, dict) is True

    def test_epoch(self):
        now = math.floor(time.time() * 1000) - 1
        result = self._epoch
        assert isinstance(result, int) is True
        assert result > now

    @pytest.mark.parametrize(
        ("char", "is_currency"),
        [("$", True), ("¥", True), ("£", True), ("€", True), ("₽", True), ("A", False), ("Test", False)],
        ids=[
            "_is_currency('$') is True",
            "_is_currency('¥') is True",
            "_is_currency('£') is True",
            "_is_currency('€') is True",
            "_is_currency('₽') is True",
            "_is_currency('A') is False",
            "_is_currency('Test') is False",
        ],
    )
    def test_is_currency_symbol(self, char, is_currency):
        result = self._is_currency_symbol(char)
        assert isinstance(result, bool) is True
        assert result is is_currency

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

    @pytest.mark.parametrize(
        ("symbol", "expected_result"),
        [("$", "USD"), ("₽", "RUB"), ("€", "EUR"), ("£", "GBP"), ("¥", "JPY"), ("ABCD", None)],
        ids=["$ is USD", "₽ is RUB", "€ is EUR", "£ is GBP", "¥ is JPY", "ABCD is None"],
    )
    def test_currency_code_from_symbol(self, symbol, expected_result):
        result = self._currency_code_from_symbol(symbol)
        assert type(result) is type(
            expected_result
        ), f"Result type {type(result)} was expected to be {type(expected_result)}"
        if expected_result is None:
            assert result is None, f"Expected result of {symbol} to be None, received {result}"

        else:
            assert result == expected_result, f"Expected result of {symbol} to be {expected_result}, received {result}"

    @pytest.mark.parametrize(
        ("code", "expected_result"),
        [("USD", "$"), ("RUB", "₽"), ("EUR", "€"), ("GBP", "£"), ("JPY", "¥"), ("ABCD", None)],
        ids=["USD is $", "RUB is ₽", "EUR is €", "GBP is £", "JPY is ¥", "ABCD is None"],
    )
    def test_currency_symbol_from_code(self, code, expected_result):
        result = self._currency_symbol_from_code(code)
        assert type(result) is type(expected_result)
        if expected_result is None:
            assert result is None
        else:
            assert result == expected_result

    @pytest.mark.parametrize(
        ("value", "casted_value", "value_type"),
        [
            ("1234", 1234, int),
            ("test", "test", str),
            ("false", False, bool),
            ("true", True, bool),
            ("123.35", 123.35, float),
            # ('',None,None)
        ],
        ids=["'1234' to 1234", "'test' to 'test'", "'false' to False", "'true' to True", "'123.35' to 123.35"],
    )
    def test_cast_type(self, value, casted_value, value_type):
        result = self._cast_type(value)
        assert isinstance(result, value_type) is True
        assert result == casted_value

    @pytest.mark.parametrize(
        ("length", "include_special"),
        [(None, None), (5, None), (100, None), (10, True)],
        ids=[
            "_random_string: None -> return unique 10 character alphanumeric string",
            "_random_string: 5 -> return unique 5 character alphanumeric string",
            "_random_string: 100 -> return unique 100 character alphanumeric string",
            "_random_string: 10 (include_special) -> return unique 10 character alphanumeric+special string",
        ],
    )
    def test_random_string(self, length, include_special):
        result_a = self._random_string(length, include_special)
        result_b = self._random_string(length, include_special)

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
