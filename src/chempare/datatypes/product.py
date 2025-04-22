"""ProductType datatype"""

from decimal import Decimal
from typing import TypedDict, Required
from chempare.datatypes import DecimalLikeType


class ProductType(TypedDict, total=False):
    """
    ProductType typed dictionary for products.

    Custom dict for products.

    :param title: The title of the variant
    :type title: str
    :param price: The actual price of the variant
    :type price: DecimalLikeType
    :param currency_symbol:  The currency symbol (eg: $)
    :type currency_symbol: str
    :param currency: The currency the price is in (USD, EUR, etc)
    :type currency: str
    :param quantity: The quantity the variant has
    :type quantity: DecimalLikeType
    :param uom: Unit of measurement the quantity represents
    :type uom: str
    :param supplier: Name of the supplier (ie: which class retrieved this product)
    :type supplier: str
    :param url: URL for variant web page
    :type url: str
    :param usd: If currency_code is not usd, then this should be the USD conversion value, defaults to None
    :type usd: DecimalLikeType, optional
    :param name: The name of the product, defaults to None
    :type name: str, optional
    :param description: Descriptor for product, defaults to None
    :type description: str, optional
    :param container: Container it's stored/shipped in, defaults to None
    :type container: str, optional
    :param uuid: Unique ID the product may have for supplier, defaults to None
    :type uuid: str, optional
    :param mpn: Manufacturer Part Number of variant, defaults to None
    :type mpn: str, optional
    :param sku: Stock Keeping Unit of variant, defaults to None
    :type sku: str, optional
    :param upc: Universal Product Code of variant, defaults to None
    :type upc: str, optional
    :param restriction: If is_restricted is True, details go here, defaults to None
    :type restriction: str, optional
    :param residential: Indicates if this product can ship to residential addresses, defaults to None
    :type residential: bool, optional
    :param individual: Indicates if this product can ship to private individuals, defaults to None
    :type individual: str, optional
    :param brand: Brand of the product, defaults to None
    :type brand: str, optional
    :param grade: Grade (quality) of product, defaults to None
    :type grade: str, optional
    :param purity: Purity of product (in percentages), defaults to None
    :type purity: str, optional
    :param cas: CAS ID for product, defaults to None
    :type cas: str, optional
    :param manufacturer: Manufacturer of product, defaults to None
    :type manufacturer: str, optional
    :param variants: List of variants this product is sold as, defaults to None
    :type variants: list[VariantType], optional
    :param formula: Chemical formula of product, defaults to None
    :type formula: str, optional
    """

    title: Required[str]
    price: Required[float | int]
    currency: Required[str]
    quantity: Required[DecimalLikeType]
    supplier: Required[str]
    url: Required[str]

    uom: str | None
    uuid: str | None
    description: str | None
    currency_symbol: str | None
    sku: str | None
    mpn: str | None
    upc: str | None
    cas: str | None
    usd: Decimal | None
    restriction: str | None
    residential: bool | None
    individual: bool | None
    manufacturer: str | None
    variants: list | None
    formula: str | None
    brand: str | None
    grade: str | None
    purity: str | None
    container: str | None
    quality: str | None
    name: str | None


# from functools import partial

# from dataclasses import dataclass
# from decimal import ROUND_HALF_UP
# from decimal import Decimal
# from typing import Any
# from typing import ItemsView
# from typing import Self
# from typing import overload
# from typing import Callable
# from typing import Iterable
# from collections.abc import Mapping

# from chempare.datatypes import DecimalLikeType
# from chempare.datatypes.variant import VariantType
# from chempare import utils


# @dataclass(repr=False)
# class ProductType:
#     """
#     ProductType dataclass for products.

#     Custom data class for products.

