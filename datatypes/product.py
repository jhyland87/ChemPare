from dataclasses import dataclass
from typing import List, Set, Tuple, Dict, Any, Union
import re


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

    manufacturer: str = None
    """Manufacturer name"""

    mpn: str = None
    """Manufacturer part number"""

    sku: str = None
    """Stock Keeping Unit - a unique code for a specific business"""

    upc: str = None
    """Universal Product Code - a globally recognized code"""

    supplier: str = None
    """Supplier the product is provided by"""

    is_restricted: bool = None
    """If there are any restrictions for this product, this should be true"""

    restriction: str = None
    """String containing the value that the restriction was found in"""

    residential: bool = None
    """Does the supplier sell to residential addresses?"""

    individual: bool = None
    """Does the supplier sell to individual people? (as opposed to businesses only)"""

    def items(self):
        return self.__dict__.items()
    
    def update(self, data: Dict):
        """Update the TypeProduct instance

        Args:
            data (Dict): Dictionary to merge into current dictioary
        """
        self.__dict__.update(data)

    def cast_properties(self, include_none:bool=False) -> Dict:
        """Cast the product attributes to the likely formats, and return them in a
        separate dictionary, excluding record with None value by default

        Args:
            include_none (bool, optional): Exclude None types. Defaults to False.

        Returns:
            TypeProduct: Product with casted values
        """
        #dc = self.__class__.__dataclass_fields__['uuid'].type

        for key, val in self.items():
            _val = self.__cast_type(value=val, key=key)
            self.__setattr__(key, _val)

        return self

    def __cast_type(self, value: Union[str,int,float,bool], key:str=None) -> Any:
        """Cast a value to the proper type. This is mostly used for casting int/float/bool

        Args:
            value (Union[str,int,float,bool]): Value to be casted (optional)

        Returns:
            Any: Casted value
        """
        if value is None:
            return None
        
        #_type = type(value)

        # if key is not None:
        #     if _type is self.__class__.__dataclass_fields__[key].type:
        #         return value
        
        # if _type is float or _type is int or _type is bool:
        #     return value
        
        # If it's not a string, then its probably a valid type..
        if type(value) != str:
            return value
        
        # Most castable values just need to be trimmed to be compatible
        value = value.strip()

        if not value or value.isspace():
            return None
            
        if value.lower() == 'true':
            return True
            
        if value.lower() == 'false':
            return False
            
        if value.isdecimal() or re.match(f'^[0-9]+.[0-9]+$', value): 
            return float(value) 
                
        if value.isnumeric() or re.match(f'^[0-9]+$', value):
            return int(value)
            
        return value