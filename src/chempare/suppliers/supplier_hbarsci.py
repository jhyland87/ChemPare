from __future__ import annotations

from typing import TYPE_CHECKING

from chempare.suppliers.supplier_shopifybase import SupplierShopifyBase

if TYPE_CHECKING:
    from datatypes import SupplierType
    from typing import Any, Final, ClassVar


# File: /suppliers/supplier_hbarsci.py
class SupplierHbarSci(SupplierShopifyBase):

    _supplier: Final[SupplierType] = {
        "name": "Hbar Science",
        "base_url": "https://www.hbarsci.com",
        "api_url": "https://searchserverapi.com",
        "api_key": "2H3i9C5v0m",
    }
    """Supplier specific data"""

    allow_cas_search: Final[bool] = True
    """Determines if the supplier allows CAS searches in addition to name
    searches"""

    __defaults: ClassVar[dict[str, Any]] = {"currency": "$", "currency_code": "USD", "is_restricted": False}
    """Default values applied to products from this supplier"""