#     :param title: The title of the variant
#     :type title: str
#     :param price: The actual price of the variant
#     :type price: DecimalLikeType
#     :param currency:  The currency symbol (eg: $)
#     :type currency: str
#     :param currency_code: The currency the price is in (USD, EUR, etc)
#     :type currency_code: str
#     :param quantity: The quantity the variant has
#     :type quantity: DecimalLikeType
#     :param uom: Unit of measurement the quantity represents
#     :type uom: str
#     :param supplier: Name of the supplier (ie: which class retrieved this product)
#     :type supplier: str
#     :param url: URL for variant web page
#     :type url: str
#     :param usd: If currency_code is not usd, then this should be the USD conversion value, defaults to None
#     :type usd: DecimalLikeType | None, optional
#     :param name: The name of the product, defaults to None
#     :type name: str | None, optional
#     :param description: Descriptor for product, defaults to None
#     :type description: str | None, optional
#     :param container: Container it's stored/shipped in, defaults to None
#     :type container: str | None, optional
#     :param uuid: Unique ID the product may have for supplier, defaults to None
#     :type uuid: str | None, optional
#     :param mpn: Manufacturer Part Number of variant, defaults to None
#     :type mpn: str | None, optional
#     :param sku: Stock Keeping Unit of variant, defaults to None
#     :type sku: str | None, optional
#     :param upc: Universal Product Code of variant, defaults to None
#     :type upc: str | None, optional
#     :param is_restricted: Is this specific product restricted or not, defaults to None
#     :type is_restricted: bool | None, optional
#     :param restriction: If is_restricted is True, details go here, defaults to None
#     :type restriction: str | None, optional
#     :param residential: Indicates if this product can ship to residential addresses, defaults to None
#     :type residential: bool | None, optional
#     :param individual: Indicates if this product can ship to private individuals, defaults to None
#     :type individual: str | None, optional
#     :param brand: Brand of the product, defaults to None
#     :type brand: str | None, optional
#     :param grade: Grade (quality) of product, defaults to None
#     :type grade: str | None, optional
#     :param purity: Purity of product (in percentages), defaults to None
#     :type purity: str | None, optional
#     :param cas: CAS ID for product, defaults to None
#     :type cas: str | None, optional
#     :param manufacturer: Manufacturer of product, defaults to None
#     :type manufacturer: str | None, optional
#     :param variants: List of variants this product is sold as, defaults to None
#     :type variants: list[VariantType] | None, optional
#     :param formula: Chemical formula of product, defaults to None
#     :type formula: str | None, optional
#     """

#     title: str
#     """Title of the product"""

#     price: DecimalLikeType
#     """Price of product"""

#     currency: str
#     """Currency the price is in"""

#     currency_code: str
#     """The currency code, if one can be determined from the currency symbol"""

#     quantity: DecimalLikeType
#     """Quantity of listing"""

#     uom: str
#     """Unit of measurement for quantity"""

#     supplier: str
#     """Supplier the product is provided by"""

#     url: str
#     """URL to direcet product"""

#     usd: DecimalLikeType | None = None
#     """USD equivelant price (if price currency is not USD)"""

#     description: str | None = None
#     """Product description"""

#     container: str | None = None
#     """Container type the product is sold in"""

#     uuid: str | int | None = None
#     """Unique identifier used by supplier"""

#     mpn: str | None = None
#     """Manufacturer part number"""

#     sku: str | None = None
#     """Stock Keeping Unit - a unique code for a specific business"""

#     upc: str | None = None
#     """Universal Product Code - a globally recognized code"""

#     is_restricted: bool | None = None
#     """If there are any restrictions for this product, this should be true"""

#     restriction: str | None = None
#     """String containing the value that the restriction was found in"""

#     residential: bool | None = None
#     """Does the supplier sell to residential addresses?"""

#     individual: bool | None = None
#     """Does the supplier sell to individual people? (as opposed to businesses
#     only)"""

#     brand: str | None = None
#     """Brand of the product"""

#     grade: str | None = None
#     """Grade of reagent (ACS, reagent, USP, technical, etc)"""

#     purity: str | None = None
#     """Purity of reagent (usually in percentages)"""

