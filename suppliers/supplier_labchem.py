from suppliers.supplier_base import SupplierBase, Product
from typing import List, Set, Tuple, Dict, Any
from bs4 import BeautifulSoup
import re

# File: /suppliers/supplier_labchem.py
class SupplierLabchem(SupplierBase):

    # Supplier specific data
    _supplier: Dict = dict(
        name = 'Labchem',
        #location = 'Poland',
        base_url = 'https://www.labchem.com/'
    )

    # If any extra init logic needs to be called... uncmment the below and add changes
    # def __init__(self, query, limit=123):
    #     super().__init__(id, query, limit)
        # Do extra stuff here

    def _query_product(self, query: str):
        """Query products from supplier

        Args:
            query (str): Query string to use
        """
        # Example request url for Labchem Supplier
        # https://www.labchem.com/AutoComplete.slt?q=mercury&limit=20
        #
        get_params = {
            'limit':self._limit,
            'q': query,
            'timestamp':1739971044228,
            'width': '395px',
            '_': 1739962847766
        }    

        search_result = self.http_get_json('AutoComplete.slt', get_params)

        if not search_result: 
            return
        
        self._query_results = search_result['response']['docs']['item'][0:self._limit]

    def _parse_products(self):
        """Parse product query results.

        Iterate over the products returned from self._query_product, creating new requests
        for each to get the HTML content of the individual product page, and creating a 
        new Product object for each to add to _products

        Todo:
            Have this execute in parallen using AsyncIO        
        """

        for product in self._query_results:
            #self._products.append(self._query_and_parse_product(product['href']))
            price = self._query_product_price(product['partnumber'])
            self._products.append(Product(
                title = product['custom_CHEMICAL_NAME'],
                name = product['custom_CHEMICAL_NAME'],
                price = price,
                brand = product['brand'],
                supplier = self._supplier['name']
            ))

    def _query_product_price(self, partnumber:str) -> str:
        """Query specific product price

        Args:
            partnumber (str): partnumber of chem to query for

        Returns:
            Product: Price of product
        """

        params = {
            'productIdList':partnumber
        }
        product_json = self.http_get_json('getPriceDetailPage.action', params=params)
        
        return product_json[0]['listPrice']

if __name__ == '__main__' and __package__ is None:
    __name__ = 'suppliers.supplier_labchem'
    __package__ = 'suppliers'
    __module__ = 'SupplierLabchem'
