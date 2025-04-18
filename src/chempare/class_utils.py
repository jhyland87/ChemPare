"""Utility class meant to provide functionality to any inheriting classes"""

import logging
import math
import os

# import sys
import random
import re
import string
import time
from decimal import ROUND_HALF_UP
from decimal import Decimal
from typing import Any
from typing import Dict
from typing import List
from urllib.parse import parse_qs
from urllib.parse import urlparse

import regex
from abcplus import ABCMeta
from abcplus import finalmethod
from currex import CURRENCIES
from currex import Currency
from datatypes import DecimalLike
from datatypes import TypePrice
from datatypes import TypeQuantity
from price_parser import Price


# import chempare

__package__ = "chempare"
__name__ = "chempare.class_utils"

_logger = logging.getLogger("chempare/class_utils")
logging.basicConfig(level=os.environ.get("LOG_LEVEL", "WARNING"))


class ClassUtils(metaclass=ABCMeta):
    """Utility class meant to provide functionality to any inheriting classes"""

    @property
    @finalmethod
    def _epoch(self) -> int:
        """Get epoch string - Used for unique values in searches (sometimes _)

        Returns:
            int: Current time in epoch
        """

        return math.floor(time.time() * 1000)

    @finalmethod
    def _parse_price(self, value: str, symbol_to_code: bool = True) -> TypePrice | None:
        """Parse a string for a price value (currency and value)

        Args:
            value (str): String with price
            symbol_to_code (bool): Attempt to convert the currency symbols to
                                   country codes if this is set to True
                                   (defaults to True)

        Returns:
            TypePrice: Returns a dictionary with 'currency' and 'price' values

        See:
            https://en.wikipedia.org/wiki/Currency_symbol

        Todo:
            - Need to deal with:
                A symbol may be positioned in various ways, according to
                national convention: before, between or after the
                numeric amounts: €2.50, 2,50€ and 2$50 with two vertical lines.
        """

        # if chempare.called_from_test is True:
        #     print(
        #         "\n\n\nchempare.called_from_test:",
        #         chempare.called_from_test,
        #         "\n\n\n",
        #     )

        iso_4217_pattern = (
            r"(?:ab\s?)?(?:(?P<currency>[\p{Sc}ƒ]|"
            r"(?P<currency>"
            r"A(?:[EM]D|[FZ]N|LL|[NW]G|OA|RS|U[D\$]?)|"
            r"B(?:AM|[BHMNZS]D|DT|[GT]N|IF|OB|RL|WP|YR)|"
            r"C(?:A[D$]|[DH]F|[LOU]P|NY|[RU]C|VE|ZK)|"
            r"D(?:JF|KK|OP|ZD)|"
            r"E(?:GP|RN|TB|UR?)|"
            r"F(?:JD|KP)|"
            r"G(?:[BGI]P|EL|HS|[YM]D|NF|TQ)|"
            r"H(?:KD|NL|RK|TG|UF)|"
            r"I(?:[NRD]R|LS|MP|QD|SK)|"
            r"J(?:EP|MD|OD|PY)|"
            r"K(?:[GE]S|HR|MF|[PR]W|[WY]D|ZT)|"
            r"L(?:AK|BP|KR|[RY]D|SL)|"
            r"M(?:[AK]D|DL|GA|[MW]K|NT|OP|RO|[UVY]R|[XZ]N)|"
            r"N(?:[AZ]D|GN|IO|OK|PR)|"
            r"(?:QA|OM|YE)R|"
            r"P(?:AB|[EKL]N|GK|HP|KR|YG)|"
            r"R(?:ON|SD|UB|WF)|"
            r"S(?:[AC]R|[BRGDT]D|DG|EK|[HY]P|[LZP]L|OS|VC)|"
            r"T(?:HB|[JZ]S|MT|[NTVW]D|OP|RY)|"
            r"U(?:AH|GX|SD?|YU|ZS)|"
            r"V(?:EF|ND|UV)|WST|"
            r"X(?:[AOP]F|CD|DR)|"
            r"Z(?:AR|MW|WD)))?"
            r"\s?(?P<price>[0-9]+(?:[,\.][0-9]+)*)"
            r"|(?P<price>[0-9]+(?:[,\.][0-9]+)*)\s?(?P<currency>[\p{Sc}ƒ]|"
            # r"(?:us|au|ca)d?|eur?|chf|rub|gbp|jyp|pln|sek|uah|hrk)"
            r"(?P<currency>"
            r"A(?:[EM]D|[FZ]N|LL|[NW]G|OA|RS|U[D\$]?)|"
            r"B(?:AM|[BHMNZS]D|DT|[GT]N|IF|OB|RL|WP|YR)|"
            r"C(?:AD|[DH]F|[LOU]P|NY|[RU]C|VE|ZK)|"
            r"D(?:JF|KK|OP|ZD)|"
            r"E(?:GP|RN|TB|UR?)|"
            r"F(?:JD|KP)|"
            r"G(?:[BGI]P|EL|HS|[YM]D|NF|TQ)|"
            r"H(?:KD|NL|RK|TG|UF)|"
            r"I(?:[NRD]R|LS|MP|QD|SK)|"
            r"J(?:EP|MD|OD|PY)|"
            r"K(?:[GE]S|HR|MF|[PR]W|[WY]D|ZT)|"
            r"L(?:AK|BP|KR|[RY]D|SL)|"
            r"M(?:[AK]D|DL|GA|[MW]K|NT|OP|RO|[UVY]R|[XZ]N)|"
            r"N(?:[AZ]D|GN|IO|OK|PR)|"
            r"(?:QA|OM|YE)R|"
            r"P(?:AB|[EKL]N|GK|HP|KR|YG)|"
            r"R(?:ON|SD|UB|WF)|"
            r"S(?:[AC]R|[BRGDT]D|DG|EK|[HY]P|[LZP]L|OS|VC)|"
            r"T(?:HB|[JZ]S|MT|[NTVW]D|OP|RY)|"
            r"U(?:AH|GX|SD?|YU|ZS)|"
            r"V(?:EF|ND|UV)|WST|"
            r"X(?:[AOP]F|CD|DR)|"
            r"Z(?:AR|MW|WD)))"
            r")?"
        )

        matches = regex.match(iso_4217_pattern, value, regex.IGNORECASE)
        if not matches:
            return None

        matches_str = matches.group()
        price = Price.fromstring(matches_str)
        currency_code = self._currency_code_from_symbol(price.currency)

        result = {
            "currency": price.currency,
            "price": float(price.amount),
            "currency_code": currency_code or price.currency,
        }

        if currency_code != "USD" and price.currency is not None and price.currency != currency_code:
            usd_price = self._to_usd(from_currency=currency_code, amount=float(price.amount))
            if usd_price:
                result["usd"] = usd_price

        return TypePrice(**result)

    @finalmethod
    def _to_usd(self, from_currency: str | None = None, amount: int | float | str | None = None) -> DecimalLike | None:
        """Convert a no USD price to the USD price

        Args:
            from_currency (str, optional): Currency the price currently is in.
                                           Defaults to None.
            amount (Union[int, float, str], optional): Amount/price to convert.
                                                       Defaults to None.

        Raises:
            Exception: If amount is string that is not parseable
            TypeError: Invalid from_currency value/type
            TypeError: No amount provided

        Returns:
            Optional[float]: USD price (if one was found)

        Example:
            >>> self._to_usd()
        """

        # try:

        # If no source currency type is provided, but we were given a string for the amount, then it may include
        # the currency type (eg: "$123.23"), and can be parsed
        if from_currency is None and isinstance(amount, str) is True:
            parsed_price = self._parse_price(amount)  # type: ignore
            if not isinstance(parsed_price, Dict):
                _logger.debug(
                    "Unable to determine from currency from amount %s of type %s (expected Dict)",
                    parsed_price,
                    type(parsed_price),
                )
                return None

            from_currency = parsed_price.currency_code
            amount = parsed_price.price

        # If there is no from_currency (either provided as a parameter or set using _parse_price), then throw
        # an exception
        if not from_currency or isinstance(from_currency, str) is False:
            _logger.debug(
                "Source currency '%s' (type %s) either not provided or wrong type", from_currency, type(from_currency)
            )
            return None

        from_currency = from_currency.upper()

        if from_currency not in CURRENCIES:
            # raise LookupError(f"Unable to convert from '{from_currency}")
            return None

        amount = self._cast_type(amount)

        if not isinstance(amount, DecimalLike):
            _logger.debug("Amount of '%s' is either invalid type or not provided (%s)", amount, type(amount))

        # if not amount:
        #     raise ValueError("No amount provided or found")

        # if isinstance(amount, int) is Falseand isinstance(amount, float) is False
        #      raise TypeError("amount needs to be float or int")

        from_currency_obj = Currency(from_currency, amount)  # type: ignore

        usd = from_currency_obj.to("USD")

        # return self._to_hundreths(usd.amount)
        return round(float(usd.amount), 2)
        # except Exception as err:
        #     # print("Exception:", err)
        #     return None

    def _to_hundreths(self, value: DecimalLike | str) -> Decimal:
        """Convert any number like value to include the hundreths place

        Args:
            value (DecimalLike | str): Value to convert

        Returns:
            Decimal: Equivelant value with hundreths.

        Example:
            >>> self._to_hundreths("123")
            '123.00'
            >>> self._to_hundreths("123.456")
            '123.45'
            >>> self._to_hundreths(123.456)
            '123.45'
            >>> self._to_hundreths(123)
            '123.00'
            >>> self._to_hundreths(Decimal("123.1"))
            '123.10'
        """
        if not isinstance(value, Decimal):
            value = Decimal(value)

        return value.quantize(Decimal("0.00"), ROUND_HALF_UP)

    # def _to_usd(
    #     self, from_currency: str = None, amount: Union[int, float, str] = None
    # ) -> Optional[float]:
    #     try:
    #         if not from_currency and type(amount) is str:
    #             parsed_price = self._parse_price(amount)
    #             if not parsed_price:
    #                 raise Exception(
    #                     "Unable to determine from currency from amount"
    #                 )

    #             from_currency = parsed_price["currency_code"]
    #             amount = parsed_price["price"]

    #         if not from_currency or isinstance(from_currency, str) is False
    #             raise TypeError("from_currency not provided or not string")

    #         from_currency = from_currency.upper()
    #         if from_currency not in CURRENCIES:
    #             print(f"Unable to convert from '{from_currency}'")
    #             # raise LookupError(f"Unable to convert from '{from_currency}")
    #             return None

    #         if not amount:
    #             raise TypeError("No amount provided or found")

    #         # if isinstance(amount, int) is Falseand isinstance(amount, float) is False
    #         #      raise TypeError("amount needs to be float or int")

    #         from_currency_obj = Currency(from_currency, amount)
    #         return from_currency_obj.to("USD")
    #     except Exception as err:
    #         print("Exception:", err)
    #         return

    @finalmethod
    def _parse_quantity(self, value: str) -> TypeQuantity | None:
        """Parse a string for the quantity and unit of measurement

        Args:
            value (str): Suspected quantity string

        Returns:
            Optional[TypeQuantity]: Returns a dictionary with the 'quantity' and
                            'uom' values
        """

        # When a UOM is found, its lower case key can be used to look up the
        # correct case format for it. If the UOM is in one of the below tuple
        # keys, then it's substituted with the value.
        uom_cases = {
            ("liter", "liters", "litres", "l"): "L",
            ("ml", "mls", "millilitre", "millilitres", "milliliter", "milliliters"): "mL",
            ("g", "gram", "grams"): "g",
            ("lb", "lbs", "pound", "pounds"): "lb",
            ("kg", "kgs", "killogram", "killograms"): "kg",
            ("mm", "millimeter", "millimeters", "millimetre", "millimetres"): "mm",
            ("cm", "centimeter", "centimeters", "centimetre", "centimetres"): "cm",
            ("m", "meter", "meters", "metre", "metres"): "m",
            ("oz", "ounce", "ounces"): "oz",
            ("gal", "gallon", "gallons"): "gal",
            ("qt", "quart", "quarts"): "qt",
        }

        if isinstance(value, str) is False:
            return None

        value = value.strip()

        if not value or value.isspace():
            return None

        # https://regex101.com/r/lDLuVX/4
        pattern = (
            r"(?P<quantity>[0-9][0-9\.\,]*)\s?"
            r"(?P<uom>(?:milli|kilo|centi)"
            r"(?:gram|meter|liter|metre)s?|z|ounces?|grams?|gallon|gal"
            r"|kg|g|lbs?|pounds?|l|qt|m?[glm])"
        )

        matches = regex.search(pattern, value, regex.IGNORECASE)

        if not matches:
            return None

        quantity_obj = matches.groupdict()

        # Look for any proper substitution UOM's
        proper_uom = self._find_values_with_element(uom_cases, str(quantity_obj["uom"]).lower())

        if len(proper_uom) > 0:
            quantity_obj["uom"] = proper_uom[0]

        return TypeQuantity(**quantity_obj)

    @finalmethod
    def _get_param_from_url(self, url: str, param: str | None = None) -> Any | None:
        """Get a specific arameter from a GET URL

        Args:
            url (str): HREF address
            param (str): Param key to find (optional)

        Returns:
            Any: Whatver the value was of the key, or nothing

        Example:
            >>> self._get_param_from_url(
            ...    'http://google.com?foo=bar&product_id=12345'
            ... )
            {'foo':'bar','product_id':'12345'}
            >>> self._get_param_from_url(
            ...    'http://google.com?foo=bar&product_id=12345', 'product_id'
            ... )
            '12345'
        """

        parsed_url = urlparse(url)
        parsed_query = parse_qs(parsed_url.query)

        # Replace any ['values'] with just 'values'
        parsed_query = {k: v[0] if len(v) == 1 else v for k, v in parsed_query.items()}

        if not param:
            return parsed_query

        # If no specific parameter was defined, then just return this
        if param not in parsed_query:
            return None

        if not parsed_query[param]:
            return None

        return parsed_query[param]

    @finalmethod
    def _split_array_into_groups(self, arr: List, size: int = 2) -> List:
        """Splits an array into sub-arrays of 2 elements each.

        Args:
            arr: The input array.
            size: Size to group array elements by

        Returns:
            A list of sub-arrays, where each sub-array contains {size} elements,
            or an empty list if the input array is empty.

        Example:
            >>> self._split_array_into_groups([
            ...    'Variant', '500 g', 'CAS', '1762-95-4'
            ... ])
            [['Variant', '500 g'],['CAS', '1762-95-4']]
        """

        result = []
        for i in range(0, len(arr), size):
            result.append(arr[i : i + size])

        return result

    @finalmethod
    def _nested_arr_to_dict(self, arr: List[List]) -> Dict | None:
        """Takes an array of arrays (ie: result from
        self._split_array_into_groups) and converts that into a dictionary.

        Args:
            arr (List[List]): The input array.

        Returns:
            Optional[Dict]: A dictionary based off of the input alues

        Example:
            >>> self._nested_arr_to_dict([["foo","bar"], ["baz","quux"]])
            {'foo':'bar','baz":'quux"}
        """

        # Only works if the array has even amount of elements
        if len(arr) % 2 != 0:
            return None

        grouped_elem = self._split_array_into_groups(arr, 2)
        variant_dict = [dict(item) for item in grouped_elem]

        return variant_dict[0] or None

    @finalmethod
    def _is_currency_symbol(self, char: str) -> bool:
        """Determines if a value is a currency symbol or not

        Args:
            char (str): Value to analyze

        Returns:
            bool: True if it's a currency symbol

        Example:
            >>> self._is_currency_symbol("$")
            True
            >>> self._is_currency_symbol("foo")
            False
        """

        # Use Pythons nifty \p{Sc} pattern to make sure the value given is
        # actually a currency symbol
        return bool(regex.match(r"\p{Sc}", char, regex.IGNORECASE))

    @finalmethod
    def _currency_code_from_symbol(self, symbol: str) -> str | None:
        """Attempt to get the currency code for a given currency symbol

        Source:
            https://www.eurochange.co.uk/travel/tips/world-currency-abbreviations-symbols-and-codes-travel-money

        Args:
            symbol (str): Currency symbol (eg: $, ¥, £, etc)

        Returns:
            Optional[str]: The currency code, if one is found

        Example:
            >>> self._currency_code_from_symbol("$")
            'USD"
        """

        if isinstance(symbol, str) is False:
            return None

        symbol = symbol.strip()

        # Use Pythons nifty \p{Sc} pattern to make sure the value given is
        # actually a currency symbol
        # if not self._is_currency_symbol(symbol):
        #     print(f"The symbol {symbol} does not match SC pattern")
        #     return None

        currency_codes = {
            "Lek": "ALL",
            "؋": "AFN",
            "$": "USD",
            "CA$": "CAD",
            "ƒ": "ANG",
            "₼": "AZN",
            "Br": "BYN",
            "BZ$": "BZD",
            "$b": "BOB",
            "KM": "BAM",
            "P": "BWP",
            "лв": "UZS",
            "R$": "BRL",
            "៛": "KHR",
            "¥": "JPY",
            "₡": "CRC",
            "₱": "PHP",
            "Kč": "CZK",
            "kr": "SEK",
            "RD$": "DOP",
            "£": "GBP",
            "€": "EUR",
            "¢": "GHS",
            "Q": "GTQ",
            "L": "HNL",
            "Ft": "HUF",
            "₹": "INR",
            "Rp": "IDR",
            "﷼": "YER",
            "₪": "ILS",
            "J$": "JMD",
            "₩": "KRW",
            "₭": "LAK",
            "ден": "MKD",
            "RM": "MYR",
            "AU$": "AUD",
            "₨": "LKR",
            "₮": "MNT",
            " د.إ": "AED",
            "MT": "MZN",
            "C$": "NIO",
            "₦": "NGN",
            "B/.": "PAB",
            "Gs": "PYG",
            "S/.": "PEN",
            "zł": "PLN",
            "lei": "RON",
            "₽": "RUB",
            "Дин.": "RSD",
            "S": "SOS",
            "R": "ZAR",
            "CHF": "CHF",
            "NT$": "TWD",
            "฿": "THB",
            "TT$": "TTD",
            "₺": "TRY",
            "₴": "UAH",
            "$U": "UYU",
            "Bs": "VEF",
            "₫": "VND",
            "Z$": "ZWD",
            # "€ab": "???",
        }

        return currency_codes.get(symbol, None)

    @finalmethod
    def _currency_symbol_from_code(self, code: str) -> str | None:

        if isinstance(code, str) is False:
            return None

        code = code.strip().upper()
        # code = code.upper()

        currency_symbols = {
            "ALL": "Lek",
            "AFN": "؋",
            "ARS": "$",
            "AWG": "ƒ",
            "AUD": "AU$",
            "AZN": "₼",
            "BSD": "$",
            "BBD": "$",
            "BYN": "Br",
            "BZD": "BZ$",
            "BMD": "$",
            "BOB": "$b",
            "BAM": "KM",
            "BWP": "P",
            "BGN": "лв",
            "BRL": "R$",
            "BND": "$",
            "KHR": "៛",
            "CAD": "CA$",
            "KYD": "$",
            "CLP": "$",
            "CNY": "¥",
            "COP": "$",
            "CRC": "₡",
            "CUP": "₱",
            "CZK": "Kč",
            "DKK": "kr",
            "DOP": "RD$",
            "XCD": "$",
            "EGP": "£",
            "SVC": "$",
            "EUR": "€",
            "FKP": "£",
            "FJD": "$",
            "GHS": "¢",
            "GIP": "£",
            "GTQ": "Q",
            "GGP": "£",
            "GYD": "$",
            "HNL": "L",
            "HKD": "$",
            "HUF": "Ft",
            "ISK": "kr",
            "INR": "₹",
            "IDR": "Rp",
            "IRR": "﷼",
            "IMP": "£",
            "ILS": "₪",
            "JMD": "J$",
            "JPY": "¥",
            "JEP": "£",
            "KZT": "лв",
            "KPW": "₩",
            "KRW": "₩",
            "KGS": "лв",
            "LAK": "₭",
            "LBP": "£",
            "LRD": "$",
            "MKD": "ден",
            "MYR": "RM",
            "MUR": "₨",
            "MXN": "$",
            "MNT": " د.إ",
            "MZN": "MT",
            "NAD": "$",
            "NPR": "₨",
            "ANG": "ƒ",
            "NZD": "$",
            "NIO": "C$",
            "NGN": "₦",
            "NOK": "kr",
            "OMR": "﷼",
            "PKR": "₨",
            "PAB": "B/.",
            "PYG": "Gs",
            "PEN": "S/.",
            "PHP": "₱",
            "PLN": "zł",
            "QAR": "﷼",
            "RON": "lei",
            "RUB": "₽",
            "SHP": "£",
            "SAR": "﷼",
            "RSD": "Дин.",
            "SCR": "₨",
            "SGD": "$",
            "SBD": "$",
            "SOS": "S",
            "ZAR": "R",
            "LKR": "₨",
            "SEK": "kr",
            "CHF": "CHF",
            "SRD": "$",
            "SYP": "£",
            "TWD": "NT$",
            "THB": "฿",
            "TTD": "TT$",
            "TRY": "₺",
            "TVD": "$",
            "UAH": "₴",
            "AED": " د.إ",
            "GBP": "£",
            "USD": "$",
            "UYU": "$U",
            "UZS": "лв",
            "VEF": "Bs",
            "VND": "₫",
            "YER": "﷼",
            "ZWD": "Z$",
        }

        if code in currency_symbols:
            return currency_symbols[code]

    @finalmethod
    def _cast_type(self, value: str | int | float | bool | None = None) -> Any:
        """Cast a value to the proper type. This is mostly used for casting
        int/float/bool

        Args:
            value (Union[str,int,float,bool]): Value to be casted (optional)

        Returns:
            Any: Casted value
        """

        # If it's not a string, then its probably a valid type..
        if isinstance(value, str) is False:
            return value

        # Most castable values just need to be trimmed to be compatible
        value = value.strip()

        if not value or value.isspace():
            return None

        if value.lower() == "true":
            return True

        if value.lower() == "false":
            return False

        try:
            return int(value)
        except Exception:
            pass

        try:
            return float(value)
        except Exception:
            pass

        return value

        # if not value.isdecimal() or re.match(r'^[0-9]+.[0-9]+$', value):
        #     return float(value)

        # if value.isnumeric() or re.match(r'^[0-9]+$', value):
        #     return int(value)

        # return value

    @finalmethod
    def _random_string(self, max_length: int = 10, include_special: bool = False) -> str:
        """Generate random string

        Args:
            max_length (int, optional): Length to generate string to. Defaults to 10
            include_special (bool, optional): Include special chars in output.
                                              Defaults to False

        Returns:
            str: Random string, {len} chars long
        """
        if isinstance(max_length, int) is False:
            max_length = 10

        # ascii_letters = abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
        # digits = 0123456789
        # punctuation = !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~
        char_list = string.ascii_letters + string.digits

        if include_special is True:
            char_list += string.punctuation

        # trunk-ignore(bandit/B311)
        return "".join(random.choice(char_list) for _ in range(max_length))

    @finalmethod
    def _find_cas(self, value: str) -> str | None:
        """Parse a string for CAS values, return the first valid one

        Args:
            value (str): String content with possible CAS issues

        Returns:
            Optional[str]: First valid CAS number, or nothing
        """

        matches = re.findall(r"([0-9]{2,7}-[0-9]{2}-[0-9])", value)

        for m in matches:
            if not self._is_cas(m):
                continue

            return m

    @finalmethod
    def _is_cas(self, value: Any) -> bool:
        """Check if a string is a valid CAS registry number

        CAS numbers are always in a format of three segments of numerical values:
            1234-56-6

        The first segment can be from 2 to 7 intigers (needs to be at least one non-zero value),
        and the second is always 2 integers. These are basically just unique numbers, but there's no
        established numbering system or other restrictions.
        The third segment is one integer, and that is the checksum of the first two segments.

        https://regex101.com/r/xPF1Yp/2
        (?P<seg_a>[0-9]{2,7})-(?P<seg_b>[0-9]{2})-(?P<checksum>[0-9])

        The checksum is calculated by taking the first two segments and iterating over each
        individual intiger in reverse order, multiplying each by its position, then taking
        the modulous of the sum of those values.

        For example, 1234-56-6 is valid because the result of the below equation matches the checksum, (which is 6)
            (6*1 + 5*2 + 4*3 + 3*4 + 2*5 + 1*6) % 10 == 6

        This can be simplified in the below aggregation:
            cas_chars = [1, 2, 3, 4, 5, 6]
            sum([(idx+1)*int(n) for idx, n
                in enumerate(cas_chars[::-1])]) % 10

        See:
            https://www.cas.org/training/documentation/chemical-substances/checkdig
            https://www.allcheminfo.com/chemistry/cas-number-lookup.html

        Args:
            value (str): The value to determine if its a CAS # or not

        Returns:
            bool: True if its a valid format and the checksum matches

        Example:
            >>> self._is_cas("1234-56-6")
            True
            >>> self._is_cas("50-00-0")
            True
            >>> self._is_cas("1234-56-999")
            False
            >>> self._is_cas("1234-56")
            False
            >>> self._is_cas("1234-56-0")
            False
            >>> self._is_cas("0000-00-0")
            False
            >>> self._is_cas("00-10-0")
            False
        """

        if isinstance(value, str) is False:
            return False

        # value='1234-56-6'
        # https://regex101.com/r/xPF1Yp/2
        cas_pattern_check = re.match(r"^(?P<seg_a>[0-9]{2,7})-(?P<seg_b>[0-9]{2})-(?P<checksum>[0-9])$", value)

        if cas_pattern_check is None:
            return False

        cas_dict = cas_pattern_check.groupdict()
        # cas_dict = dict(seg_a="1234", seg_b="56", checksum="6")

        if int(cas_dict["seg_a"]) == 0:
            return False

        cas_chars = list(cas_dict["seg_a"] + cas_dict["seg_b"])
        # cas_chars = ["1","2","3","4","5","6"]

        checksum = sum([(idx + 1) * int(n) for idx, n in enumerate(cas_chars[::-1])]) % 10
        # checksum = 6

        return int(checksum) == int(cas_dict["checksum"])

    @finalmethod
    def _filter_highest_item_value(self, input_dict: Dict) -> Dict:
        """Filter a dictionary for the entry with the highest numerical value.

        Args:
            input_dict (Dict): Dictionary to iterate through

        Returns:
            Dict: Item in dictionary with highest value

        Example:
            >>> self._filter_highest_item_value({"foo": 123, "bar": 555})
            {'bar": 555}
            >>> self._filter_highest_item_value({"foo": 999999, "bar": 123})
            {'foo": 999999}
        """

        if not input_dict:
            return {}
        max_value = max(input_dict.values())
        return {k: v for k, v in input_dict.items() if v == max_value}

    @finalmethod
    def _get_common_phrases(
        self, texts: list, maximum_length: int = 3, minimum_repeat: int = 2, stopwords: list | None = None
    ) -> dict:
        """Get the most common phrases out of a list of phrases.

        This is used to analyze the results from a query to
        https://cactus.nci.nih.gov/chemical/structure/{NAME OR CAS}/names to
        find the most common term used in the results. This term may yield
        better search results on some sites.

        Source:
            https://dev.to/mattschwartz/quickly-find-common-phrases-in-a-large-list-of-strings-9in

        Args:
            texts (list): Array of text values to analyze
            maximum_length (int, optional): Max length of phrse. Defaults to 3.
            minimum_repeat (int, optional): Min length of phrse. Defaults to 2.
            stopwords (list, optional): Phrases to exclude. Defaults to [].

        Returns:
            dict: Dictionary of sets of words and the frequency as the value.
        """

        stopwords = stopwords or []
        phrases = {}
        for text in texts:
            # Replace separators and punctuation with spaces
            text = re.sub(r"[.!?,:;/\-\s]", " ", text)
            # Remove extraneous chars
            text = re.sub(r"[\\|@#$&~%\(\)*\"]", "", text)

            words = text.split(" ")
            # Remove stop words and empty strings
            words = [w for w in words if len(w) and w.lower() not in stopwords]
            length = len(words)
            # Look at phrases no longer than maximum_length words long
            size = length if length <= maximum_length else maximum_length
            while size > 0:
                pos = 0
                # Walk over all sets of words
                while pos + size <= length:
                    phrase = words[pos : pos + size]
                    phrase = tuple(w.lower() for w in phrase)
                    if phrase in phrases:
                        phrases[phrase] += 1
                    else:
                        phrases[phrase] = 1
                    pos += 1
                size -= 1

        phrases = {k: v for k, v in phrases.items() if v >= minimum_repeat}

        longest_phrases = {}
        keys = list(phrases.keys())
        keys.sort(key=len, reverse=True)
        for phrase in keys:
            found = False
            for l_phrase in longest_phrases:
                intersection = set(l_phrase).intersection(phrase)
                if len(intersection) != len(phrase):
                    continue

                # If the entire phrase is found in a longer tuple...
                # ... and their frequency overlaps by 75% or more, we'll drop it
                difference = (phrases[phrase] - longest_phrases[l_phrase]) / longest_phrases[l_phrase]
                if difference < 0.25:
                    found = True
                    break
            if not found:
                longest_phrases[phrase] = phrases[phrase]

        return longest_phrases

    @finalmethod
    def _find_values_with_element(self, source: Dict, element: str | int | None) -> List:
        """
        Finds values in a dictionary that are tuples and contain a specific
        element.

        Args:
            source (Dict): The dictionary to search.
            element (str, int): The element to search for within the tuple keys

        Returns:
            List: A list of values that were found

        Example:
            >>> my_dict = {
            ...    (1, 2): "a",
            ...    (2, 3): "b",
            ...    (3, 4): "c",
            ...    "hello": "d",
            ...    (2, 5, 6): "e"
            ... }
            >>> self._find_values_with_element(my_dict, 1)
            ['a']
            >>> self._find_values_with_element(my_dict, 2)
            ['a', 'b', 'e']
            >>> self._find_values_with_element(my_dict, "hello")
            ['d']
        """

        return [
            source[key]
            for key in source
            if (isinstance(key, tuple) and element in key) or (isinstance(key, str) and element == key)
        ]

    @finalmethod
    def _split_set_cookie(self, set_cookie: str) -> list:
        return regex.split(r'(?<!Mon|Tue|Wed|Thu|Fri|Sat|Sun),\s?', set_cookie)

    @finalmethod
    def _parse_cookie(self, value: str) -> dict[str, Any] | None:
        """
        Get cookie name/value out of the full set-cookie header segment.

        Args:
            value (str): The set-cookie segment.

        See:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Set-Cookie

        Returns:
            dict[str, str]: The cookie info (name, value, attrs, etc)

        Example:
            >>> self._parse_cookie("ssr-caching=cache#desc=hit#varnish=hit_hit#dc#desc=fastly_g; max-age=20")
            {'name': 'ssr-caching', 'value': 'cache#desc=hit#varnish=hit_hit#dc#desc=fastly_g', 'max-age': '20'}
            >>> self._parse_cookie("client-session-bind=7435e070-c09e-4b97-9b70-b679273af80a; Path=/; Secure; SameSite=Lax;")
            {'name': 'client-session-bind', 'value': '7435e070-c09e-4b97-9b70-b679273af80a', 'path': '/', 'secure': True, 'samesite': 'Lax'
            >>> self._parse_cookie("server-session-bind=7435e070-c09e-4b97-9b70-b679273af80a; Path=/; Secure; SameSite=Lax; HttpOnly;")
            {'name': 'server-session-bind', 'value': '7435e070-c09e-4b97-9b70-b679273af80a', 'path': '/', 'secure': True, 'samesite': 'Lax', 'httponly': True}
        """

        cookie_matches = regex.match(
            r'^(?P<name>[a-zA-Z0-9_-]+)=(?P<value>[^;]+)(?:$|;\s)(?P<args>(.*)+)?$', value, regex.IGNORECASE
        )

        # print(cookie_matches.capturesdict())

        cookie_match_dict = cookie_matches.capturesdict()

        result = {"name": cookie_match_dict.get('name', [None])[0], "value": cookie_match_dict.get('value', [None])[0]}

        args = cookie_match_dict.get('args', [])[0].rstrip(';').split(';')

        cookie_args = {}

        for a in args:
            arg_segs = a.strip().split('=')
            if len(arg_segs) == 1:
                cookie_args[arg_segs[0].lower()] = True
                continue

            cookie_args[arg_segs[0].lower()] = arg_segs[1]

        result.update(cookie_args)

        return result


__all__ = ["ClassUtils"]
