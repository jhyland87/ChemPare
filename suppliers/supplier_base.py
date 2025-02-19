import os, sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

#import requests
from curl_cffi import requests
from abcplus import ABCMeta, abstractmethod, finalmethod
from dataclasses import dataclass, astuple
from typing import List, Set, Tuple, Dict, Any, Union
from datatypes.product import Product


# File: /suppliers/supplier_base.py
class SupplierBase(object, metaclass=ABCMeta):

    # Supplier specific data
    _supplier: Dict = dict(
        name = 'Base Supplier',
        location = None,
        base_url = None
    )

    # List of Product elements
    _products: List[Product] = []

    _limit: int = None

    # Cookies to use for supplier
    _cookies: Dict = {}

    # Location of cached query result (what other methods pull data from)
    _query_results: Any = None

    # Default headers to include in requests
    _headers: Dict = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.7',
        # 'cookie': 'OCSESSID=e7d2642d83310cfc58135d2914; language=en-gb; currency=USD',
        'priority': 'u=0, i',
        #'referer': 'https://onyxmet.com/',
        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Brave";v="132"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'sec-gpc': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    }

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

        if self._supplier.get('base_url') not in path:
            path = '{0}/{1}'.format(self._supplier.get('base_url'), path)
            
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
        by this method, which in turn parses each property and creates a new Product object that
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

if (__name__ == '__main__' or __name__ == 'suppliers.supplier_base') and __package__ is None:
    __package__ = 'suppliers.supplier_base.SupplierBase'
    __module__ = 'SupplierBase'