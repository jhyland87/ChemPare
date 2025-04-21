"""QuantityType datatype"""

from dataclasses import asdict
from dataclasses import dataclass

from chempare.datatypes import DecimalLikeType


@dataclass
class QuantityType:
    """
    QuantityType dataclass for quantity values.

    This stores an object that contains specific quantity information about a product
    or its variants.

    :param quantity: The quantity the product or variant has
    :type quantity: DecimalLikeType
    :param uom: Unit of measurement the quantity represents
    :type uom: str
    """

    quantity: DecimalLikeType
    uom: str

    def __iter__(self):
        return iter(asdict(self).items())

    def __sizeof__(self):
        return len(asdict(self).values())

    def __bool__(self):
        return len(asdict(self).values()) > 0
