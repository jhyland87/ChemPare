"""Custom Datatype"""

from decimal import Decimal
from typing import TypedDict
from typing import Required
from typing import Literal
from typing import Protocol
from typing import Any

from enum import Enum

# export MYPYPATH=/Users/justinhyland/Documents/projects/ChemPare/src/chempare/stubs
DecimalLikeType = int | float | Decimal
PrimitiveType = int | float | str | bool
TimeoutType = float | tuple[float, float] | tuple[float, None]
TruthyType = Literal["on", "true", "True", "TRUE", "1", True]
FalsyType = Literal["off", "false", "False", "FALSE", "0", False]

UndefinedType = Enum('UndefinedType', ['undefined'])
undefined = UndefinedType.undefined
type Undefined = Literal[UndefinedType.undefined]

class SupportsDict(Protocol):
    __dict__: dict[str, Any]

class PriceType(TypedDict, total=False):
    price: Required[DecimalLikeType]
    currency: Required[str]
    currency_symbol: str | None
    usd: DecimalLikeType | None

class QuantityType(TypedDict, total=False):
    quantity: Required[DecimalLikeType]
    uom: str

class SupplierType(TypedDict, total=False):
    """
    SupplierType dataclass for supplier specific data


    :param name: Name of the supplier
    :type name: str
    :param base_url: Base URL of suppliers website
    :type base_url: str
    :param api_url: Base URL of suppliers API resource, defaults to None
    :type api_url: str | None, optional
    :param api_key: API key for supplier, if there is one found, defaults to None
    :type api_key: str | None, optional
    :param location: Location the supplier is based out of, defaults to None
    :type location: str | None, optional
    """

    name: Required[str]
    """Name of supplier"""

    base_url: Required[str]
    """Base URL for supplier"""

    api_url: str | None
    """URL for public facing API - may not be the same as base_url"""

    api_key: str | None
    """Key for API calls, if needed"""

    location: str | None
    """Location of supplier"""

class VariantType(TypedDict, total=False):
    """
    VariantType dataclass for product variants.

    This contains some of the same attributes as the ProductType datatype.

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
    """

    title: Required[str]
    """Title of the product"""

    # price: PriceType
    price: Required[DecimalLikeType]
    """Price of product"""

    quantity: Required[DecimalLikeType]
    """Quantity of listing"""

    name: str
    """Unique name, if different than title"""

    uom: str
    """Unit of measurement for quantity"""

    url: str
    """URL to direcet product (if availabe, will default to product pages url)"""

    usd: DecimalLikeType
    """USD equivelant price (if price currency is not USD)"""

    description: str
    """Product description"""

    container: str
    """Container type of the product"""

    uuid: str | int
    """Unique identifier used by supplier"""

    mpn: str
    """Manufacturer part number"""

    sku: str
    """Stock Keeping Unit - a unique code for a specific business"""

    upc: str
    """Universal Product Code - a globally recognized code"""

    restriction: str
    """String containing the value that the restriction was found in"""

    residential: bool
    """Does the supplier sell to residential addresses?"""

    individual: bool
    """Does the supplier sell to individual people? (as opposed to businesses
    only)"""

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
    :param usd: If currency_code is not usd, then this should be the USD conversion value
    :type usd: DecimalLikeType, optional
    :param name: The name of the product
    :type name: str, optional
    :param description: Descriptor for product
    :type description: str, optional
    :param container: Container it's stored/shipped in
    :type container: str, optional
    :param uuid: Unique ID the product may have for supplier
    :type uuid: str, optional
    :param mpn: Manufacturer Part Number of variant
    :type mpn: str, optional
    :param sku: Stock Keeping Unit of variant
    :type sku: str, optional
    :param upc: Universal Product Code of variant
    :type upc: str, optional
    :param restriction: If is_restricted is True, details go here
    :type restriction: str, optional
    :param residential: Indicates if this product can ship to residential addresses
    :type residential: bool, optional
    :param individual: Indicates if this product can ship to private individuals
    :type individual: str, optional
    :param brand: Brand of the product
    :type brand: str, optional
    :param grade: Grade (quality) of product
    :type grade: str, optional
    :param purity: Purity of product (in percentages)
    :type purity: str, optional
    :param cas: CAS ID for product
    :type cas: str, optional
    :param manufacturer: Manufacturer of product
    :type manufacturer: str, optional
    :param variants: List of variants this product is sold as
    :type variants: list[VariantType], optional
    :param formula: Chemical formula of product
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
