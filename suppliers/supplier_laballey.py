from suppliers.supplier_base import SupplierBase, TypeProduct, TypeSupplier
from typing import List, Set, Tuple, Dict, Any
import re

# File: /suppliers/supplier_laboratoriumdiscounter.py
class SupplierLaballey(SupplierBase):

    _supplier: TypeSupplier = dict(
        name = 'Laballey',
        location = None,
        base_url = 'https://www.laballey.com',
        api_url = 'https://searchserverapi.com',
        api_key = '8B7o0X1o7c'
    )
    """Supplier specific data"""

    allow_cas_search: bool = True
    """Determines if the supplier allows CAS searches in addition to name searches"""

    # If any extra init logic needs to be called... uncmment the below and add changes
    # def __init__(self, query, limit=123):
    #     super().__init__(id, query, limit)
        # Do extra stuff here

    def _query_products(self, query: str):
        """Query products from supplier

        Args:
            query (str): Query string to use
        """
        print('self._supplier.api_key:',self._supplier['api_key'])

        # Example request url for Laboratorium Discounter
        # https://searchserverapi.com/getwidgets?api_key=8B7o0X1o7c&q=sulf&maxResults=6&startIndex=0&items=true&pages=true&facets=false&categories=true&suggestions=true&vendors=false&tags=false&pageStartIndex=0&pagesMaxResults=3&categoryStartIndex=0&categoriesMaxResults=3&suggestionsMaxResults=4&vendorsMaxResults=3&tagsMaxResults=3&output=json&_=1740051794061
        # 
        get_params = {
            # Setting the limit here to 1000, since the limit parameter should apply to
            # results returned from Supplier3SChem, not the rquests made by it. 
            'api_key': self._supplier['api_key'],
            'q':query,
            'maxResults': 6,
            'startIndex': 0,
            'items': True,
            'pages': False,
            'facets':False,
            'categories': True,
            'suggestions': True,
            'vendors':False,
            'tags':False,
            'pageStartIndex':0,
            'pagesMaxResults':10,
            'categoryStartIndex': 0,
            'categoriesMaxResults': 3,
            'suggestionsMaxResults': 4,
            'vendorsMaxResults': 3,
            'tagsMaxResults': 3,
            'output': 'json',
            '_': self._epoch    
        }

        search_result = self.http_get_json(f'getwidgets', get_params)

        if not search_result: 
            return
        
        self._query_results = search_result['items'][0:self._limit]
    
    # Method iterates over the product query results stored at self._query_results and 
    # returns a list of TypeProduct objects.
    def _parse_products(self):
        #print('self._query_results:',self._query_results)
        for product_obj in self._query_results: 

            # Add each product to the self._products list in the form of a TypeProduct
            # object.
            self._products.append(self._parse_product(product_obj))

    def _parse_product(self, product_obj:Tuple[List, Dict]) -> TypeProduct:
        """Parse single product and return single TypeProduct object

        Args:
            product_obj (Tuple[List, Dict]): Single product object from JSON body

        Returns:
            TypeProduct: Instance of TypeProduct

        Todo:
            - It looks like each product has a shopify_variants array that stores data
              about the same product but in different quantities. This could maybe be
              included?
        """
        product = TypeProduct(
            uuid = product_obj['product_id'],
            name = product_obj['title'],
            title = product_obj['title'],
            description = product_obj['description'],
            price = product_obj['price'],
            url = '{0}{1}'.format(self._supplier['base_url'], product_obj['link']),
            supplier = product_obj['vendor'],
            currency = 'USD'
        )

        # SKU/Quantity regex pattern test:  https://regex101.com/r/A1e2C2/1
        quantity_pattern = re.compile(r'^(?:[A-Z0-9]+)-(?P<quantity>[0-9\.]+)(?P<uom>[A-Za-z]+)$')
        quantity_matches = quantity_pattern.search(product_obj['product_code'])
        product.update(quantity_matches.groupdict())

        return product
    
if __name__ == '__main__' and __package__ is None:
    __name__ = 'suppliers.supplier_laballey'
    __package__ = 'suppliers'
    __module__ = 'SupplierLaballey'