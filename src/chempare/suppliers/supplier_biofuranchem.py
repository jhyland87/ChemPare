"""Biofuran Chem Supplier Module"""
from __future__ import annotations

from typing import TYPE_CHECKING

from chempare.suppliers.supplier_wixbase import SupplierWixBase

if TYPE_CHECKING:
    from datatypes import SupplierType
    from typing import Final


# File: /suppliers/supplier_biofuranchem.py
class SupplierBioFuranChem(SupplierWixBase):

    _supplier: Final[SupplierType] = {
        "name": "BioFuran Chem",
        "location": None,
        "base_url": "https://www.biofuranchem.com",
        "api_url": "https://www.biofuranchem.com",
    }
    """Supplier specific data"""

    allow_cas_search: Final[bool] = True
    """Determines if the supplier allows CAS searches in addition to name searches"""
