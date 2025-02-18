import os, sys

SCRIPT_DIR = os.path.dirname(os.path.abspath('suppliers/supplier_onyxmet'))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from suppliers.supplier_onyxmet import SupplierOnyxmet

def fetch_from_onyxmet(chem):
    onyxmet = SupplierOnyxmet(chem)

    name_list = []
    price_list = []

    for product in onyxmet.products[:3]:
        name_list.append(product.name)
        price_list.append(product.price)

    return name_list, price_list, "Onyxmet", "Poland", "https://onyxmet.com/index.php?route=product/search&search=" + chem