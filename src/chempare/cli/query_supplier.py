"""query supplier"""

import sys
import signal
import os
import inquirer

# from curl_cffi.requests.exceptions import ConnectionError
from chempare import SearchFactory


# Testing single supplier
# from chempare.suppliers import SupplierLaballey, SupplierLabchem, SupplierLabchem, SupplierChemsavers, SupplierOnyxmet
# from chempare.suppliers.supplier_laballey import SupplierLaballey
# from chempare.suppliers.supplier_labchem import SupplierLabchem
# from chempare.suppliers.supplier_chemsavers import SupplierChemsavers
# from chempare.suppliers.supplier_onyxmet import SupplierOnyxmet
# from chempare.suppliers.supplier_esdrei import SupplierEsDrei

# from chempare.suppliers.supplier_synthetika import SupplierSynthetika
# from chempare.suppliers.supplier_tcichemicals import SupplierTciChemicals
# from chempare.suppliers.supplier_ftfscientific import SupplierFtfScientific
# from chempare.suppliers.supplier_loudwolf import SupplierLoudwolf
# from chempare.suppliers.supplier_warchem import SupplierWarchem
# from chempare.suppliers.supplier_laboratoriumdiscounter import (
#     SupplierLaboratoriumDiscounter,
# )
# from chempare.suppliers.supplier_3schem import Supplier3SChem
from chempare.suppliers import *


def signal_handler(sig, frame):
    print("\033[?1049l")
    os.system(f"kill -3 {os.getpid()}")
    raise SystemExit


signal.signal(signal.SIGINT, signal_handler)


def main(supplier_module="SearchFactory", query="water"):
    print(f"Searching supplier {supplier_module} for {query}...")

    product_search = globals()[supplier_module](query)

    print(f"Found {len(product_search)} products for {query}\n")

    for product in product_search:
        for key, value in product.items():
            if value is not None:
                print("{:>15}: {}".format(key, value))
        print("---------")
        print("")


questions = [
    inquirer.List(
        "supplier_module",
        message="Supplier module",
        choices=[
            "SearchFactory",
            "SupplierLaballey",
            "SupplierLabchem",
            "SupplierChemsavers",
            "SupplierOnyxmet",
            "SupplierEsDrei",
            "Supplier3SChem",
            "SupplierSynthetika",
            "SupplierTciChemicals",
            "SupplierFtfScientific",
            "SupplierLoudwolf",
            "SupplierWarchem",
            "SupplierLaboratoriumDiscounter",
        ],
        default="SearchFactory",
    ),
    inquirer.Text("query", message="Query", default="water"),
]


def init():
    # print("\033[?1049h\033[H")

    # try:
    if len(sys.argv) >= 3:
        query_params = {"supplier_module": sys.argv[1], "query": sys.argv[2]}
    else:
        query_params = inquirer.prompt(questions)

    main(**query_params)


# except KeyboardInterrupt:
#     pass
# except ConnectionError:
#     pass
# except SystemExit:
#     pass
# except BaseException:
#     pass
# except BaseException:
#     print("\033[?1049l")
#     os.system(f"kill -3 {os.getpid()}")
#     raise SystemExit
#     return
# finally:
#     os.system(f"kill -3 {os.getpid()}")
#     raise SystemExit

if __name__ == "__main__":
    init()
