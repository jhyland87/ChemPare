import os, sys
from abcplus import finalmethod

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import suppliers

class SearchFactory(object):
    # suppliers property lets scripts call 'SearchFactory.suppliers' to get a list of suppliers
    suppliers = suppliers.__all__

    __results: list = []

    def __init__(self, query, limit=3):
        """Init for SearchFactory
        
        Args:
            query: Search query
            limit: Amount to limit the search by
        """
        
        self.__query(query, limit)

    def __query(self, query, limit=None):
        """Query function (private)
        
        Iterates over the suppliers, running the query, then returning the results.

        Args:
            query: Search query
            limit: Amount to limit the search by

        Returns:
            List of Product elements
        """

        for supplier in suppliers.__all__:
            supplier_module = getattr(suppliers, supplier)
            if __debug__:
                print(f'Searching for {query} from {supplier_module.__name__}...')
            res = supplier_module(query, limit)
            if not res:
                if __debug__:
                    print('  No results found\n')
                next
            
            if __debug__:
                print(f'  found {len(res.products)} products\n')
            self.__results.extend(res.products)

        return self.__results
    
    @property
    @finalmethod 
    def results(self):
        """Results getter"""
        return self.__results