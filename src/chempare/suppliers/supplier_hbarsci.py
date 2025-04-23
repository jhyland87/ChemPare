from __future__ import annotations

from chempare.suppliers.supplier_shopifybase import SupplierShopifyBase
from datatypes import SupplierType


# File: /suppliers/supplier_hbarsci.py
class SupplierHbarSci(SupplierShopifyBase):

    _supplier: SupplierType = SupplierType(
        name="Hbar Science",
        base_url="https://www.hbarsci.com",
        api_url="https://searchserverapi.com",
        api_key="2H3i9C5v0m",
    )
    """Supplier specific data"""

    allow_cas_search: bool = True
    """Determines if the supplier allows CAS searches in addition to name
    searches"""

    __defaults: dict = {"currency": "$", "currency_code": "USD", "is_restricted": False}
    """Default values applied to products from this supplier"""
