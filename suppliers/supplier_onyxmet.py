from suppliers.supplier_base import SupplierBase, Product
from typing import List, Set, Tuple, Dict, Any
from bs4 import BeautifulSoup
import re

# File: /suppliers/supplier_onyxmet.py
class SupplierOnyxmet(SupplierBase):

    # Supplier specific data
    _supplier: Dict = dict(
        name = 'Onyxmet',
        location = 'Poland',
        base_url = 'https://onyxmet.com'
    )

    # Regex tested at https://regex101.com/r/ddGVsT/1 (matches 66/80)
    #_title_regex_pattern = r'^(?P<name>.*) (-\s)?(?P<quantity>[0-9,]+)(?P<uom>k?g|[cmμ]m)'

    # Regex tested at https://regex101.com/r/qL8u8s/1 67/80
    #_title_regex_pattern = r'^(?P<name>.*) (-\s)?(?P<quantity>[0-9,]+)(?P<uom>[cmkμ]?[mlg])'

    # Regex tested at https://regex101.com/r/bLWC2b/3 (matches 80-ish/80)
    # NOTE: The group names here should match keys in the self._product dictionary, as the 
    #       regex results will be merged into it.
    _title_regex_pattern = r'^(?P<product>[a-zA-Z\s\-\(\)]+[a-zA-Z\(\)])[-\s]+(?P<purity>[0-9,]+%)?[-\s]*(?:(?P<quantity>[0-9,]+)(?P<unit>[cmkμ]?[mlg]))?'

    # If any extra init logic needs to be called... uncmment the below and add changes
    # def __init__(self, query, limit=123):
    #     super().__init__(id, query, limit)
        # Do extra stuff here

    def _query_product(self, query: str):
        """Query products from supplier

        Args:
            query (str): Query string to use
        """
        # Example request url for Onyxmet Supplier
        # https://onyxmet.com/index.php?route=product/search/json&term={query}
        # 
        get_params = {
            'route':'product/search/json',
            'term': query
        }    

        search_result = self.http_get_json('index.php', get_params)

        if not search_result: 
            return
        
        self._query_results = search_result[0:self._limit]

    def _parse_products(self):
        """Parse product query results.

        Iterate over the products returned from self._query_product, creating new requests
        for each to get the HTML content of the individual product page, and creating a 
        new Product object for each to add to _products

        Todo:
            Have this execute in parallen using AsyncIO        
        """

        for product in self._query_results:
            self._products.append(self._query_and_parse_product(product['href']))

    def _query_and_parse_product(self, href:str) -> Product:
        """Query specific product page and parse results

        Args:
            href (str): The path of the web page to query and parse using BeautifulSoup

        Returns:
            Product: Single instance of Product
        """
       
        product_page_html = self.http_get_html(href)

        product_soup = BeautifulSoup(product_page_html, 'html.parser')

        # Since we know the element is a <h3 class=product-price /> element, search for H3's
        h3_elems = product_soup.find_all('h3')  

        # Find the one with the 'product-price' class
        title_elem = next(obj for obj in h3_elems if 'product-title' in obj.get('class'))
        price_elem = next(obj for obj in h3_elems if 'product-price' in obj.get('class'))

        # TODO: I'm sure there's an easier way to just specifically look for the 'h3.product-price' element,
        #       instead of _all_ h3 elements then filtering the results for one that has the 'product-price'
        #       class... But I'll leave that optimization up to you :-)

        if not price_elem:
            raise Exception("No price found")
        
        # Get the product name and price
        # (Set the product name here to default it, we ca re-set it to the parsed value down below)
        product = Product(
            title = title_elem.contents[0],
            name = title_elem.contents[0],
            price = price_elem.contents[0],
            supplier = self._supplier['name']
        )

        # Use the regex pattern to parse the name for some useful data. 
        title_pattern = re.compile(self._title_regex_pattern)
        title_matches = title_pattern.search(product.name)

         # If something is matched, then just merge the key/names into the self._product property
        if title_matches:
            product.update(title_matches.groupdict())

        return product

if __name__ == '__main__' and __package__ is None:
    __name__ = 'suppliers.supplier_onyxmet'
    __package__ = 'suppliers'
    __module__ = 'SupplierOnyxmet'
