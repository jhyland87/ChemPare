"""ProductType datatype"""

from functools import partial

from dataclasses import dataclass
from decimal import ROUND_HALF_UP
from decimal import Decimal
from typing import Any
from typing import ItemsView
from typing import Self
from typing import overload
from typing import Callable

from chempare.datatypes import DecimalLikeType
from chempare.datatypes import SupportsDict
from chempare.datatypes.variant import VariantType
from chempare import utils


@dataclass(repr=False)
class ProductType:
    """
    ProductType dataclass for products.

    Custom data class for products.

    :param title: The title of the variant
    :type title: str
    :param price: The actual price of the variant
    :type price: DecimalLikeType
    :param currency:  The currency symbol (eg: $)
    :type currency: str
    :param currency_code: The currency the price is in (USD, EUR, etc)
    :type currency_code: str
    :param quantity: The quantity the variant has
    :type quantity: DecimalLikeType
    :param uom: Unit of measurement the quantity represents
    :type uom: str
    :param supplier: Name of the supplier (ie: which class retrieved this product)
    :type supplier: str
    :param url: URL for variant web page
    :type url: str
    :param usd: If currency_code is not usd, then this should be the USD conversion value, defaults to None
    :type usd: DecimalLikeType | None, optional
    :param name: The name of the product, defaults to None
    :type name: str | None, optional
    :param description: Descriptor for product, defaults to None
    :type description: str | None, optional
    :param container: Container it's stored/shipped in, defaults to None
    :type container: str | None, optional
    :param uuid: Unique ID the product may have for supplier, defaults to None
    :type uuid: str | None, optional
    :param mpn: Manufacturer Part Number of variant, defaults to None
    :type mpn: str | None, optional
    :param sku: Stock Keeping Unit of variant, defaults to None
    :type sku: str | None, optional
    :param upc: Universal Product Code of variant, defaults to None
    :type upc: str | None, optional
    :param is_restricted: Is this specific product restricted or not, defaults to None
    :type is_restricted: bool | None, optional
    :param restriction: If is_restricted is True, details go here, defaults to None
    :type restriction: str | None, optional
    :param residential: Indicates if this product can ship to residential addresses, defaults to None
    :type residential: bool | None, optional
    :param individual: Indicates if this product can ship to private individuals, defaults to None
    :type individual: str | None, optional
    :param brand: Brand of the product, defaults to None
    :type brand: str | None, optional
    :param grade: Grade (quality) of product, defaults to None
    :type grade: str | None, optional
    :param purity: Purity of product (in percentages), defaults to None
    :type purity: str | None, optional
    :param cas: CAS ID for product, defaults to None
    :type cas: str | None, optional
    :param manufacturer: Manufacturer of product, defaults to None
    :type manufacturer: str | None, optional
    :param variants: List of variants this product is sold as, defaults to None
    :type variants: list[VariantType] | None, optional
    :param formula: Chemical formula of product, defaults to None
    :type formula: str | None, optional
    """

    title: str
    """Title of the product"""

    price: DecimalLikeType
    """Price of product"""

    currency: str
    """Currency the price is in"""

    currency_code: str
    """The currency code, if one can be determined from the currency symbol"""

    quantity: DecimalLikeType
    """Quantity of listing"""

    uom: str
    """Unit of measurement for quantity"""

    supplier: str
    """Supplier the product is provided by"""

    url: str
    """URL to direcet product"""

    usd: DecimalLikeType | None = None
    """USD equivelant price (if price currency is not USD)"""

    description: str | None = None
    """Product description"""

    container: str | None = None
    """Container type the product is sold in"""

    uuid: str | int | None = None
    """Unique identifier used by supplier"""

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

    brand: str | None = None
    """Brand of the product"""

    grade: str | None = None
    """Grade of reagent (ACS, reagent, USP, technical, etc)"""

    purity: str | None = None
    """Purity of reagent (usually in percentages)"""

    cas: str | None = None
    """CAS Number"""

    manufacturer: str | None = None
    """Manufacturer name"""

    variants: list[VariantType] | None = None
    """list of variants for this product"""

    formula: str | None = None
    """Chemical formula"""

    name: str | None = None
    """Unique name, if different than title"""

    # def __init__(self, **kwargs):
    #     if 'name' in kwargs:
    #         kwargs['_name'] = kwargs.get('name')

    #         del kwargs['name']

    #     self.__dict__.update(kwargs)
    #     super().__init__(self)

    def __post_init__(self):
        if self.name is None:
            self.name = self.title

    def __iter__(self):
        return iter({k: v for k, v in self.__dict__.items() if v is not None})

    def __repr__(self):
        args = str(', '.join([f"{k}='{v}'" for k, v in sorted(self.__dict__.items()) if v is not None]))
        return f"{self.__class__.__name__}({args})"

    @overload
    @staticmethod
    def partial(**data: str) -> Callable:
        """
        partial Partial product creation

        Create a partial ProductType object that can be used as a template to make complete objects

        :param data: Dictionary with kwargs used to create partial ProductType
        :type data: dict
        :return: Partial ProductType instance
        :rtype: Callable
        :Example:
        >>> partialProduct = ProductType.partial(supplier='Foo', currency_code='USD', currency='$')
        >>> partialProduct(title='Test from partial', price=123.45, quantity=5, uom='L', url='http://website.com')
        ProductType(currency='$', currency_code='USD', price='123.45', quantity='5', supplier='Foo',
        title='Test from partial', uom='L', url='http://website.com')
        """

    @overload
    @staticmethod
    def partial(data: SupportsDict) -> Callable:
        """
        partial Partial product creation

        Create a partial ProductType object that can be used as a template to make complete objects

        :param data: Dictionary (or dictionary-ish) to create the partial from
        :type data: dict
        :return: Partial ProductType instance
        :rtype: Callable
        :Example:
        >>> partialProduct = ProductType.partial({'supplier': 'Bar', 'currency_code': 'USD', 'currency': '$'})
        >>> partialProduct(title='Test from partial', price=123.45, quantity=5, uom='L', url='http://website.com')
        ProductType(currency_code='USD', currency='$', price='123.45', quantity='5', supplier='Bar',
        title='Test from partial', uom='L', url='http://website.com')
        """

    @staticmethod
    def partial(*args, **kwargs) -> Callable:
        """
        partial Create a partial ProductType object

        This is the method that can take either a dictionary or kwargs to make the ProductType instance


        :return: Partial ProductType instance
        :rtype: Callable
        :Example:
        >>> partialProductA = ProductType.partial(supplier='Foo', currency_code='USD', currency='$')
        >>> partialProductA(title='Test from partial', price=123.45, quantity=5, uom='L', url='http://website.com')
        ProductType(currency='$', currency_code='USD', price='123.45', quantity='5', supplier='Foo',
        title='Test from partial', uom='L', url='http://website.com')
        >>> partialProductB = ProductType.partial({'supplier': 'Bar', 'currency_code': 'USD', 'currency': '$'})
        >>> partialProductB(title='Test from partial', price=123.45, quantity=5, uom='L', url='http://website.com')
        ProductType(currency_code='USD', currency='$', price='123.45', quantity='5', supplier='Bar',
        title='Test from partial', uom='L', url='http://website.com')
        """
        data = {}
        if len(args) > 0 and isinstance(args[0], dict):
            data.update(args[0])

        if len(kwargs.keys()) != 0:
            data.update(**kwargs)
        return partial(ProductType, **data)

    # @property
    # def name(self) -> str | None:
    #     """
    #     name - Name of property, may be different than the title

    #     Sometimes products are listed with a name and a title, one is usually more viewer
    #     friendly than the other.

    #     :return: The name of the product. Will return the title value if no product name was set.
    #     :rtype: str | None
    #     """
    #     return getattr(self, '_name', self.title)

    # # name: str | None = property(get_name)

    # @name.setter
    # def name(self, name: str) -> None:
    #     """
    #     name setter

    #     Setter for the product name property.

    #     :param name: Value to set the name property to
    #     :type name: str
    #     """
    #     self._name = name

    def update(self, data: dict) -> None:
        """
        update the product

        Update/extend the products data using a dictionary.

        :param data: Dictionary with keys used in this datatype
        :type data: dict
        :Example:
        >>> product: ProductType = ProductType(title, price, currency, **kwargs)
        >>> product.update({"uuid":"123","sku":"abc"})
        """
        self.__dict__.update(data)

    def setdefault(self, key: str, val: Any) -> None:
        """
        setdefault Set the default value of a property

        Just to make it compatible with some dict style functions

        :param key: Key of the default attribute being defined
        :type key: str
        :param val: Value of the attribute
        :type val: Any
        """
        self.__dict__.setdefault(key, val)

    def setdefaults(self, data: SupportsDict) -> None:
        """
        setdefaults uses setdefault for a full dictionary

        Makes it easier if one needs to run setdefault() for a dictionary of values

        :param data: Any dictionary like object (anything with __dict__)
        :type data: SupportsDict

        """
        for key, val in data.__dict__.items():
            self.setdefault(key, val)

    def __bool__(self) -> bool:
        """
        This just allows us to use 'if not product' checks.

        :return: This will always be true since the object couldn't be created without
                 the necessary values (title, price, currency, currency_code, quality,
                 uom, supplier, url)
        :rtype: bool
        """
        return bool(len(self.items()))

    def __nonzero__(self) -> bool:
        """This just allows us to use 'if not product'"""
        return True

    def items(self) -> ItemsView[str, Any]:
        return self.__dict__.items()

    def set(self, key, value) -> None:
        """Set a local attribute for this product"""
        setattr(self, key, value)

    def cast_properties(self, include_none: bool = False) -> Self:
        """
        cast_properties Cast properties of product to appropriate data types.

        Cast the product attributes to the likely formats, and return them
        in a separate dictionary, excluding record with None value by default

        :param include_none: Unless True, all None values will be removed, defaults to False
        :type include_none: bool, optional
        :return: Product with casted values
        :rtype: Self
        :Example:
        >>> product: ProductType = ProductType(title, price, currency, **kwargs)
        >>> product.update({"uuid":"123","sku":"abc"})
        >>> product.cast_properties()
        ProductType(... uuid=123, sku="abc")
        """

        for key, val in self.items():
            _val = val
            if key == "usd" and val is not None:
                _val = Decimal(val).quantize(Decimal("0.00"), ROUND_HALF_UP)
                continue

            if key == "price" and val is not None:
                _val = Decimal(val).quantize(Decimal("0.00"), ROUND_HALF_UP)
                continue

            if isinstance(val, str):
                _val = utils.cast(value=val)

            if _val is None and include_none is True:
                continue

            self.set(key, val)

        return self
