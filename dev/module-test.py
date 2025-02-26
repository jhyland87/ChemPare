#!/usr/bin/env python3 

import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from search_factory import SearchFactory

# Testing single supplier
# from suppliers.supplier_laballey import SupplierLaballey
# from suppliers.supplier_labchem import SupplierLabchem
# from suppliers.supplier_chemsavers import SupplierChemsavers
#from suppliers.supplier_onyxmet import SupplierOnyxmet
#from suppliers.supplier_synthetika import SupplierSynthetika
#from suppliers.supplier_tcichemicals import SupplierTciChemicals
#from suppliers.supplier_ftfscientific import SupplierFtfScientific
#from suppliers.supplier_loudwolf import SupplierLoudwolf
from suppliers.supplier_warchem import SupplierWarchem


query = sys.argv[1] if len(sys.argv) >= 2 else 'benz'
print(f'Searching for {query}...')
product_search = SupplierWarchem(query)

print(f'Found {len(product_search)} products for {query}\n')

for product in product_search:
    #print('product:',product)
    #print(f'\tTitle: {product.title}')
    for key, value in product.items():
        if value is not None:
            print('{:>15}: {}'.format(key,value))
    print('---------')
    print('')

# for p in search:
#     print('\n\np:', p)

# print('len(search.products):', len(search.products))
# for product in search.products:
#     for key, value in product.items():
#         if value is not None:
#             print('{:>12}: {:12}'.format(key,value))
#             #print(f"{key}: {value}")
#     print('---------')
#     print('')

#print('search:',search.products)
# for p in search.products:
#     print(p)
#     # print('name:', p.name)
#     # print('price:', p.price)
#     # print('currency:', p.currency)
#     # print('quantity:', p.quantity)
#     # print('uom:', p.uom)
#     print('\n')


# product_search = SearchFactory(query)

# for product in product_search:
#     #print('{:>25}: {}'.format(product.supplier,product.title))
#     for key, value in product.items():
#         if value is not None:
#             print('{:>15}: {}'.format(key,value))
#     print('---------')
#     print('')