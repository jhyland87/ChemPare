"""FTF Scientific Supplier Module"""

from chempare.datatypes import SupplierType
from chempare.suppliers.supplier_wixbase import SupplierWixBase


# File: /suppliers/supplier_ftfscientific.py
class SupplierFtfScientific(SupplierWixBase):
    """FTF Scientific Supplier Class"""

    _supplier: SupplierType = SupplierType(
        name="FTF Scientific",
        location=None,
        base_url="https://www.ftfscientific.com",
        api_url="https://www.ftfscientific.com",
        # api_key = '8B7o0X1o7c'
    )
    """Supplier specific data"""

    allow_cas_search: bool = True
    """Determines if the supplier allows CAS searches in addition to name
    searches"""
