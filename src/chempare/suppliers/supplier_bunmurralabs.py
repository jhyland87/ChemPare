from __future__ import annotations

from typing import TYPE_CHECKING

from chempare.suppliers.supplier_wixbase import SupplierWixBase

if TYPE_CHECKING:
    from typing import Final

    from datatypes import SupplierType


# File: /suppliers/supplier_bunmurralabs.py
class SupplierBunmurraLabs(SupplierWixBase):
    """Bunmurra Labs Supplier Class"""

    _supplier: Final[SupplierType] = {
        "name": "Bunmurra Labs",
        "location": None,
        "base_url": "https://www.bunmurralabs.store",
        "api_url": "https://www.bunmurralabs.store",
        # api_key = '8B7o0X1o7c'
    }
    """Supplier specific data"""

    allow_cas_search: Final[bool] = True
    """Determines if the supplier allows CAS searches in addition to name
    searches"""


# The site is currently down, so we disable the supplier
__disabled__ = True
