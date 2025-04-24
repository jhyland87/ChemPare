from __future__ import annotations

from decimal import Decimal
from decimal import ROUND_HALF_UP
from typing import NewType
from typing import TYPE_CHECKING
import regex
from chempare._constants import CURRENCY_CODES_MAP
from chempare._constants import CURRENCY_SYMBOLS_MAP
from currex import Currency
from datatypes import PriceType, DecimalLikeType
from price_parser.parser import Price

if TYPE_CHECKING:
    from datatypes import PriceType  # , Undefined

    # # Undefined = Enum('Undefined', ['undefined'])
    # # undefined = Undefined.undefined
    # Undefined = NewType('Undefined', str)

    # UndefinedStr = str | Undefined
    # undef = Undefined('undefined')

Undefined = NewType('Undefined', str)
undefined = str | Undefined


def is_currency_symbol(char: str) -> bool:
    """
    Determines if a value is a currency symbol or not

    Args:
        char (str): Value to analyze

    Returns:
        bool: True if it's a currency symbol

    Example:
        >>> utils.is_currency_symbol("$")
        True
        >>> utils.is_currency_symbol("foo")
        False
    """

    # Use Pythons nifty \p{Sc} pattern to make sure the value given is
    # actually a currency symbol
    return bool(regex.match(r"\p{Sc}", char, regex.IGNORECASE))


def parse_price(value) -> PriceType | None:
    price = Price.fromstring(value)

    if price is None or price.amount is None:
        return None
    # this gives us the currency (symbol), amount, amount_text and amount_float

    if not hasattr(price, 'currency'):
        raise ValueError("Price has no currency")

    currency_code = get_currency_code_from_symbol(price.currency)

    result: PriceType = {
        "currency": str(currency_code or price.currency),
        "currency_symbol": price.currency,
        "price": price.amount_float,
    }

    if currency_code is not None and currency_code != 'USD':
        if (usd_price := to_usd(price.amount_float, currency_code)) is not None:
            result["usd"] = usd_price

    return result


def to_usd(amount, from_currency):
    from_currency_obj = Currency(from_currency, amount)  # type: ignore

    if (in_usd := from_currency_obj.to("USD")) is None:
        return None

    return in_usd.amount.quantize(Decimal("0.00"), ROUND_HALF_UP)


def get_currency_code_from_symbol(symbol):
    if not symbol:
        return None

    return CURRENCY_CODES_MAP.get(symbol, None)


def get_currency_symbol_from_code(currency):
    if not currency:
        return None

    return CURRENCY_SYMBOLS_MAP.get(currency, None)


def to_hundreths(value: DecimalLikeType | str) -> Decimal:
    """
    Convert any number like value to include the hundreths place

    Args:
        value (DecimalLikeType | str): Value to convert

    Returns:
        Decimal: Equivelant value with hundreths.

    Example:
        >>> utils.to_hundreths("123")
        '123.00'
        >>> utils.to_hundreths("123.456")
        '123.45'
        >>> utils.to_hundreths(123.456)
        '123.45'
        >>> utils.to_hundreths(123)
        '123.00'
        >>> utils.to_hundreths(Decimal("123.1"))
        '123.10'
    """
    if not isinstance(value, Decimal):
        value = Decimal(value)

    return value.quantize(Decimal("0.00"), ROUND_HALF_UP)