#     cas: str | None = None
#     """CAS Number"""

#     manufacturer: str | None = None
#     """Manufacturer name"""

#     variants: list[VariantType] | None = None
#     """list of variants for this product"""

#     formula: str | None = None
#     """Chemical formula"""

#     name: str | None = None
#     """Unique name, if different than title"""

#     def __post_init__(self) -> None:
#         """
#         The function sets the 'name' attribute to 'title' if 'name' is None
#         """
#         if self.name is None:
#             self.name = self.title

#     def __iter__(self) -> Iterable:
#         """
#         The function returns an iterator for key-value pairs in the object's dictionary excluding None values.
#         :return: A dictionary comprehension is being used to filter out any key-value pairs where the value is
#         None from the object's `__dict__` attribute. The filtered key-value pairs are then returned as an iterator
#         using the `iter()` function.
#         """
#         return iter({k: v for k, v in self.__dict__.items() if v is not None})

#     def __repr__(self):
#         """
#         The `__repr__` function returns a string representation of an object's attributes in a formatted way.
#         :return: The `__repr__` method is returning a string representation of the object's class name and
#         its attributes. The attributes are formatted as key-value pairs with single quotes around the values,
#         and only attributes with non-None values are included in the string.
#         """
#         args = str(', '.join([f"{k}='{v}'" for k, v in sorted(self.__dict__.items()) if v is not None]))
#         return f"{self.__class__.__name__}({args})"

#     @overload
#     @staticmethod
#     def partial(**data: str) -> Callable:
#         """
#         partial Partial product creation

#         Create a partial ProductType object that can be used as a template to make complete objects

#         :param data: Dictionary with kwargs used to create partial ProductType
#         :type data: dict
#         :return: Partial ProductType instance
#         :rtype: Callable
#         :Example:
#         >>> partialProduct = ProductType.partial(supplier='Foo', currency_code='USD', currency='$')
#         >>> partialProduct(title='Test from partial', price=123.45, quantity=5, uom='L', url='http://website.com')
#         ProductType(currency='$', currency_code='USD', price='123.45', quantity='5', supplier='Foo',
#         title='Test from partial', uom='L', url='http://website.com')
#         """

#     @overload
#     @staticmethod
#     def partial(data: Mapping) -> Callable:
#         """
#         partial Partial product creation

#         Create a partial ProductType object that can be used as a template to make complete objects

#         :param data: Dictionary (or dictionary-ish) to create the partial from
#         :type data: dict
#         :return: Partial ProductType instance
#         :rtype: Callable
#         :Example:
#         >>> partialProduct = ProductType.partial({'supplier': 'Bar', 'currency_code': 'USD', 'currency': '$'})
#         >>> partialProduct(title='Test from partial', price=123.45, quantity=5, uom='L', url='http://website.com')
#         ProductType(currency_code='USD', currency='$', price='123.45', quantity='5', supplier='Bar',
#         title='Test from partial', uom='L', url='http://website.com')
#         """

#     @staticmethod
#     def partial(*args, **kwargs) -> Callable:
#         """
#         partial Create a partial ProductType object

#         This is the method that can take either a dictionary or kwargs to make the ProductType instance.

#         :return: Partial ProductType instance
#         :rtype: Callable
#         :Example:
#         >>> partialProductA = ProductType.partial(supplier='Foo', currency_code='USD', currency='$')
#         >>> partialProductA(title='Test from partial', price=123.45, quantity=5, uom='L', url='http://website.com')
#         ProductType(currency='$', currency_code='USD', price='123.45', quantity='5', supplier='Foo',
#         title='Test from partial', uom='L', url='http://website.com')
#         >>> partialProductB = ProductType.partial({'supplier': 'Bar', 'currency_code': 'USD', 'currency': '$'})
#         >>> partialProductB(title='Test from partial', price=123.45, quantity=5, uom='L', url='http://website.com')
#         ProductType(currency_code='USD', currency='$', price='123.45', quantity='5', supplier='Bar',
#         title='Test from partial', uom='L', url='http://website.com')
#         """
#         data = {}
#         if len(args) > 0 and isinstance(args[0], dict):
#             data.update(args[0])

