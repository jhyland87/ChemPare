import os, sys
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath('suppliers/supplier_laboratoriumdiscounter'))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from suppliers.supplier_laboratoriumdiscounter import SupplierLaboratoriumDiscounter

def fetch_from_lab_dis(chem):
    laboratoriumDiscounter = SupplierLaboratoriumDiscounter(chem, 3)

    name_list = []
    price_list = []
    quantity_list = []

    pattern = r"^(.*) (-\s)?([0-9,]+)(k?g|[cmμ]m)"

    for product in laboratoriumDiscounter.products[:3]:
        name_list.append(product.name)
        price_list.append(product.price)

        quantity = None
        try:
            quantity = re.match(pattern, product.name).group(3) + re.match(pattern, product.name).group(4)
        except:
            quantity = ""
        quantity_list.append(quantity)

    return name_list, price_list, "Laboratoriumdiscounter", "The Netherlands", "https://www.laboratoriumdiscounter.nl/en/search/" + chem + "/", quantity_list