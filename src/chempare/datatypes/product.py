"""ProductType datatype"""

import re
from dataclasses import dataclass
from decimal import ROUND_HALF_UP
from decimal import Decimal
from typing import Any
from typing import ItemsView
from typing import Self

from chempare.datatypes.variant import VariantType


@dataclass
class ProductType:
    """Custom data class for products"""

    name: str
    """Product name (sometimes different than title)"""

    price: float | int | str
    """Price of product"""

    currency: str | None = None
    """Currency the price is in"""

    currency_code: str | None = None
    """The currency code, if one can be determined from the currency symbol"""

    quantity: float | str | None = None
    """Quantity of listing"""

    uom: str | None = None
    """Unit of measurement for quantity"""

    uuid: str | int | None = None
    """Unique identifier used by supplier"""

    title: str | None = None
    """Title of the product"""

    description: str | None = None
    """Product description"""

    brand: str | None = None
    """Brand of the product"""

    grade: str | None = None
    """Grade of reagent (ACS, reagent, USP, technical, etc)"""

    purity: str | None = None
    """Purity of reagent (usually in percentages)"""

    url: str | None = None
    """URL to direcet product (if availabe)"""

    cas: str | None = None
    """CAS Number"""

    manufacturer: str | None = None
    """Manufacturer name"""

    mpn: str | None = None
    """Manufacturer part number"""

    sku: str | None = None
    """Stock Keeping Unit - a unique code for a specific business"""

    upc: str | None = None
    """Universal Product Code - a globally recognized code"""

    supplier: str | None = None
    """Supplier the product is provided by"""

    is_restricted: bool | None = None
    """If there are any restrictions for this product, this should be true"""

    restriction: str | None = None
    """String containing the value that the restriction was found in"""

    residential: bool | None = None
    """Does the supplier sell to residential addresses?"""

    individual: bool | None = None
    """Does the supplier sell to individual people? (as opposed to businesses
    only)"""

    variants: list[VariantType] | None = None
    """list of variants for this product"""

    formula: str | None = None
    """Chemical formula"""

    usd: str | int | float | None = None
    """USD equivelant price (if price currency is not USD)"""

    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     self.update(kwargs)

    def update(self, data: dict) -> None:
        """Append a dictionary data to the product"""
        self.__dict__.update(data)

    def setdefault(self, key: str, val: Any) -> None:
        """Set the default value of a property"""
        self.__dict__.setdefault(key, val)

    def __bool__(self) -> bool:
        """This just allows us to use 'if not product'"""
        return True

    def __nonzero__(self) -> bool:
        """This just allows us to use 'if not product'"""
        return True

    def items(self) -> ItemsView[str, Any]:
        return self.__dict__.items()

    def set(self, key, value) -> None:
        """Set a local attribute for this product"""
        setattr(self, key, value)

    def cast_properties(self, include_none: bool = False) -> Self:
        """Cast the product attributes to the likely formats, and return them
        in a separate dictionary, excluding record with None value by default

        Args:
            include_none (bool, optional): Exclude None types. Defaults
                                           to False.

        Returns:
            ProductType: Product with casted values
        """
        # dc = self.__class__.__dataclass_fields__['uuid'].type

        for key, val in self.items():
            if key == "usd" and val is not None:
                _val = Decimal(val).quantize(Decimal("0.00"), ROUND_HALF_UP)
                continue

            if key == "price" and val is not None:
                _val = Decimal(val).quantize(Decimal("0.00"), ROUND_HALF_UP)
                continue

            _val = self.__cast_type(value=val)

            if _val is None and include_none is True:
                continue

            self.set(key, val)
            # setattr(self, key, val)
            # self.setarr(key, _val)

        return self

    def __cast_type(self, value: Any) -> Any:
        """Cast a value to the proper type. This is mostly used for casting
        int/float/bool

        Args:
            value (Any): Value to be casted (optional)

        Returns:
            Any: Casted value
        """
        if value is None:
            return None

        # If it's not a string, then its probably a valid type..
        if isinstance(value, str) is False:
            return value

        # Most castable values just need to be trimmed to be compatible
        value = value.strip()

        if not value or value.isspace():
            return None

        if value.lower() == "true":
            return True

        if value.lower() == "false":
            return False

        if re.match(r"^[0-9]+\.[0-9]+$", value):
            return float(value)

        if re.match(r"^[0-9]+$", value):
            return int(value)

        return value
