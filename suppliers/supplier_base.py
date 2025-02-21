import os, sys, time, math

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

    def __init__(self, query: str, limit: int=None):
        # Set the limit for how many results to iterate over
        self._limit = limit

        # Execute the basic product search (logic should be in inheriting class)
        self._query_product(query)

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
    def _query_product(self, query: str):
        """Query the website for the product (name or CAS).

        This should define the self._query_results property with the results

        Args:
            query: query string to use

        Returns:
            None
        """

        pass

    @abstractmethod
    def _parse_products(self):
        """Method to set the local properties for the queried product.
        
        The self._query_results (populated by calling self._query_product()) is iterated over
        by this method, which in turn parses each property and creates a new TypeProduct object that
        gets saved to this._products

        Returns:
            None
        """
        pass

    """ GENERAL USE UTILITY METHODS """

    @finalmethod
    def _split_array_into_groups(self, arr: list, size: int=2):
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
    def _nested_arr_to_dict(self, arr: list):
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
        """Get epoch string"""
        return math.floor(time.time()*1000)

if (__name__ == '__main__' or __name__ == 'suppliers.supplier_base') and __package__ is None:
    __package__ = 'suppliers.supplier_base.SupplierBase'
    __module__ = 'SupplierBase'