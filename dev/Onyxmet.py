import os, sys
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath('suppliers/supplier_onyxmet'))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from chempare.suppliers.supplier_onyxmet import SupplierOnyxmet

def fetch_from_onyxmet(chem):
    onyxmet = SupplierOnyxmet(chem, 3)

    name_list = []
    price_list = []
    quantity_list = []

    pattern = r"^(.*) (-\s)?([0-9,]+)(k?g|[cmμ]m)"

    for product in onyxmet.products[:3]:
        name_list.append(product.name)
        price_list.append(product.price)

        quantity = None
        try:
            quantity = re.match(pattern, product.name).group(3) + re.match(pattern, product.name).group(4)
        except:
            quantity = ""
        quantity_list.append(quantity)

    return name_list, price_list, "Onyxmet", "Poland", "https://onyxmet.com/index.php?route=product/search&search=" + chem, quantity_list