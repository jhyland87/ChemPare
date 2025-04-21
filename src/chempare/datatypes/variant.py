"""VariantType datatype"""

from dataclasses import dataclass
from typing import Any
from chempare.datatypes import DecimalLikeType


@dataclass
class VariantType:
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

    title: str
    """Title of the product"""

    # price: PriceType | None = None
    price: DecimalLikeType
    """Price of product"""
    """The currency code, if one can be determined from the currency symbol"""

    quantity: DecimalLikeType
    """Quantity of listing"""

    uom: str
    """Unit of measurement for quantity"""

    currency: str | None = None
    """Currency the price is in"""

    currency_code: str | None = None

    url: str | None = None
    """URL to direcet product (if availabe, will default to product pages url)"""

    usd: DecimalLikeType | None = None
    """USD equivelant price (if price currency is not USD)"""

    description: str | None = None
    """Product description"""

    container: str | None = None
    """Container type of the product"""

    uuid: str | int | None = None
    """Unique identifier used by supplier"""

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

    _name: str | None = None
    """Unique name, if different than title"""

    @property
    def name(self) -> str | None:
        """
        Return the variants name if it is different than title. Sometimes products are
        listed with a name and a title, one is usually more viewer friendly than the
        other.

        Returns:
            str | None: The name of the product. Will return the title value if no
                        product name was set.
        """
        return self._name or self.title

    @name.setter
    def name(self, name: str) -> None:
        """
        Setter for the variant name property.

        Args:
            name (str): Name of the variant.
        """
        self._name = name

    def update(self, data: dict) -> None:
        """
        update the variant

        Update/extend the variant data using a dictionary.

        :param data: Dictionary with keys used in this datatype
        :type data: dict
        """
        self.__dict__.update(data)

    def setdefault(self, key: str, val: Any) -> None:
        """Set the default value of a property"""
        self.__dict__.setdefault(key, val)
