from datatypes import SupplierType
from chempare.suppliers.supplier_shopifybase import SupplierShopifyBase


# File: /suppliers/supplier_laballey.py
class SupplierLaballey(SupplierShopifyBase):

    _supplier: SupplierType = SupplierType(
        name="Laballey",
        base_url="https://www.laballey.com",
        api_url="https://searchserverapi.com",
        api_key="8B7o0X1o7c",
    )
    """Supplier specific data"""

    allow_cas_search: bool = True
    """Determines if the supplier allows CAS searches in addition to name
    searches"""

    __defaults: dict = {"currency": "$", "currency_code": "USD", "is_restricted": False}
    """Default values applied to products from this supplier"""
