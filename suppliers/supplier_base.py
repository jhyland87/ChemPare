import requests
from abcplus import ABCMeta, abstractmethod, finalmethod

# File: /suppliers/supplier_base.py
class SupplierBase(object, metaclass=ABCMeta):
    _name = None
    _base_url = None
    _cookies = {}
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
    _search_cache = {}

    def __init__(self):
        pass

    @property
    def name(self):
        return self._name

    @abstractmethod
    def search_products(self, query):
        pass

    @abstractmethod
    def get_product(self, name):
        pass

    @abstractmethod
    def get_product_price(self, name):
        pass

    @finalmethod 
    def http_get(self, path, params):
        get_url = '{0}/{1}'.format(self._base_url, path)
        return requests.get(get_url, cookies=self._cookies, headers=self._headers, params=params)

    @finalmethod
    def http_get_html(self, path, params):
        res = self.http_get(path, params)
        return res.content
    
    @finalmethod
    def http_get_json(self, path, params):
        res = self.http_get(path, params)
        return res.json()

if __name__ == "__main__" and __package__ is None:
    __package__ = "suppliers.supplier_base.SupplierBase"