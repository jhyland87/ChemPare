"""Utils class that can be extended by supplier modules"""

import logging
import math
import os
import random
import re
import string
import time
from typing import Any, Dict, List, NoReturn, Optional, Union
from urllib.parse import parse_qs, urlparse

import regex
from abcplus import ABCMeta, finalmethod

class ClassUtils(metaclass=ABCMeta):
    """Utility class - meant to be extended by Suppliers if needed"""

    _logger = None

    def _init_logging(self) -> NoReturn:
        """Create the logger specific to this class instance (child)

        Returns:
            NoReturn: None

        Note:
            Uses the LOG_LEVEL env var for the log level. Valid values are:
            CRITICAL FATAL ERROR WARNING INFO DEBUG. The default is WARNING
        """
        if hasattr(self, "_logger") is False or not self._logger:
            return

        self._logger = logging.getLogger(str(self.__class__.__name__))
        logging.basicConfig(level=os.environ.get("LOG_LEVEL", "WARNING"))

    def _log(self, message: str) -> NoReturn:
        """Create a regular log entry

        Args:
            message (str): Message to send to the logs

        Returns:
            NoReturn: None
        """
        if hasattr(self, "_logger") is False or not self._logger:
            return

        self._logger.log(logging.INFO, message)

    def _debug(self, message: str) -> NoReturn:
        """Create a debugger log entry

        Args:
            message (str): Message to send to the logs

        Returns:
            NoReturn: None
        """
        if hasattr(self, "_logger") is False or not self._logger:
            return

        self._logger.log(logging.DEBUG, message)

    def _error(self, message: str) -> NoReturn:
        """Create an error log entry

        Args:
            message (str): Message to send to the logs

        Returns:
            NoReturn: None
        """
        if hasattr(self, "_logger") is False or not self._logger:
            return

        self._logger.log(logging.ERROR, message)

    def _warn(self, message: str) -> NoReturn:
        """Create a warning log entry

        Args:
            message (str): Message to send to the logs

        Returns:
            NoReturn: None
        """
        if hasattr(self, "_logger") is False or not self._logger:
            return

        self._logger.log(logging.WARN, message)

        # CRITICAL = 50
        # FATAL = CRITICAL
        # ERROR = 40
        # WARNING = 30
        # WARN = WARNING
        # INFO = 20
        # DEBUG = 10
        # NOTSET = 0

    @property
    @finalmethod
    def _epoch(self) -> int:
        """Get epoch string - Used for unique values in searches (sometimes _)

        Returns:
            int: Current time in epoch
        """

        return math.floor(time.time() * 1000)

    @finalmethod
    def _parse_price(
        self, content: str, symbol_to_code: bool = True
    ) -> Optional[Dict]:
        """Parse a string for a price value (currency and value)

        Args:
            content (str): String with price
            symbol_to_code (bool): Attempt to convert the currency symbols to
                                   country codes if this is set to True
                                   (defaults to True)

        Returns:
            Dict: Returns a dictionary with 'currency' and 'price' values

        See:
            https://en.wikipedia.org/wiki/Currency_symbol

        Todo:
            - Need to deal with:
                A symbol may be positioned in various ways, according to
                national convention: before, between or after the
                numeric amounts: €2.50, 2,50€ and 2$50 with two vertical lines.
        """

        iso_4217_pattern = (
            r"(?:ab\s?)?(?:(?P<currency>\p{Sc}|"
            r"(?P<currency>"
            r"A(?:[EM]D|[FZ]N|LL|[NW]G|OA|RS|UD?)|"
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
            r"\s?(?P<price>[0-9]+(?:[,\.][0-9]+)*)"
            r"|(?P<price>[0-9]+(?:[,\.][0-9]+)*)\s?(?P<currency>\p{Sc}|"
            # r"(?:us|au|ca)d?|eur?|chf|rub|gbp|jyp|pln|sek|uah|hrk)"
            r"(?P<currency>"
            r"A(?:[EM]D|[FZ]N|LL|[NW]G|OA|RS|UD?)|"
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
            r")"
        )

        matches = regex.match(iso_4217_pattern, content, regex.IGNORECASE)
        if not matches:
            return None

        matches_dict = matches.groupdict()

        if self._is_currency_symbol(
            matches_dict["currency"]
        ):  # If the currency is a symbol
            matches_dict["currency_code"] = self._currency_code_from_symbol(
                matches_dict["currency"]
            )
        else:
            matches_dict["currency_code"] = matches_dict["currency"]
            matches_dict["currency"] = self._currency_symbol_from_code(
                matches_dict["currency_code"]
            )

        # If we are trying to convert the currency symbol to the country code,
        # then check that the "currency" matched is at least a currency symbol.
        # if symbol_to_code is True and self._is_currency_symbol(
        #     matches_dict["currency"]
        # ):
        #     # ... Then attempt to get the country code from it.
        #     country_code = self._currency_code_from_symbol(
        #         matches_dict["currency"]
        #     )
        #     if country_code:
        #         # If one was found, then override the "currency" property in
        #         # the result
        #         matches_dict["currency_code"] = country_code

        if matches_dict["currency_code"] in ["USD", "CAD", "EUR"]:
            price = str(matches_dict["price"]).replace(",", "")
            matches_dict["price"] = f"{float(price):.2f}"

        return matches_dict

    @finalmethod
    def _parse_quantity(self, content: str) -> Optional[Dict]:
        """Parse a string for the quantity and unit of measurement

        Args:
            content (str): Suspected quantity string

        Returns:
            Optional[Dict]: Returns a dictionary with the 'quantity' and
                            'uom' values
        """

        # When a UOM is found, its lower case key can be used to look up the
        # correct case format for it. If the UOM is in one of the below tuple
        # keys, then it's substituted with the value.
        uom_cases = {
            ("liter", "liters", "litres", "l"): "L",
            (
                "ml",
                "mls",
                "millilitre",
                "millilitres",
                "milliliter",
                "milliliters",
            ): "mL",
            ("g", "gram", "grams"): "g",
            ("lb", "lbs", "pound", "pounds"): "lb",
            ("kg", "kgs", "killogram", "killograms"): "kg",
            (
                "mm",
                "millimeter",
                "millimeters",
                "millimetre",
                "millimetres",
            ): "mm",
            (
                "cm",
                "centimeter",
                "centimeters",
                "centimetre",
                "centimetres",
            ): "cm",
            ("m", "meter", "meters", "metre", "metres"): "m",
            ("oz", "ounce", "ounces"): "oz",
            ("gal", "gallon", "gallons"): "gal",
            ("qt", "quart", "quarts"): "qt",
        }

        if type(content) is not str:
            return None

        content = content.strip()

        if not content or content.isspace():
            return None

        # https://regex101.com/r/lDLuVX/4
        pattern = (
            r"(?P<quantity>[0-9][0-9\.\,]*)\s?"
            r"(?P<uom>(?:milli|kilo|centi)"
            r"(?:gram|meter|liter|metre)s?|z|ounces?|grams?|gallon|gal"
            r"|kg|g|lbs?|pounds?|l|qt|m?[glm])"
        )

        matches = regex.search(pattern, content, regex.IGNORECASE)

        if not matches:
            return None

        quantity_obj = matches.groupdict()

        # Look for any proper substitution UOM's
        proper_uom = self._find_values_with_element(
            uom_cases, str(quantity_obj["uom"]).lower()
        )

        if len(proper_uom) > 0:
            quantity_obj["uom"] = proper_uom[0]

        return quantity_obj

    @finalmethod
    def _get_param_from_url(self, url: str, param: str = None) -> Optional[Any]:
        """Get a specific arameter from a GET URL

        Args:
            url (str): HREF address
            param (str): Param key to find (optional)

        Returns:
            Any: Whatver the value was of the key, or nothing

        Example:
            self._get_param_from_url(
                'http://google.com?foo=bar&product_id=12345'
            )
            {'foo':'bar','product_id':'12345'}
            self._get_param_from_url(
                'http://google.com?foo=bar&product_id=12345', 'product_id'
            )
            '12345'
        """

        parsed_url = urlparse(url)
        parsed_query = parse_qs(parsed_url.query)

        # Replace any ['values'] with just 'values'
        parsed_query = {
            k: v[0] if len(v) == 1 else v for k, v in parsed_query.items()
        }

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
            self._split_array_into_groups([
                'Variant', '500 g', 'CAS', '1762-95-4'
            ])
            [['Variant', '500 g'],['CAS', '1762-95-4']]
        """

        result = []
        for i in range(0, len(arr), size):
            result.append(arr[i : i + size])

        return result

    @finalmethod
    def _nested_arr_to_dict(self, arr: List[List]) -> Optional[Dict]:
        """Takes an array of arrays (ie: result from
        self._split_array_into_groups) and converts that into a dictionary.

        Args:
            arr (List[List]): The input array.

        Returns:
            Optional[Dict]: A dictionary based off of the input alues

        Example:
            self._nested_arr_to_dict([['foo','bar'], ['baz','quux']])
            {'foo':'bar','baz':'quux'}

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
            self._is_currency_symbol("$")
            True
            self._is_currency_symbol("foo")
            False
        """

        # Use Pythons nifty \p{Sc} pattern to make sure the value given is
        # actually a currency symbol
        return bool(regex.match(r"\p{Sc}", char, regex.IGNORECASE))

    @finalmethod
    def _currency_code_from_symbol(self, symbol: str) -> Optional[str]:
        """Attempt to get the currency code for a given currency symbol

        Source:
            https://www.eurochange.co.uk/travel/tips/world-currency-abbreviations-symbols-and-codes-travel-money

        Args:
            symbol (str): Currency symbol (eg: $, ¥, £, etc)

        Returns:
            Optional[str]: The currency code, if one is found

        Example:
            self._currency_code_from_symbol("$")
            "USD"
        """

        if type(symbol) is not str:
            return None

        symbol = symbol.strip()

        # Use Pythons nifty \p{Sc} pattern to make sure the value given is
        # actually a currency symbol
        if not self._is_currency_symbol(symbol):
            print(f"The symbol {symbol} does not match SC pattern")
            return None

        currency_codes = {
            "Lek": "ALL",
            "؋": "AFN",
            "$": "USD",
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

        return currency_codes[symbol] or None

    @finalmethod
    def _currency_symbol_from_code(self, code: str) -> Optional[str]:

        if type(code) is not str:
            return None

        code = code.strip().upper()
        # code = code.upper()

        currency_symbols = {
            "ALL": "Lek",
            "AFN": "؋",
            "ARS": "$",
            "AWG": "ƒ",
            "AUD": "$",
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
    def _cast_type(self, value: Union[str, int, float, bool] = None) -> Any:
        """Cast a value to the proper type. This is mostly used for casting
        int/float/bool

        Args:
            value (Union[str,int,float,bool]): Value to be casted (optional)

        Returns:
            Any: Casted value
        """

        # If it's not a string, then its probably a valid type..
        if type(value) is not str:
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
    def _random_string(
        self, length: Optional[int] = 10, include_special: bool = False
    ) -> str:
        """Generate random string

        Args:
            length (int, optional): Length to generate string to. Defaults to 10
            include_special (bool, optional): Include special chars in output.
                                              Defaults to False

        Returns:
            str: Random string, {length} chars long
        """
        if type(length) is not int:
            length = 10

        # ascii_letters = abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
        # digits = 0123456789
        # punctuation = !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~
        char_list = string.ascii_letters + string.digits

        if include_special is True:
            char_list += string.punctuation

        # trunk-ignore(bandit/B311)
        return "".join(random.choice(char_list) for _ in range(length))

    @finalmethod
    def _find_cas(self, value: str) -> Optional[str]:
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

        This is done by taking the first two segments and iterating over each
        individual intiger in reverse order, multiplying each by its position,
        then taking the modulous of the sum of those values.

        Example:
            1234-56-6 is valid because the result of the below equation matches
            the checksum, (which is 6)
                (6*1 + 5*2 + 4*3 + 3*4 + 2*5 + 1*6) % 10 == 6

            This can be simplified in the below aggregation:
                cas_chars = [1, 2, 3, 4, 5, 6]
                sum([(idx+1)*int(n) for idx, n
                    in enumerate(cas_chars[::-1])]) % 10

        See:
            https://www.cas.org/training/documentation/chemical-substances/checkdig

        Args:
            value (str): The value to determine if its a CAS # or not

        Returns:
            bool: True if its a valid format and the checksum matches
        """

        if type(value) is not str:
            return False

        # value='1234-56-6'
        # https://regex101.com/r/xPF1Yp/2
        cas_pattern_check = re.match(
            r"^(?P<seg_a>[0-9]{2,7})-(?P<seg_b>[0-9]{2})-(?P<checksum>[0-9])$",
            value,
        )

        if cas_pattern_check is None:
            return False

        cas_dict = cas_pattern_check.groupdict()
        # cas_dict = dict(seg_a='1234', seg_b='56', checksum='6')

        cas_chars = list(cas_dict["seg_a"] + cas_dict["seg_b"])
        # cas_chars = ['1','2','3','4','5','6']

        checksum = (
            sum([(idx + 1) * int(n) for idx, n in enumerate(cas_chars[::-1])])
            % 10
        )
        # checksum = 6

        return int(checksum) == int(cas_dict["checksum"])

    @finalmethod
    def _filter_highest_value(self, input_dict: Dict) -> Dict:
        """Filter a dictionary for the entry with the highest numerical value.

        Args:
            input_dict (Dict): Dictionary to iterate through

        Returns:
            Dict: Item in dictionary with highest value
        """

        if not input_dict:
            return {}
        max_value = max(input_dict.values())
        return {k: v for k, v in input_dict.items() if v == max_value}

    @finalmethod
    def _get_common_phrases(
        self,
        texts: list,
        maximum_length: int = 3,
        minimum_repeat: int = 2,
        stopwords: list = None,
    ) -> dict:
        stopwords = stopwords or []
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
                difference = (
                    phrases[phrase] - longest_phrases[l_phrase]
                ) / longest_phrases[l_phrase]
                if difference < 0.25:
                    found = True
                    break
            if not found:
                longest_phrases[phrase] = phrases[phrase]

        return longest_phrases

    @finalmethod
    def _find_values_with_element(
        self, source: Dict, element: Union[str, int]
    ) -> List:
        """
        Finds values in a dictionary that are tuples and contain a specific
        element.

        Args:
            source (Dict): The dictionary to search.
            element (str, int): The element to search for within the tuple keys

        Returns:
            List: A list of values that were found

        Example:
            my_dict = {
                (1, 2): "a",
                (2, 3): "b",
                (3, 4): "c",
                "hello": "d",
                (2, 5, 6): "e"
            }
            self._find_values_with_element(my_dict, 1)
            ['a']
            self._find_values_with_element(my_dict, 2)
            ['a', 'b', 'e']
            self._find_values_with_element(my_dict, "hello")
            ['d']
        """

        return [
            source[key]
            for key in source
            if (isinstance(key, tuple) and element in key)
            or (isinstance(key, str) and element == key)
        ]


__all__ = "ClassUtils"
