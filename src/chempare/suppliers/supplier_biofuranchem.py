"""Biofuran Chem Supplier Module"""

from datatypes import SupplierType
from chempare.suppliers.supplier_wixbase import SupplierWixBase


# File: /suppliers/supplier_biofuranchem.py
class SupplierBioFuranChem(SupplierWixBase):

    _supplier: SupplierType = SupplierType(
        name="BioFuran Chem",
        location=None,
        base_url="https://www.biofuranchem.com",
        api_url="https://www.biofuranchem.com",
    )
    """Supplier specific data"""

    allow_cas_search: bool = True
    """Determines if the supplier allows CAS searches in addition to name searches"""
