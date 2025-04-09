"""TypeVariant datatype"""

from dataclasses import dataclass
from typing import Dict


@dataclass(init=False, match_args=True, kw_only=True)
class TypeVariant(Dict):
    """Custom data class for product variants"""

    name: str
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

    uuid: float | int | None = None
    """Unique identifier used by supplier"""

    description: str | None = None
    """Product description"""

    container: str | None = None
    """Container type of the product"""

    url: str | None = None
    """URL to direcet product (if availabe)"""

    mpn: str | None = None
    """Manufacturer part number"""

    sku: str | None = None
    """Stock Keeping Unit - a unique code for a specific business"""

    upc: str | None = None
    """Universal Product Code - a globally recognized code"""

    is_restricted: bool | None = None
    """If there are any restrictions for this variant, this should be true"""

    restriction: str | None = None
    """String containing the value that the restriction was found in"""

    residential: bool | None = None
    """Does the supplier sell to residential addresses?"""

    individual: bool | None = None
    """Does the supplier sell to individual people? (as opposed to businesses
    only)"""

    # def __init__(self: Self, **kwargs):
    #     super().__init__(kwargs)
    #     self.update(kwargs)

    # def __hash__(self) -> int:
    #     return hash((self.items))

    # def __eq__(self: Self, other):
    #     return (
    #         isinstance(TypeVariant, other) is True
    #         and self.__hash__() == other.__hash__()
    #     )

    # def __str__(self):
    #     return f"({self.items})"

    # def __iter__(self):
    #     """Used when dict(variant) is called. This will exclude empty values
    #     and private properties.
    #     """
    #     for key, val in self.__dict__.items():
    #         if val is not None and not key.startswith("_"):
    #             yield (key, val)

    # def items(self) -> Dict[Any, Any]:
    #     """Get Variant dictionary items in list format"""
    #     # return self.__dict__.items()
    #     return dict(self).items()

    # def update(self: Self, data: Dict) -> None:
    #     """Update the TypeProduct instance

    #     Args:
    #         data (Dict): Dictionary to merge into current dictioary
    #     """
    #     if data:
    #         self.__dict__.update(data)

    # def set(self: Self, key, value) -> None:
    #     """Set a local attribute for this product variant"""
    #     setattr(self, key, value)
