import os, sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

# Testing single supplier
# from suppliers.supplier_laballey import SupplierLaballey
# from suppliers.supplier_labchem import SupplierLabchem
# from suppliers.supplier_chemsavers import SupplierChemsavers

#print('allow_cas_search:',SupplierLabchem.allow_cas_search)
#search = SupplierChemsavers('toluene')

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
from search_factory import SearchFactory

# print(f'Searching {len(SearchFactory.suppliers)} suppliers for "{query}"...')p
product_search = SearchFactory('67-64-1')

# print('\n\n')
# print(f'RESULTS: - Found {len(product_search.results)} results for "{query}":\n')

for product in product_search.results:
    # if product.name: print('  Supplier:', product.supplier) 
    # if product.name: print('  Name:', product.name) 
    # if product.price: print('  Price:', product.price)
    # if product.url: print('  URL:', product.url)
    # if product.cas: print('  CAS:', product.cas)
    for key, value in product.items():
        if value is not None:
            print('{:>12}: {:12}'.format(key,value))
    print('---------')
    print('')