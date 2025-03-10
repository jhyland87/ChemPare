
from datatypes.product import TypeProduct
import suppliers
from typing import Optional, List, NoReturn
from curl_cffi import requests
from abcplus import finalmethod
from class_utils import ClassUtils
# import os
# import sys
# SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(os.path.dirname(SCRIPT_DIR))

class SearchFactory(ClassUtils, object):
    suppliers: List = suppliers.__all__
    """suppliers property lets scripts call 'SearchFactory.suppliers' to get a list of suppliers"""

    __results: List = None
    """Contains a list of all the product results"""

    __index: int = 0
    """Index used for __iter__ iterations"""

    def __init__(self, query: str, limit: int=3) -> NoReturn:
        """Factory method for executing a search in all suppliers automatically

        Args:
            query (str): Search query
            limit (int, optional): Limit results to this. Defaults to 3.
        """

        self.__results = []

        self.__query(query, limit)

    def __iter__(self):
        """Simple iterator, making this object usable in for loops"""

        return self

    def __next__(self) -> TypeProduct:
        """Next dunder method for for loop iterations

        Raises:
            StopIteration: When the results are done

        Returns:
            TypeProduct: Individual products
        """

        if self.__index >= len(self.__results):
            raise StopIteration

        value = self.__results[self.__index]
        self.__index += 1

        return value

    def __len__(self) -> int:
        """Result to return when len() is used

        Returns:
            int: Number of results from the last query
        """

        return len(self.__results)

    def __query(self, query: str, limit: int=None) -> NoReturn:
        """Iterates over the suppliers, running the query, then returning the results.

        Args:
            query (str): Search query
            limit (int, optional): Amount to limit the search by. Defaults to None.
        """

        query_is_cas = self._is_cas(query)

        # Get both the chemical name and CAS values for searches, to avoid having to make
        # the same HTTP calls to cactus.nci.nih.gov several times
        if query_is_cas is True:
            query_cas = query
            # Use self.__get_name() to get the IUPAC name.
            # Example: '67-64-1' yields 'propan-2-one'
            #query_name = self.__get_name(query) or query

            # Use self.__get_popular_name(query) to try and determine the most common name.
            # Example: '67-64-1' yields 'acetone'
            query_name = self.__get_popular_name(query) or query
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
                if supplier_module.allow_cas_search is True:
                    res = supplier_module(query_name, limit)
                    if __debug__:
                        print(f'Searching for {query_name} from {supplier_module.__name__}...')
                if not res:
                    if __debug__:
                        print('  No results found\n')
                    continue

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

        cas = None
        try:
            # Send a GET request to the API
            cas_request = requests.get(f'https://cactus.nci.nih.gov/chemical/structure/{chem_name}/cas')
            # Check if the request was successful
            if cas_request.status_code != 200:
                return None

            # Decode the bytes to a string
            cas_response = cas_request.content.decode('utf-8')

            if not cas_response:
                return None

            cas_list = cas_response.split('\n')
            cas = cas_list[0]
        except Exception as e:
            print('Failed to get CAS #', e)

        return cas

        # # Should only be one line/value, so just strip it before returning, if a value was found
        # return str(cas_response).strip() if cas_response else None

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

    def __get_popular_name(self, query:str) -> str:
        """Get the most frequently used name for a chemical from a list of its aliases

        Args:
            query (str): Chemical name or CAS

        Returns:
            str: The most frequently found name
        """
        # Send a GET request to the API
        name_request = requests.get(f'https://cactus.nci.nih.gov/chemical/structure/{query}/names')

        # Check if the request was successful
        if name_request.status_code != 200:
            raise SystemError(f"Error: {name_request.status_code}")

        name_response = name_request.content.decode('utf-8')  # Decode the bytes to a string
        name_lines = name_response.split('\n')  # Split by newline

        highest_val = self._filter_highest_value(self._get_common_phrases(name_lines))

        keys = list(highest_val.keys())
        return keys[0][0]

    @property
    @finalmethod
    def results(self) -> List[TypeProduct]:
        """Results getter

        Returns:
            List[TypeProduct]: List of the aggregated TypeProduct objects from each supplier
        """
        return self.__results