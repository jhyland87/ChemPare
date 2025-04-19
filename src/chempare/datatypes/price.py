"""PriceType datatype"""

from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import fields

from chempare.datatypes import DecimalLikeType


@dataclass
class PriceType:
    price: DecimalLikeType
    currency: str
    currency_code: str | None = None
    usd: DecimalLikeType | None = None

    def __iter__(self):
        return iter(asdict(self).items())

    def __sizeof__(self):
        return len(asdict(self).values())

    def __bool__(self):
        return len(asdict(self).values()) > 0
