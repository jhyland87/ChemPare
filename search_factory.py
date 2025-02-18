import os, sys
from abcplus import finalmethod

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import suppliers

class SearchFactory(object):
    # suppliers property lets scripts call 'SearchFactory.suppliers' to get a list of suppliers
    suppliers: list = suppliers.__all__

    __results: list = []

    def __init__(self, query: str, limit: int=3):
        """Factory method for executing a search in all suppliers automatically

        Args:
            query (str): Search query
            limit (int, optional): Limit results to this. Defaults to 3.
        """
        self.__query(query, limit)

    def __query(self, query: str, limit:int =None):
        """Iterates over the suppliers, running the query, then returning the results.

        Args:
            query (str): Search query
            limit (int, optional): Amount to limit the search by. Defaults to None.
        """

        # Iterate over the modules in the suppliers package
        for supplier in suppliers.__all__:
            # Create a direct reference to this supplier class
            supplier_module = getattr(suppliers, supplier)

            if __debug__:
                print(f'Searching for {query} from {supplier_module.__name__}...')
            
            # Execute a search by initializing an instance of the supplier class with
            # the product query term as the first param
            res = supplier_module(query, limit)
            if not res:
                if __debug__:
                    print('  No results found\n')
                next
            
            if __debug__:
                print(f'  found {len(res.products)} products\n')

            # If there were some results found, then extend the self.__results list with those products
            self.__results.extend(res.products)
    
    @property
    @finalmethod 
    def results(self):
        """Results getter"""
        return self.__results