from typing import List, Set, Tuple, Dict, Any, Optional
import os, sys, time, math, re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

#import requests
from curl_cffi import requests
from abcplus import ABCMeta, abstractmethod, finalmethod
from dataclasses import dataclass, astuple
from typing import List, Set, Tuple, Dict, Any, Union
#from datatypes import TypeSupplier, TypeProduct

# Todo: this should be automatic
from datatypes.supplier import TypeSupplier
from datatypes.product import TypeProduct

# File: /suppliers/supplier_base.py
class SupplierBase(object, metaclass=ABCMeta):

    _supplier: TypeSupplier = None
    """Supplier specific data"""

    _products: List[TypeProduct] = []
    """List of TypeProduct elements"""

    _limit: int = None
    """Max products to query/return"""

    _cookies: Dict = {}
    """Cookies to use for supplier"""

    _query_results: Any = None
    """Location of cached query result (what other methods pull data from)"""

    allow_cas_search: bool = False
    """Determines if the supplier allows CAS searches in addition to name searches"""

    def __init__(self, query: str, limit: int=None):    
        self._limit = limit
        self._query = query

        # Execute the basic product search (logic should be in inheriting class)
        self._query_products(self._query)

        # Execute the method that parses self._query_results to define the product properties
        self._parse_products()

    """ FINAL methods/properties """

    @property
    @finalmethod 
    def products(self):
        """Product title getter"""
        return self._products

    @finalmethod 
    def http_get(self, path: str, params: Dict=None) -> requests:
        """Base HTTP getter (not specific to data type).

       Args:
            path: URL Path to get (should not include the self._base_url value)
            params: Dictionary of params to use in request (optional)

        Returns:
            Result from requests.get()
        """

        api_url = self._supplier.get('api_url', None)
        base_url = self._supplier.get('base_url', None)

        if base_url not in path and (api_url is None or api_url not in path):
            path = f'{base_url}/{path}'
            
        return requests.get(path, params=params, impersonate="chrome")

    @finalmethod
    def http_get_html(self, path: str, params: Dict=None) -> str:
        """HTTP getter (for HTML content).

        Args:
            path: URL Path to get (should not include the self._base_url value)
            params: Dictionary of params to use in request (optional)

        Returns:
            HTML content of response object
        """

        res = self.http_get(path, params)

        return res.content
    
    @finalmethod
    def http_get_json(self, path: str, params: Dict=None) -> Union[List,Dict]:
        """HTTP getter (for JSON content).

        Args:
            path: URL Path to get (should not include the self._base_url value)
            params: Dictionary of params to use in request (optional)

        Returns:
            JSON object from response body
        """

        api_url = self._supplier.get('api_url', None)
        if api_url is not None:
            path = f'{api_url}/{path}'

        res = self.http_get(path, params)
        return res.json()

    """ ABSTRACT methods/properties """

    @abstractmethod
    def _query_products(self, query: str):
        """Query the website for the products (name or CAS).

        Args:
            query: query string to use

        Returns:
            None

        This should define the self._query_results property with the results
        """
        pass

    @abstractmethod
    def _parse_products(self):
        """Method to set the local properties for the queried product.
        
        The self._query_results (populated by calling self._query_products()) is iterated over
        by this method, which in turn parses each property and creates a new TypeProduct object that
        gets saved to this._products

        Returns:
            None
        """
        pass

    """ GENERAL USE UTILITY METHODS """

    @finalmethod
    def _split_array_into_groups(self, arr: List, size: int=2) -> List:
        """Splits an array into sub-arrays of 2 elements each.

        Args:
            arr: The input array.
            size: Size to group array elements by

        Returns:
            A list of sub-arrays, where each sub-array contains {size} elements, or an empty list if the input array is empty.

        Example:
            self._split_array_into_groups(['Variant', '500 g', 'CAS', '1762-95-4'])
            [['Variant', '500 g'],['CAS', '1762-95-4']]
        """

        result = []
        for i in range(0, len(arr), size):
            result.append(arr[i:i + size])

        return result
    
    @finalmethod
    def _nested_arr_to_dict(self, arr: List) -> Optional[Dict]:
        """Splits an array into sub-arrays of 2 elements each.

        Args:
            arr: The input array.
            size: Size to group array elements by

        Returns:
            A list of sub-arrays, where each sub-array contains {size} elements, or an empty list if the input array is empty.

        Example:
            self._split_array_into_groups(['Variant', '500 g', 'CAS', '1762-95-4'])
            [['Variant', '500 g'],['CAS', '1762-95-4']]
        """

        # Only works if the array has even amount of elements
        if len(arr) % 2 != 0: 
            return None

        grouped_elem = self._split_array_into_groups(arr, 2)

        variant_dict = [dict(item) for item in [grouped_elem]]

        return variant_dict[0] or None
    
    @property
    @finalmethod 
    def _epoch(self) -> int:
        """Get epoch string - Used for unique values in searches (sometimes _)

        Returns:
            int: Current time in epoch
        """
        return math.floor(time.time()*1000)
    
    @finalmethod 
    def _is_cas(self, value:Any) -> bool:
        """Check if a string is a valid CAS registry number

        This is done by taking the first two segments and iterating over them in reverse
        order, multiplying each by their position, then taking the modulous of that number.

        Example:
            1234-56-6 is valid because the result of the below equation matches the checksum
                ((6*1)+(5*2)+(4*3)+(3*4)+(2*5)+(1*6)) % 10 == 6

            This can be simplified in the below aggregation:
                cas_chars = [1, 2, 3, 4, 5, 6]
                sum([(idx+1)*int(n) for idx, n in enumerate(cas_chars[::-1])]) % 10

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


if (__name__ == '__main__' or __name__ == 'suppliers.supplier_base') and __package__ is None:
    __package__ = 'suppliers.supplier_base.SupplierBase'
    __module__ = 'SupplierBase'