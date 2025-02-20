from suppliers.supplier_base import SupplierBase, TypeProduct, TypeSupplier
from typing import List, Set, Tuple, Dict, Any


# File: /suppliers/supplier_3schem.py
class Supplier3SChem(SupplierBase):

    # Supplier specific data
    _supplier: TypeSupplier = dict(
        name = '3S Chemicals LLC',
        location = None,
        base_url = 'https://3schemicalsllc.com'
    )

    # If any extra init logic needs to be called... uncmment the below and add changes
    # def __init__(self, query, limit=123):
    #     super().__init__(id, query, limit)
        # Do extra stuff here

    def _query_product(self, query):
        """Query products from supplier

        Args:
            query (str): Query string to use
        """
        
        # Example request url for 3S Supplier
        # https://3schemicalsllc.com/search/suggest.json?q=clean&resources[type]=product&resources[limit]=6&resources[options][unavailable_products]=last
        # 
        get_params = {
            'q': query,
            'resources[type]':'product',
            # Setting the limit here to 1000, since the limit parameter should apply to
            # results returned from Supplier3SChem, not the rquests made by it. 
            'resources[limit]':1000,
            'resources[options][unavailable_products]':'last'
        }        
        search_result = self.http_get_json('search/suggest.json', get_params)

        if not search_result: 
            return
        
        self._query_results = search_result['resources']['results']['products'][0:self._limit]

    def _parse_products(self):
        """Parse products stored at self._query_results"""
        for product in self._query_results: 
            # Skip unavailable
            if product['available'] is False:
                next
                
            self._products.append(TypeProduct(
                uuid = product['id'],
                name = product['title'],
                title = product['title'],
                price = product['price'],
                url = self._supplier['base_url'] + product['url'],
                supplier = self._supplier['name']
            ))

if __name__ == '__main__' and __package__ is None:
    __name__ = 'suppliers.supplier_3schem'
    __package__ = 'suppliers'
    __module__ = 'Supplier3SChem'
