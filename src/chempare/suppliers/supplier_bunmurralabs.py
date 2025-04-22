from datatypes import SupplierType
from chempare.suppliers.supplier_wixbase import SupplierWixBase


# File: /suppliers/supplier_bunmurralabs.py
class SupplierBunmurraLabs(SupplierWixBase):
    """Bunmurra Labs Supplier Class"""

    _supplier: SupplierType = SupplierType(
        name="Bunmurra Labs",
        location=None,
        base_url="https://www.bunmurralabs.store",
        api_url="https://www.bunmurralabs.store",
        # api_key = '8B7o0X1o7c'
    )
    """Supplier specific data"""

    allow_cas_search: bool = True
    """Determines if the supplier allows CAS searches in addition to name
    searches"""
