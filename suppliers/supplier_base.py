import os
import sys
from typing import List, Dict, Any, Union
from curl_cffi import requests
from abcplus import ABCMeta, abstractmethod, finalmethod
from class_utils import ClassUtils

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

#from datatypes import TypeSupplier, TypeProduct

# Todo: this should be automatic
from datatypes.supplier import TypeSupplier
from datatypes.product import TypeProduct

# File: /suppliers/supplier_base.py
class SupplierBase(ClassUtils, metaclass=ABCMeta):

    #_supplier: TypeSupplier = None
    """Supplier specific data"""

    #_products: List[TypeProduct] = []
    """List of TypeProduct elements"""

    _limit: int = None
    """Max products to query/return"""

    #_cookies: Dict = {}
    """Cookies to use for supplier"""

    #_index: int = 0
    """Index value used for __iter__ dunder method (for loop iteration)"""

    #_query_results: Any = None
    """Location of cached query result (what other methods pull data from)"""

    allow_cas_search: bool = False
    """Determines if the supplier allows CAS searches in addition to name searches"""

    language_for_search: Any = None
    """For what language it should use for the search query"""

    def __init__(self, query: str, limit:int=None):    
        if limit is not None:
            self._limit = limit

        self._products = []
        self._query_results = []
        self._index = 0
        self._query = query
        self._cookies = {}
        self._headers = {}

        if hasattr(self, '_setup'):
            self._setup(query)

        # Execute the basic product search (logic should be in inheriting class)
        self._query_products(self._query)

        # Execute the method that parses self._query_results to define the product properties
        self._parse_products()

    def __len__(self):
        return len(self._products)
    
    def __iter__(self):
        return self

    def __next__(self) -> TypeProduct:
        if self._index >= len(self._products):
            raise StopIteration
        value = self._products[self._index]
        self._index += 1
        return value
    
    """ FINAL methods/properties """

    @property
    @finalmethod 
    def products(self):
        """Product title getter"""
        return self._products

    @finalmethod 
    def http_get(
            self, 
            path:str=None, 
            params:Dict=None,
            cookies:Dict=None,
            headers:Dict=None) -> requests:
        """Base HTTP getter (not specific to data type).

       Args:
            path: URL Path to get (should not include the self._base_url value)
            params: Dictionary of params to use in request (optional)

        Returns:
            Result from requests.get()
        """
        
        base_url = self._supplier.get('base_url', None)
        api_url = self._supplier.get('api_url', base_url)

        if not path:
            path = api_url
        elif api_url not in path:
            path=f'{api_url}/{path}'

        return requests.get(path, 
                            params=params, 
                            impersonate="chrome", 
                            cookies=cookies or self._cookies, 
                            headers=headers or self._headers)
    
    @finalmethod 
    def http_post(
            self, 
            path: str, 
            params: Dict=None, 
            data: Any=None, 
            json: Union[Dict, List]=None,
            cookies:Dict=None,
            headers:Dict=None) -> requests:
        """Base HTTP poster (not specific to data type).

       Args:
            path: URL Path to post (should not include the self._base_url value)
            params: Dictionary of params to use in request (optional)
            body: Body of data to post (text, json, etc)

        Returns:
            Result from requests.post()
        """

        api_url = self._supplier.get('api_url', None)
        base_url = self._supplier.get('base_url', None)

        if base_url not in path and (api_url is None or api_url not in path):
            path = f'{base_url}/{path}'
            
        return requests.post(path, 
                             params=params, 
                             impersonate="chrome", 
                             json=json,
                             data=data,
                             headers=headers or self._headers,
                             cookies=cookies or self._cookies)

    @finalmethod
    def http_get_headers(
            self,
            **kwargs) -> requests.Headers:
        """Get the response headers for a GET request

        Returns:
            requests.Headers: Header object
        """
        
        resp = self.http_get(**kwargs)

        return resp.headers 

    @finalmethod 
    def http_post_json(
            self, 
            path:str=None, 
            params:Dict=None,
            json:Dict=None,
            headers:Dict=None,
            cookies:Dict=None) -> Union[Dict, List]:
        """Post a JSON request and get a JSON response

        Args:
            path (str, optional): Path to post to. Defaults to None.
            params (Dict, optional): params object. Defaults to None.
            json (Dict, optional): json body. Defaults to None.
            headers (Dict, optional): override headers. Defaults to None.
            cookies (Dict, optional): override cookies. Defaults to None.

        Returns:
            Union[Dict, List]: JSON response, if there was one
        """

        url = self._supplier.get('api_url', None)

        if path:
            url=f'{url}/{path}'

        req = self.http_post(url, 
                             params=params, 
                             json=json, 
                             cookies=cookies or self._cookies,
                             headers=headers or self._headers)
        if req is None:
            return None
        
        return req.json()
    
    @finalmethod
    def http_get_html(self, 
                      path:str=None, 
                      params:Dict=None) -> str:
        """HTTP getter (for HTML content).

        Args:
            path: URL Path to get (should not include the self._base_url value)
            params: Dictionary of params to use in request (optional)

        Returns:
            HTML content of response object
        """

        base_url = self._supplier.get('base_url', None)
        api_url = self._supplier.get('api_url', base_url)

        if path and api_url not in path:
            path=f'{api_url}/{path}'

        res = self.http_get(path, params)

        return res.content
    
    @finalmethod
    def http_get_json(self, path:str=None, **kwargs) -> Union[List,Dict]:
        """HTTP getter (for JSON content).

        Args:
            path: URL Path to get (should not include the self._base_url value)
            params: Dictionary of params to use in request (optional)

        Returns:
            JSON object from response body
        """

        # api_url = self._supplier.get('api_url', None)
        # if api_url:
        #     path = f'{api_url}/{path}'
        #print(kwargs)
        #return {}
        res = self.http_get(path, **kwargs)

        if not res:
            return None
        
        return res.json()
    
    def _setup(self, query:str=None):
        pass
    
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

if __package__ == 'suppliers':
    __disabled__ = True