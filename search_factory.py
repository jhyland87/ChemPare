import os, sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import suppliers

def product_search(query):
    all_results = []

    for supplier in suppliers.__all__:
        supplier_module = getattr(suppliers, supplier)
        if __debug__:
            print(f'Searching for {query} from {supplier_module.__name__}...')
        res = supplier_module(query, 2)
        if not res:
            if __debug__:
                print('  No results found\n')
            next
        
        if __debug__:
            print(f'  found {len(res.products)} products\n')
        all_results.extend(res.products)

    return all_results

