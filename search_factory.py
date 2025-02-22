
import os, sys, re
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

        query_is_cas = self.__is_cas(query)

        # Get both the chemical name and CAS values for searches, to avoid having to make
        # the same HTTP calls to cactus.nci.nih.gov several times
        if query_is_cas is True:
            query_cas = query
            query_name = self.__get_name(query) or query
        else:
            query_cas = self.__get_cas(query) or query
            query_name = query

        # Iterate over the modules in the suppliers package
        for supplier in suppliers.__all__:
            # Create a direct reference to this supplier class
            supplier_module = getattr(suppliers, supplier)
            supplier_query = query

            # If the supplier allows a CAS search and the current value isn't a CAS number...
            if supplier_module.allow_cas_search is True and query_is_cas is False:
                # ... Then do a lookup to get the CAS number
                supplier_query = query_cas
            # If the supplier does not allow CAS searches, but were searching by CAS..
            elif supplier_module.allow_cas_search is False and query_is_cas is True:
                # ... Then try to lookup the name for this
                supplier_query = query_name
               
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
        
        # Decode the bytes to a string
        cas_response = cas_request.content.decode('utf-8')  

        # Should only be one line/value, so just strip it before returning, if a value was found
        return str(cas_response).strip() if cas_response else None
       
    def __get_name(self, cas_no:str) -> Optional[str]:
        """Search for a chemical name given a CAS #

        Args:
            cas_no (str): CAS #

        Returns:
            Optional[str]: IUPAC name
        """
           
        # Send a GET request to the API
        name_request = requests.get(f'https://cactus.nci.nih.gov/chemical/structure/{cas_no}/iupac_name')
        
        # Check if the request was successful
        if name_request.status_code != 200:
            return f"Error: {name_request.status_code}"
        
        name_response = name_request.content.decode('utf-8')  # Decode the bytes to a string
        name_lines = name_response.split('\n')  # Split by newline
            
        # Do we want the first value?
        return name_lines[0]
    
    def __is_cas(self, value:Any) -> bool:
        """Check if a string is a valid CAS registry number

        This is done by taking the first two segments and iterating over each individual
        intiger in reverse order, multiplying each by its position, then taking the 
        modulous of the sum of those values.

        Example:
            1234-56-6 is valid because the result of the below equation matches the checksum,
            (which is 6)
                (6*1 + 5*2 + 4*3 + 3*4 + 2*5 + 1*6) % 10 == 6

            This can be simplified in the below aggregation:
                cas_chars = [1, 2, 3, 4, 5, 6]
                sum([(idx+1)*int(n) for idx, n in enumerate(cas_chars[::-1])]) % 10

        See: 
            https://www.cas.org/training/documentation/chemical-substances/checkdig

        Args:
            value (str): The value to determine if its a CAS # or not

        Returns:
            bool: True if its a valid format and the checksum matches
        """

        if type(value) is not str:
            return False
        
        # value='1234-56-6'
        # https://regex101.com/r/xPF1Yp/2
        cas_pattern_check = re.match(r'^(?P<seg_a>[0-9]{2,7})-(?P<seg_b>[0-9]{2})-(?P<checksum>[0-9])$', value)

        if cas_pattern_check is None:
            return False

        cas_dict = cas_pattern_check.groupdict()
        # cas_dict = dict(seg_a='1234', seg_b='56', checksum='6')

        cas_chars = list(cas_dict['seg_a'] + cas_dict['seg_b'])
        # cas_chars = ['1','2','3','4','5','6']

        checksum = sum([(idx+1)*int(n) for idx, n in enumerate(cas_chars[::-1])]) % 10
        # checksum = 6

        return int(checksum) == int(cas_dict['checksum'])
    
    @property
    @finalmethod 
    def results(self):
        """Results getter"""
        return self.__results