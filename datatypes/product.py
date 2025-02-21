from dataclasses import dataclass, astuple
from typing import List, Set, Tuple, Dict, Any


@dataclass
class TypeProduct:
    """Custom data class for products"""

    uuid: str = None
    """Unique identifier used by supplier"""

    title: str = None
    """Title of the product"""

    name: str = None
    """Product name (sometimes different than title)"""

    description: str = None
    """Product description"""

    brand: str = None
    """Brand of the product"""

    grade: str = None
    """Grade of reagent (ACS, reagent, USP, technical, etc)"""

    url: str = None
    """URL to direcet product (if availabe)"""

    cas: str = None
    """CAS Number"""

    price: float = None
    """Price of product"""

    currency: str = None
    """Currency the price is in"""

    quantity: float = None
    """Quantity of listing"""

    uom: str = None
    """Unit of measurement for quantity"""

    supplier: str = None
    """Supplier the product is provided by"""

    def update(self, data: Dict):
        """Update the TypeProduct instance

        Args:
            data (Dict): Dictionary to merge into current dictioary
        """
        self.__dict__.update(data)