"""TypePrice datatype"""

from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import fields
from decimal import Decimal


DecimalLike = int | float | Decimal


@dataclass
class TypePrice:
    price: DecimalLike
    currency: str
    currency_code: str | None = None
    usd: DecimalLike | None = None

    def __iter__(self):
        return iter(asdict(self).items())

    def __sizeof__(self):
        return len(asdict(self).values())

    def __bool__(self):
        return len(asdict(self).values()) > 0
