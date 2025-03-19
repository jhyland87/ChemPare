"""query supplier"""

# pylint: disable=unused-import
# pylint: disable=unused-wildcard-import
# pylint: disable=wildcard-import
# pylint: disable=missing-function-docstring
# pylint: disable=unused-argument


import os
import signal
import sys

import inquirer

# from curl_cffi.requests.exceptions import ConnectionError
from chempare import SearchFactory  # noqa: F401
from chempare.suppliers import *  # noqa: F401,F403


def signal_handler(sig, frame):
    print(f"Trapped signal {sig}")
    print("\033[?1049l")
    os.system(f"kill -3 {os.getpid()}")
    raise SystemExit


signal.signal(signal.SIGINT, signal_handler)


def main(supplier="SearchFactory", query="water"):
    print(f"Searching supplier {supplier} for {query}...")

    product_search = globals()[supplier](query)

    print(f"Found {len(product_search)} products for {query}\n")

    for product in product_search:
        for key, value in product.items():
            if value is not None:
                print(f"{key:>15}: {value}")
        print("---------")
        print("")


questions = [
    inquirer.List(
        "supplier",
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
