#!/usr/bin/env python3 -O
import sys
import inquirer
from chempare.search_factory import SearchFactory


# Testing single supplier
from chempare.suppliers.supplier_laballey import SupplierLaballey
from chempare.suppliers.supplier_labchem import SupplierLabchem
from chempare.suppliers.supplier_chemsavers import SupplierChemsavers
from chempare.suppliers.supplier_onyxmet import SupplierOnyxmet
from chempare.suppliers.supplier_esdrei import SupplierEsDrei

from chempare.suppliers.supplier_synthetika import SupplierSynthetika
from chempare.suppliers.supplier_tcichemicals import SupplierTciChemicals
from chempare.suppliers.supplier_ftfscientific import SupplierFtfScientific
from chempare.suppliers.supplier_loudwolf import SupplierLoudwolf
from chempare.suppliers.supplier_warchem import SupplierWarchem
from chempare.suppliers.supplier_laboratoriumdiscounter import (
    SupplierLaboratoriumDiscounter,
)
from chempare.suppliers.supplier_3schem import Supplier3SChem

def main(supplier_module="SearchFactory", query="water"):
    print(f"Searching supplier {supplier_module} for {query}...")

    product_search = eval(supplier_module)(query)

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
        default="SearchFactory"
    ),
    inquirer.Text("query", message="Query", default="water"),
]

def init():
    if len(sys.argv) >= 3:
        query_params = {
            "supplier_module": sys.argv[1],
            "query": sys.argv[2]
        }
    else:
        query_params = inquirer.prompt(questions)

    main(**query_params)
if __name__ == "__main__":
    init()