from dataclasses import dataclass, astuple
from typing import List, Set, Tuple, Dict, Any


@dataclass
class Product:
    """Custom data class for products"""

    # Unique identifier used by supplier
    uuid: str = None

    # Title of the product
    title: str = None

    # Product name (sometimes different than title)
    name: str = None

    # Product description
    description: str = None

    # Brand of the product
    brand: str = None

    # Grade of reagent (ACS, reagent, USP, technical, etc)
    grade: str = None

    # URL to direcet product (if availabe)
    url: str = None

    # CAS Number
    cas: str = None

    # Price of product
    price: float = None

    # Currency the price is in
    currency: str = None

    # Quantity of listing
    quantity: float = None

    # Unit of measurement for quantity
    uom: str = None

    # Supplier the product is provided by
    supplier: str = None

    def update(self, data):
        self.__dict__.update(data)