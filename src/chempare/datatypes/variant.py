"""VariantType datatype"""

from dataclasses import dataclass


@dataclass(init=False, match_args=True, kw_only=True)
class VariantType:
    """Custom data class for product variants"""

    uuid: str | int | None = None
    """Unique identifier used by supplier"""

    title: str | None = None
    """Title of the product"""

    name: str | None = None
    """Product name (sometimes different than title)"""

    description: str | None = None
    """Product description"""

    container: str | None = None
    """Container type of the product"""

    url: str | None = None
    """URL to direcet product (if availabe)"""

    price: float | None = None
    """Price of product"""

    currency: str | None = None
    """Currency the price is in"""

    currency_code: str | None = None
    """The currency code, if one can be determined from the currency symbol"""

    quantity: float | None = None
    """Quantity of listing"""

    uom: str | None = None
    """Unit of measurement for quantity"""

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

    # def __init__(self, **kwargs):
    #     super().__init__(kwargs)
    #     self.update(kwargs)

    # def __hash__(self):
    #     return hash((self.__id, self.name))

    # def __eq__(self, other):
    #     return (
    #         isinstance(VariantType, other) is True
    #         and self.__hash__() == other.__hash__()
    #     )

    # def __str__(self):
    #     return f"({self.__id}, {self.name})"

    # def __repr__(self):
    #     return f"VariantType(_id='{self._id}', name={self.name})"

    # def set_id(self, id):
    #     self.__id = id

    # def __iter__(self):
    #     """Used when dict(variant) is called. This will exclude empty values
    #     and private properties.
    #     """
    #     for key, val in self.__dict__.items():
    #         if val is not None and not key.startswith("_"):
    #             yield (key, val)

    # def items(self) -> list:
    #     """Get Variant dictionary items in list format"""
    #     # return self.__dict__.items()
    #     return dict(self).items()

    # def update(self, data: dict) -> None:
    #     """Update the ProductType instance

    #     Args:
    #         data (dict): Dictionary to merge into current dictioary
    #     """
    #     if data:
    #         self.__dict__.update(data)

    # def set(self, key, value) -> None:
    #     """Set a local attribute for this product variant"""
    #     setattr(self, key, value)
