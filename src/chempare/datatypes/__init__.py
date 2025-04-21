"""Custom datatypes"""

from decimal import Decimal
from enum import Enum
from typing import Literal
from typing import Protocol
from typing import Any


class SupportsDict(Protocol):
    __dict__: dict[str, Any]


DecimalLikeType = int | float | Decimal
PrimitiveType = int | float | str | bool
TimeoutType = float | tuple[float, float] | tuple[float, None]
TruthyType = Literal["on", "true", "True", "TRUE", "1", True]
FalsyType = Literal["off", "false", "False", "FALSE", "0", False]

UndefinedType = Enum('UndefinedType', ['undefined'])
undefined = UndefinedType.undefined
type Undefined = Literal[UndefinedType.undefined]

from chempare.datatypes.price import PriceType  # pylint: disable=wrong-import-position
from chempare.datatypes.variant import VariantType  # pylint: disable=wrong-import-position
from chempare.datatypes.quantity import QuantityType  # pylint: disable=wrong-import-position
from chempare.datatypes.product import ProductType  # pylint: disable=wrong-import-position
from chempare.datatypes.supplier import SupplierType  # pylint: disable=wrong-import-position


__all__ = [
    "DecimalLikeType",
    "PrimitiveType",
    "Undefined",
    "TruthyType",
    "FalsyType",
    "PriceType",
    "VariantType",
    "ProductType",
    "QuantityType",
    "SupplierType",
    "SupportsDict",
]
