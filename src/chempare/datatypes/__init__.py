"""Custom datatypes"""

from decimal import Decimal
from enum import Enum
from typing import Literal
from typing import NewType


DecimalLikeType = int | float | Decimal
PrimitiveType = int | float | str | bool
TimeoutType = float | tuple[float, float] | tuple[float, None]
TruthyType = Literal["on", "true", "True", "TRUE", "1", True]
FalsyType = Literal["off", "false", "False", "FALSE", "0", False]

UndefinedType = Enum('UndefinedType', ['undefined'])
undefined = UndefinedType.undefined
type Undefined = Literal[UndefinedType.undefined]

from chempare.datatypes.price import PriceType
from chempare.datatypes.product import ProductType
from chempare.datatypes.quantity import QuantityType
from chempare.datatypes.supplier import SupplierType
from chempare.datatypes.variant import VariantType


__all__ = [
    "SupplierType",
    "ProductType",
    "VariantType",
    "DecimalLikeType",
    "QuantityType",
    "PriceType",
    "PrimitiveType",
    "Undefined",
    "TruthyType",
    "FalsyType",
]

# QuantityType.__name__
