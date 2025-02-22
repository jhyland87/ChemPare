
import os, sys
from typing import List, Set, Tuple, Dict, Any, Optional
from curl_cffi import requests
from abcplus import finalmethod

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import suppliers

class SearchFactory(object):
    suppliers: list = suppliers.__all__
    """suppliers property lets scripts call 'SearchFactory.suppliers' to get a list of suppliers"""

    __results: list = []
    """Contains a list of all the product results"""

    def __init__(self, query: str, limit: int=3):
        """Factory method for executing a search in all suppliers automatically

        Args:
            query (str): Search query
            limit (int, optional): Limit results to this. Defaults to 3.
        """
        self.__query(query, limit)

    def __query(self, query: str, limit: int=None):
        """Iterates over the suppliers, running the query, then returning the results.

        Args:
            query (str): Search query
            limit (int, optional): Amount to limit the search by. Defaults to None.
        """

        # Iterate over the modules in the suppliers package
        for supplier in suppliers.__all__:
            # Create a direct reference to this supplier class
            supplier_module = getattr(suppliers, supplier)
            supplier_query = query

            # If the supplier allows a cas search, then do the cas lookup and try to use that
            if supplier_module.allow_cas_search is True:
                supplier_query = self.__get_cas(query) or query
               
            if __debug__:
                print(f'Searching for {supplier_query} from {supplier_module.__name__}...')

            # Execute a search by initializing an instance of the supplier class with
            # the product query term as the first param
            res = supplier_module(supplier_query, limit)
            if not res:
                if __debug__:
                    print('  No results found\n')
                next
            
            if __debug__:
                print(f'  found {len(res.products)} products\n')

            # If there were some results found, then extend the self.__results list with those products
            self.__results.extend(res.products)
    
    def __get_cas(self, chem_name:str) -> Optional[str]:
        """Search for the CAS value(s) given a chemical name

        Args:
            chem_name (str): Name of chemical to search for

        Returns:
            Optional[str]: CAS value of chemical
        """
        
        # Send a GET request to the API
        cas_request = requests.get(f'https://cactus.nci.nih.gov/chemical/structure/{chem_name}/cas')
        
        # Check if the request was successful
        if cas_request.status_code != 200:
            return f"Error: {cas_request.status_code}"
        
        cas_response = cas_request.content.decode('utf-8')  # Decode the bytes to a string
        cas_lines = cas_response.split('\n')  # Split by newline
            
        # Do we want the first value?
        return cas_lines[0]
        
        # Or the last?
        #return cas_lines[-1]
        
    @property
    @finalmethod 
    def results(self):
        """Results getter"""
        return self.__results