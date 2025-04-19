"""Custom datatypes"""

from dataclasses import dataclass
from decimal import Decimal
from typing import Optional
from typing import TypedDict


TypeDecimalLike = int | float | Decimal
TypePrimitive = int | float | str | bool
TypeTimeout = float | tuple[float, float] | tuple[float, None]

from chempare.datatypes.price import TypePrice
from chempare.datatypes.product import TypeProduct
from chempare.datatypes.quantity import TypeQuantity
from chempare.datatypes.supplier import TypeSupplier
from chempare.datatypes.variant import TypeVariant


__all__ = [
    "TypeSupplier",
    "TypeProduct",
    "TypeVariant",
    "TypeDecimalLike",
    "TypeQuantity",
    "TypePrice",
    "TypePrimitive",
]

# TypeQuantity.__name__
