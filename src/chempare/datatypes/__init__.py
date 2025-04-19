"""Custom datatypes"""

from decimal import Decimal


DecimalLikeType = int | float | Decimal
PrimitiveType = int | float | str | bool
TimeoutType = float | tuple[float, float] | tuple[float, None]

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
]

# QuantityType.__name__
