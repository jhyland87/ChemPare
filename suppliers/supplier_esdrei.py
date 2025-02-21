from suppliers.supplier_base import SupplierBase, TypeProduct, TypeSupplier
from typing import List, Set, Tuple, Dict, Any
from bs4 import BeautifulSoup
import re

# File: /suppliers/supplier_esdrei.py
class SupplierEsDrei(SupplierBase):

    # Supplier specific data
    _supplier: TypeSupplier = dict(
        name = 'EsDrei',
        #location = '',
        base_url = 'https://shop.es-drei.de' 
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
        # Example request url for S3Chem Supplier
        # https://shop.es-drei.de/search/index/sSearch/mercury?p=1&n=48
        # https://shop.es-drei.de/search?sSearch=mercury&p=1&n=48
        # 
        get_params = {
            'sSearch': query,
            'p': 1, # Page number
            'n': self._limit # Items per page per page
        }    

        search_result = self.http_get_html('search', get_params)

        if not search_result: 
            return
        
        self._query_results = search_result

    def _parse_products(self):
        """Parse product query results.

        Iterate over the products returned from self._query_product, creating new requests
        for each to get the HTML content of the individual product page, and creating a 
        new TypeProduct object for each to add to _products

        Todo:
            Have this execute in parallen using AsyncIO        
        """

        product_page_soup = BeautifulSoup(self._query_results, 'html.parser')
        product_containers = product_page_soup.find_all('div',class_='product--info')
        
        for product in product_containers[:self._limit]:
            self._products.append(self._parse_product(product))

    def _parse_product(self, product_elem:BeautifulSoup) -> TypeProduct:
        """Parse a single div.product--info element, creating a Partner object

        Args:
            product_elem (BeautifulSoup): One of the elements returned from the BS search

        Returns:
            TypeProduct: Object of parsed product
        """

        # Get some of the basic elements from this product_element object (which is just
        # a BeautifulSoup object)
        title_elem = product_elem.find('a', class_='product--title')
        product_desc = product_elem.find('div', class_='product--description')
        price_info = product_elem.find('div', class_='product--price-info')

        # Parse the nested elements under the product_elem children
        price_default = price_info.find('span', class_='price--default')
        price_unit = price_info.find('div', class_='price--unit')
        price_units = price_unit.find_all('span')
        price_data = price_default.string.strip().split('\n')[0]

        # Parse the price for the useful information
        # Pattern tested at: https://regex101.com/r/R4PQ5K/1
        price_pattern = re.compile(r'^(?P<price>.*)\s+(?P<currency>.)$')
        price_matches = price_pattern.search(price_data)

        # Parse the quantity for the quantity and uom
        # Pattern tested at: https://regex101.com/r/qpTlFm/1
        quantity_pattern = re.compile(r'^(?P<quantity>[0-9,.]+)\s+(?P<uom>\w+)$')
        quantity_matches = quantity_pattern.search(price_units[1].string.strip())

        product = TypeProduct(
            title = title_elem.attrs['title'],
            name = title_elem.attrs['title'],
            description = product_desc.string,
            url = title_elem.attrs['href'],
            supplier = self._supplier['name'],
        )
    
        # Since the pattern were matching for will name the matched groups 'price' and 'currency',
        # we can use the `groupdict()` method to return a dictionary like {price: 123, currency: '$'},
        # which we can then just directly update the product with.
        #
        # This is just faster than doing:
        #   product.price = price_matches.price
        #   product.currency = price_matches.currency
        product.update(price_matches.groupdict())

        # Same thing with the quantity matches, they're named 'quantity' and 'uom', so that can just
        # me merged with the product as well.
        product.update(quantity_matches.groupdict())

        # I notice the prices sometimes will have a 'from     32.24', so lets
        # reduce any multi-spaced gaps down to a single space
        product.price = re.sub(r'\s+', r' ', product.price)

        return product

if __name__ == '__main__' and __package__ is None:
    __name__ = 'suppliers.supplier_esdrie'
    __package__ = 'suppliers'
    __module__ = 'SupplierEsDrei'