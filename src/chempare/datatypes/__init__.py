"""Custom datatypes"""

from dataclasses import dataclass
from decimal import Decimal
from typing import Dict
from typing import Optional
from typing import TypedDict

from chempare.datatypes.product import TypeProduct
from chempare.datatypes.supplier import TypeSupplier
from chempare.datatypes.variant import TypeVariant

DecimalLike = int | float | Decimal


@dataclass
class QuantityType(Dict):
    quantity: DecimalLike
    uom: str


@dataclass
class PriceType(Dict):
    price: DecimalLike
    currency: str
    currency_code: Optional[str | None] = None
    usd: Optional[DecimalLike | None] = None


__all__ = [
    "TypeSupplier",
    "TypeProduct",
    "TypeVariant",
    "DecimalLike",
    "QuantityType",
    "PriceType",
]

# QuantityType.__name__
