"""FTF Scientific Supplier Module"""
from __future__ import annotations

from typing import TYPE_CHECKING

from chempare.suppliers.supplier_wixbase import SupplierWixBase

if TYPE_CHECKING:
    from datatypes import SupplierType
    from typing import Final


# File: /suppliers/supplier_ftfscientific.py
class SupplierFtfScientific(SupplierWixBase):
    """FTF Scientific Supplier Class"""

    _supplier: Final[SupplierType] = {
        "name": "FTF Scientific",
        "location": None,
        "base_url": "https://www.ftfscientific.com",
        "api_url": "https://www.ftfscientific.com",
        # api_key = '8B7o0X1o7c'
    }
    """Supplier specific data"""

    allow_cas_search: Final[bool] = True
    """Determines if the supplier allows CAS searches in addition to name
    searches"""
