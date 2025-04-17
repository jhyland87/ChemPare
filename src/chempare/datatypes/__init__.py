"""Custom datatypes"""

from dataclasses import dataclass
from decimal import Decimal
from typing import Dict
from typing import Optional
from typing import TypedDict

from chempare.datatypes.price import TypePrice
from chempare.datatypes.product import TypeProduct
from chempare.datatypes.quantity import TypeQuantity
from chempare.datatypes.supplier import TypeSupplier
from chempare.datatypes.variant import TypeVariant


DecimalLike = int | float | Decimal

__all__ = ["TypeSupplier", "TypeProduct", "TypeVariant", "DecimalLike", "TypeQuantity", "TypePrice"]

# TypeQuantity.__name__
