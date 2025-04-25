from __future__ import annotations

from typing import TYPE_CHECKING

from chempare.suppliers.supplier_shopifybase import SupplierShopifyBase

if TYPE_CHECKING:
    from datatypes import SupplierType
    from typing import Any, Final, ClassVar


# File: /suppliers/supplier_laballey.py
class SupplierLaballey(SupplierShopifyBase):

    _supplier: Final[SupplierType] = {
        "name": "Laballey",
        "base_url": "https://www.laballey.com",
        "api_url": "https://searchserverapi.com",
        "api_key": "8B7o0X1o7c",
    }
    """Supplier specific data"""

    allow_cas_search: Final[bool] = True
    """Determines if the supplier allows CAS searches in addition to name
    searches"""

    __defaults: ClassVar[dict[str, Any]] = {"currency": "$", "currency_code": "USD", "is_restricted": False}
    """Default values applied to products from this supplier"""
