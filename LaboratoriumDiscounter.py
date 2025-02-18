import os, sys

SCRIPT_DIR = os.path.dirname(os.path.abspath('suppliers/supplier_laboratoriumdiscounter'))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from suppliers.supplier_laboratoriumdiscounter import SupplierLaboratoriumDiscounter

def fetch_from_lab_dis(chem):
    laboratoriumDiscounter = SupplierLaboratoriumDiscounter(chem)

    name_list = []
    price_list = []

    for product in laboratoriumDiscounter.products[:3]:
        name_list.append(product.name)
        price_list.append(product.price)

    return name_list, price_list, "Laboratoriumdiscounter", "The Netherlands", "https://www.laboratoriumdiscounter.nl/en/search/" + chem + "/"