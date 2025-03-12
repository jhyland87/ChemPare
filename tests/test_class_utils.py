# trunk-ignore-all(isort)
#!/usr/bin/env python3
import os
import sys
import pytest

# from assertions import assert_
# from assertions.operators import Operators

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from class_utils import ClassUtils


class TestClass(ClassUtils, object):
    @pytest.mark.parametrize(
        ("value", "price", "currency","currency_code"),
        [
            ("$123.45", "123.45", "$","USD"),
            ("$12,345.45", "12,345.45", "$","USD"),
            ("123.45 USD", "123.45", "$","USD"),
            ("123.45 CAD", "123.45", "CA$", "CAD"),
            ("€1,1234.5", "1,1234.5", "€", "EUR"),
            ("£123", "123", "£", "GBP"),
            ("674 ¥", "674", "¥","JPY"),
        ],
        ids=["_parse_price: '$123.45' -> $123.45 USD",
             "_parse_price: '$12,345.45' -> $12,345.45 USD",
             "_parse_price: '123.45 USD' -> $123.45 USD",
             "_parse_price: '123.45 CAD' -> $123.45 CAD",
             "_parse_price: '€1,1234.5' -> €1,1234.5 EUR",
             "_parse_price: '£123' -> £123 GBP",
             "_parse_price: '674 ¥' -> 674 ¥ JPY"],
    )
    def test_parse_price(self, value, price, currency, currency_code):
        result = self._parse_price(value)
        assert type(result) is dict
        assert "currency" in result
        assert "price" in result
        assert "currency_code" in result
        assert result["currency"] == currency
        assert result["price"] == price
        assert result["currency_code"] == currency_code
        # assert_( type(result) is list, what='result', operator=Operators.TRUTH)
        # assert_('currency', result, what='currency', operator=Operators.CONTAINS)
        # assert_('price', result, what='price', operator=Operators.CONTAINS)

    @pytest.mark.parametrize(
        ("value", "quantity", "uom"),
        [
            ("1 ounce", "1", "ounce"),
            ("43 ounces", "43", "ounces"),
            ("1 lb", "1", "lb"),
            ("4 lbs", "4", "lbs"),
            ("5 g", "5", "g"),
            ("10 gal", "10", "gal"),
            ("43.56 qt", "43.56", "qt"),
            ("10L", "10", "L"),
            ("5 l", "5", "l"),
            ("123.45mm", "123.45", "mm"),
            ("100 millimeters", "100", "millimeters"),
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
            "_parse_quantity: '5 l' -> 5 l",
            "_parse_quantity: '123.45mm' -> 123.45 mm",
            "_parse_quantity: '100 millimeters' -> 100 millimeters"
        ]
    )
    def test_parse_quantity(self, value, quantity, uom):
        result = self._parse_quantity(value)

        if type(result) is not dict:
            pytest.fail(f"_parse_quantity({value}) returned non-dict type")
            return

        if "quantity" not in result:
            pytest.fail(f'_parse_quantity({value}) missing "quantity" key')
        elif result["quantity"] != quantity:
            pytest.fail(f"_parse_quantity({value}) quantity mismatch")

        if "uom" not in result:
            pytest.fail(f'_parse_quantity({value}) missing "uom" key')
        elif result["uom"] != uom:
            pytest.fail(f"_parse_quantity({value}) uom mismatch")

    @pytest.mark.parametrize(
        ("value, param_name, expected_result"),
        [
            (
                "http://google.com?foo=bar&product_id=12345",
                None,
                {"foo": "bar", "product_id": "12345"},
            ),
            ("http://google.com?foo=bar&product_id=12345", "product_id", "12345"),
        ],
        ids=["no param_name", "with param_name"],
    )
    def test_get_param_from_url(self, value, param_name, expected_result):
        result = self._get_param_from_url(value, param_name)

        if type(result) is not type(expected_result):
            pytest.fail(
                f"type of result ({type(result)}) does not match expected result type ({type(expected_result)})"
            )
        elif result != expected_result:
            pytest.fail(f"result is not identical to expected reslt")

    @pytest.mark.parametrize(
        ("array", "expected_result"),
        [
            (["Variant", "500 g", "CAS", "1762-95-4"], [["Variant", "500 g"], ["CAS", "1762-95-4"]]),
            (["name", "23", "address"], [["name", "23"], ["address"]]),
        ]
    )
    def test_split_array_into_groups(self, array, expected_result):
        result = self._split_array_into_groups(array)

        if type(result) is not type(expected_result):
            pytest.fail(f'expected type "{type(expected_result)}" for result, but got "{type(result)}')

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
            ([["foo", "bar"], ["baz", "quux"]], {"foo": "bar", "baz": "quux"}),
        ]
    )
    def test_nested_arr_to_dict(self, array, expected_result):
        result = self._nested_arr_to_dict(array)
        assert type(result) is dict
        assert result == expected_result

    def test_epoch(self):
        result = self._epoch
        assert type(result) is int

    @pytest.mark.parametrize(
        ("char", "is_currency"),
        [
            ("$", True),
            ("¥", True),
            ("£", True),
            ("€", True),
            ("₽", True),
            ("A", False),
            ("Test", False),
        ],
        ids=["_is_currency('$') is True",
             "_is_currency('¥') is True",
             "_is_currency('£') is True",
             "_is_currency('€') is True",
             "_is_currency('₽') is True",
             "_is_currency('A') is False",
             "_is_currency('Test') is False"
        ],
    )
    def test_is_currency_symbol(self, char, is_currency):
        result = self._is_currency_symbol(char)
        assert type(result) is bool
        assert result is is_currency

    @pytest.mark.parametrize(
        ("cas", "valid_cas"),
        [
            ("7732-18-5", True),
            ("7664-93-9", True),
            ("123-34-34", False),
            ("321-2-1", False),
            ("a-1-333", False),
        ],
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
        assert type(result) is bool
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
        [
            ("$", "USD"),
            ("₽", "RUB"),
            ("€", "EUR"),
            ("£", "GBP"),
            ("¥", "JPY"),
            ("ABCD", None),
        ],
        ids=[
            "$ is USD",
            "₽ is RUB",
            "€ is EUR",
            "£ is GBP",
            "¥ is JPY",
            "ABCD is None",
        ],
    )
    def test_currency_code_from_symbol(self, symbol, expected_result):
        result = self._currency_code_from_symbol(symbol)
        assert type(result) is type(expected_result)
        if expected_result is None:
            assert result is None
        else:
            assert result == expected_result

    @pytest.mark.parametrize(
        ("code", "expected_result"),
        [
            ("USD", "$"),
            ("RUB", "₽"),
            ("EUR", "€"),
            ("GBP", "£"),
            ("JPY", "¥"),
            ("ABCD", None),
        ],
        ids=[
            "USD is $",
            "RUB is ₽",
            "EUR is €",
            "GBP is £",
            "JPY is ¥",
            "ABCD is None",
        ],
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
        ids=[
            "'1234' to 1234",
            "'test' to 'test'",
            "'false' to False",
            "'true' to True",
            "'123.35' to 123.35",
        ],
    )
    def test_cast_type(self, value, casted_value, value_type):
        result = self._cast_type(value)
        assert type(result) is value_type
        assert result == casted_value

    @pytest.mark.parametrize(
        ("length"),
        [
            (None),
            (5),
            (100),
        ],
        ids=[
            "_random_string: None -> return unique 10 character string",
            "_random_string: 5 -> return unique 5 character string",
            "_random_string: 100 -> return unique 100 character"
        ],
    )
    def test_random_string(self, length):
        result_a = self._random_string(length)
        result_b = self._random_string(length)
        assert type(result_a) is str
        assert type(result_b) is str
        assert len(result_a) == length or 10
        assert len(result_b) == length or 10
        assert result_a != result_b

    @pytest.mark.parametrize(
        ("value", "expected_result"),
        [
            ({"foo": 123, "bar": 555}, {"bar": 555}),
            ({"foo": 999999, "bar": 123}, {"foo": 999999}),
        ],
        ids=["Pulling bar from object", "Pulling foo from object"],
    )
    def test_filter_highest_value(self, value, expected_result):
        result = self._filter_highest_value(value)
        assert result == expected_result

    @pytest.mark.parametrize(
        ("phrases", "expected_result"),
        [
            ([
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
            ],{("atomic",): 2, ("oxygen",): 4}),
        ],
        ids=["Parse array of phrases"],
    )
    def test_get_common_phrases(self, phrases, expected_result):
        result = self._get_common_phrases(
            phrases
        )
        assert type(result) is dict
        assert result == expected_result
