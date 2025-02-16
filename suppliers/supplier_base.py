import requests
from abcplus import ABCMeta, abstractmethod, finalmethod

# File: /suppliers/supplier_base.py
class SupplierBase(object, metaclass=ABCMeta):
    
    # Supplier specific data
    _supplier = dict(
        name = 'Base Supplier',
        location = None,
        base_url = None
    )

    # Product specific details
    _product = dict(
        title = None,
        name = None,
        price = None,
        purity = None,
        quantity = None,
        uom = None
    )

    # Cookies to use for supplier
    _cookies = {}

    # Location of cached query result (what other methods pull data from)
    _query_result = None

    # Default headers to include in requests
    _headers = {
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

    def __init__(self, query):
        # Execute the basic product search (logic should be in inheriting class)
        self._query_result = self._query_product(query)

        # Execute the method that parses self._query_result to define the product properties
        self._set_values()

    """ FINAL methods/properties """

    @property
    @finalmethod 
    def title(self):
        """Product title getter"""
        return self._product.get('title')

    @property
    @finalmethod 
    def name(self):
        """Product name getter"""
        return self._product.get('name')

    @property
    @finalmethod 
    def price(self):
        """Product price getter"""
        return self._product.get('price')
    
    @property
    @finalmethod 
    def purity(self):
        """Product purity getter"""
        return self._product.get('purity')
    
    @property
    @finalmethod 
    def quantity(self):
        """Product quantity getter"""
        return self._product.get('quantity')
    
    @property
    @finalmethod 
    def uom(self):
        """Product UOM (Unit Of Measure) getter"""
        return self._product.get('uom')
    
    @finalmethod 
    def http_get(self, path, params=None):
        """Base HTTP getter (not specific to data type).

        Keyword arguments:
        path -- URL Path to get (should not include the self._base_url value)
        params -- Dictionary of params to use in request (optional)
        """
        if self._supplier.get('base_url') not in path:
            path = '{0}/{1}'.format(self._supplier.get('base_url'), path)
            
        return requests.get(path, cookies=self._cookies, headers=self._headers, params=params)

    @finalmethod
    def http_get_html(self, path, params=None):
        """HTTP getter (for HTML content).

        Keyword arguments:
        path -- URL Path to get (should not include the self._base_url value)
        params -- Dictionary of params to use in request (optional)
        """
        res = self.http_get(path, params)

        return res.content
    
    @finalmethod
    def http_get_json(self, path, params=None):
        """HTTP getter (for JSON content).

        Keyword arguments:
        path -- URL Path to get (should not include the self._base_url value)
        params -- Dictionary of params to use in request (optional)
        """
        res = self.http_get(path, params)
        return res.json()

    """ ABSTRACT methods/properties """

    @abstractmethod
    def _query_product(self, query):
        """Query the website for the product (name or CAS).

        Keyword arguments:
        query -- query string to use
        """
        pass

    @abstractmethod
    def _set_values(self):
        """Method to set the local properties for the queried product."""
        pass

if __name__ == '__main__' and __package__ is None:
    __package__ = 'suppliers.supplier_base.SupplierBase'