#         if len(kwargs.keys()) != 0:
#             data.update(**kwargs)

#         return partial(ProductType, **data)

#     def update(self, data: dict) -> None:
#         """
#         update the product

#         Update/extend the products data using a dictionary.

#         :param data: Dictionary with keys used in this datatype
#         :type data: dict
#         :Example:
#         >>> product: ProductType = ProductType(title, price, currency, **kwargs)
#         >>> product.update({"uuid":"123","sku":"abc"})
#         """
#         self.__dict__.update(data)

#     def setdefault(self, key: str, val: Any) -> Self:
#         """
#         setdefault Set the default value of a property

#         Just to make it compatible with some dict style functions

#         :param key: Key of the default attribute being defined
#         :type key: str
#         :param val: Value of the attribute
#         :type val: Any
#         """
#         if self.__dict__.get(key) is None:
#             self.__dict__[key] = val

#         return self

#     def setdefaults(self, data: Mapping) -> Self:
#         """
#         setdefaults uses setdefault for a full dictionary

#         Makes it easier if one needs to run setdefault() for a dictionary of values

#         :param data: Any dictionary like object (anything with __dict__)
#         :type data: Mapping

#         """
#         for key, val in data.items():
#             self.setdefault(key, val)

#         return self

#     def __bool__(self) -> bool:
#         """
#         This just allows us to use 'if not product' checks.

#         :return: This will always be true since the object couldn't be created without
#                  the necessary values (title, price, currency, currency_code, quality,
#                  uom, supplier, url)
#         :rtype: bool
#         """
#         return bool(len(self.items()))

#     def __nonzero__(self) -> bool:
#         """
#         The function __nonzero__ always returns True, to make `if product` checks easier
#         :return: The method `__nonzero__` is returning a boolean value `True`.
#         """
#         return True

#     def items(self) -> ItemsView[str, Any]:
#         """
#         The function returns a view of the items in the object's dictionary.
#         :return: The `items()` method is being called on the `self.__dict__` attribute, which returns a view
#         object that displays a list of a dictionary's key-value tuple pairs.
#         """
#         return self.__dict__.items()

#     def set(self, key, value) -> None:
#         """
#         The function sets an attribute with a specified key and value in the object.

#         :param key: The `key` parameter in the `set` method is used to specify the attribute name that you want to
#         set on the object instance
#         :param value: The `value` parameter in the `set` method represents the value that you want to associate
#         with the specified `key`. When you call the `set` method with a `key` and a `value`, it sets the attribute
#         with the name `key` on the object to the specified `value`
#         """
#         setattr(self, key, value)

#     def cast_properties(self, include_none: bool = False) -> Self:
#         """
#         cast_properties Cast properties of product to appropriate data types.

#         Cast the product attributes to the likely formats, and return them
#         in a separate dictionary, excluding record with None value by default

#         :param include_none: Unless True, all None values will be removed, defaults to False
#         :type include_none: bool, optional
#         :return: Product with casted values
#         :rtype: Self
#         :Example:
#         >>> product: ProductType = ProductType(title, price, currency, **kwargs)
#         >>> product.update({"uuid":"123","sku":"abc"})
#         >>> product.cast_properties()
#         ProductType(... uuid=123, sku="abc")
#         """
#         for key, val in self.items():
#             if val is None and include_none is False:
#                 continue

#             if key == "usd" and val is not None:
#                 val = Decimal(val).quantize(Decimal("0.00"), ROUND_HALF_UP)
#             elif key == "price" and val is not None:
#                 val = Decimal(val).quantize(Decimal("0.00"), ROUND_HALF_UP)
#             elif isinstance(val, str):
#                 val = utils.cast(value=val)

#             self.set(key, val)

#         return self
