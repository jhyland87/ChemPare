import os, sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from search_factory import SearchFactory

query = 'mercury'

print(f'Searching {len(SearchFactory.suppliers)} suppliers for "{query}"...')

product_search = SearchFactory(query)

print('\n\n')
print(f'RESULTS: - Found {len(product_search.results)} results for "{query}":\n')

for product in product_search.results:
    if product.name: print('  Supplier:', product.supplier) 
    if product.name: print('  Name:', product.name) 
    if product.price: print('  Price:', product.price)
    if product.url: print('  URL:', product.url)
    if product.cas: print('  CAS:', product.cas)
    print('')