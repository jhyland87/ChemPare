"""TypeVariant datatype"""

from dataclasses import dataclass
from typing import Dict
from typing import List
from typing import NoReturn
from typing import Union


@dataclass(init=False, match_args=True, kw_only=True)
class TypeVariant(Dict):
    """Custom data class for product variants"""

    __id: int = None
    """Index of the variant"""

    uuid: Union[str, int] = None
    """Unique identifier used by supplier"""

    title: str = None
    """Title of the product"""

    name: str = None
    """Product name (sometimes different than title)"""

    description: str = None
    """Product description"""

    container: str = None
    """Container type of the product"""

    url: str = None
    """URL to direcet product (if availabe)"""

    price: float = None
    """Price of product"""

    currency: str = None
    """Currency the price is in"""

    currency_code: str = None
    """The currency code, if one can be determined from the currency symbol"""

    quantity: float = None
    """Quantity of listing"""

    uom: str = None
    """Unit of measurement for quantity"""

    mpn: str = None
    """Manufacturer part number"""

    sku: str = None
    """Stock Keeping Unit - a unique code for a specific business"""

    upc: str = None
    """Universal Product Code - a globally recognized code"""

    is_restricted: bool = None
    """If there are any restrictions for this variant, this should be true"""

    restriction: str = None
    """String containing the value that the restriction was found in"""

    residential: bool = None
    """Does the supplier sell to residential addresses?"""

    individual: bool = None
    """Does the supplier sell to individual people? (as opposed to businesses
    only)"""

    def __init__(self, **kwargs):
        super().__init__(kwargs)
        self.update(kwargs)

    def __hash__(self):
        return hash((self.__id, self.name))

    def __eq__(self, other):
        return (
            isinstance(TypeVariant, other) is True
            and self.__hash__() == other.__hash__()
        )

    def __str__(self):
        return f"({self.__id}, {self.name})"

    # def __repr__(self):
    #     return f"TypeVariant(_id='{self._id}', name={self.name})"

    def set_id(self, id):
        self.__id = id

    def __iter__(self):
        """Used when dict(variant) is called. This will exclude empty values
        and private properties.
        """
        for key, val in self.__dict__.items():
            if val is not None and not key.startswith("_"):
                yield (key, val)

    def items(self) -> List:
        """Get Variant dictionary items in list format"""
        # return self.__dict__.items()
        return dict(self).items()

    def update(self, data: Dict) -> NoReturn:
        """Update the TypeProduct instance

        Args:
            data (Dict): Dictionary to merge into current dictioary
        """
        if data:
            self.__dict__.update(data)

    def set(self, key, value) -> NoReturn:
        """Set a local attribute for this product variant"""
        setattr(self, key, value)
