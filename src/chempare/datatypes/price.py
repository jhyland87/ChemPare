"""PriceType datatype"""

from dataclasses import asdict
from dataclasses import dataclass

from chempare.datatypes import DecimalLikeType


@dataclass
class PriceType:
    """
    PriceType dataclass for price like values.

    This is to be used for any product prices as well as the prices in the VariantType datatype.

    :param price: The actual price in a numerical type format
    :type price: DecimalLikeType
    :param currency: The currency symbol (eg: $)
    :type currency: str
    :param currency_code: The currency the price is in (USD, EUR, etc)
    :type currency_code: str
    :param usd: If currency_code is not usd, then this should be the USD conversion value, defaults to None
    :type usd: DecimalLikeType | None, optional
    """

    price: DecimalLikeType
    currency: str
    currency_code: str
    usd: DecimalLikeType | None = None

    def __iter__(self):
        return iter(asdict(self).items())

    def __sizeof__(self):
        return len(asdict(self).values())

    def __bool__(self):
        return len(asdict(self).values()) > 0
