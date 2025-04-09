"""TypeProduct datatype"""

import re
from dataclasses import dataclass
from typing import Any
from typing import Dict
from typing import ItemsView
from typing import List
from typing import Self

from chempare.datatypes.variant import TypeVariant


@dataclass
class TypeProduct:
    """Custom data class for products"""

    supplier: str
    """Supplier the product is provided by"""

    name: str | None = None
    """Product name (sometimes different than title)"""

    price: float | int | None = None
    """Price of product"""

    currency: str | None = None
    """Currency the price is in"""

    currency_code: str | None = None
    """The currency code, if one can be determined from the currency symbol"""

    quantity: float | int | None = None
    """Quantity of listing"""

    uom: str | None = None
    """Unit of measurement for quantity"""

    title: str | None = None
    """Title of the product"""

    uuid: str | int | None = None
    """Unique identifier used by supplier"""

    description: str | None = None
    """Product description"""

    brand: str | None = None
    """Brand of the product"""

    grade: str | None = None
    """Grade of reagent (ACS, reagent, USP, technical, etc)"""

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

    is_restricted: bool | None = None
    """If there are any restrictions for this product, this should be true"""

    restriction: str | None = None
    """String containing the value that the restriction was found in"""

    residential: bool | None = None
    """Does the supplier sell to residential addresses?"""

    individual: bool | None = None
    """Does the supplier sell to individual people? (as opposed to businesses
    only)"""

    variants: List[TypeVariant] | None = None
    """List of variants for this product"""

    formula: str | None = None
    """Chemical formula"""

    def items(self: Self) -> ItemsView[str, Any]:
        """Return dict_items of product attributes"""
        return self.__dict__.items()

    def update(self: Self, data: Dict) -> None:
        """Update the TypeProduct instance

        Args:
            data (Dict): Dictionary to merge into current dictioary
        """
        if data:
            self.__dict__.update(data)

    def set(self: Self, key, value) -> None:
        """Set a local attribute for this product"""
        setattr(self, key, value)

    def cast_properties(self: Self, include_none: bool = False) -> Dict:
        """Cast the product attributes to the likely formats, and return them
        in a separate dictionary, excluding record with None value by default

        Args:
            include_none (bool, optional): Exclude None types. Defaults
                                           to False.

        Returns:
            TypeProduct: Product with casted values
        """
        # dc = self.__class__.__dataclass_fields__['uuid'].type

        for key, val in self.items():
            _val = self.__cast_type(value=val)

            if _val is None and include_none is True:
                continue

            self.set(key, val)

        return self.__dict__

    def __cast_type(self: Self, value: Any) -> Any:
        """Cast a value to the proper type. This is mostly used for casting
        int/float/bool

        Args:
            value (Any): Value to be casted (optional)

        Returns:
            Any: Casted value
        """
        if value is None:
            return None

        # _type = type(value)

        # if key is not None:
        #     if _type is self.__class__.__dataclass_fields__[key].type:
        #         return value

        # if _type is float or _type is int or _type is bool:
        #     return value

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
