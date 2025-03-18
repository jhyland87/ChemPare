import os
import sys


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from search_factory import SearchFactory
from suppliers.supplier_3schem import Supplier3SChem
from suppliers.supplier_chemsavers import SupplierChemsavers
from suppliers.supplier_esdrei import SupplierEsDrei
from suppliers.supplier_ftfscientific import SupplierFtfScientific

# Testing single supplier
from suppliers.supplier_laballey import SupplierLaballey
from suppliers.supplier_labchem import SupplierLabchem
from suppliers.supplier_laboratoriumdiscounter import (
    SupplierLaboratoriumDiscounter,
)
from suppliers.supplier_loudwolf import SupplierLoudwolf
from suppliers.supplier_onyxmet import SupplierOnyxmet
from suppliers.supplier_synthetika import SupplierSynthetika
from suppliers.supplier_tcichemicals import SupplierTciChemicals
from suppliers.supplier_warchem import SupplierWarchem


query = sys.argv[1] if len(sys.argv) >= 2 else "water"
supplier_class = sys.argv[2] if len(sys.argv) >= 3 else "SearchFactory"

print(f"Searching supplier {supplier_class} for {query}...")

product_search = eval(supplier_class)(query)

print(f"Found {len(product_search)} products for {query}\n")

for product in product_search:
    for key, value in product.items():
        if value is not None:
            print("{:>15}: {}".format(key, value))
    print("---------")
    print("")
