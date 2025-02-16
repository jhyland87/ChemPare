from suppliers.supplier_base import SupplierBase
from bs4 import BeautifulSoup
import re

# File: /suppliers/supplier_onyxmet.py
class SupplierOnyxmet(SupplierBase):
    
    # Supplier specific data
    _supplier = dict(
        name = 'Onyxmet',
        location = 'Poland',
        base_url = 'https://onyxmet.com'
    )

    # Regex tested at https://regex101.com/r/ddGVsT/1 (matches 66/80)
    #_title_regex_pattern = r'^(?P<name>.*) (-\s)?(?P<quantity>[0-9,]+)(?P<uom>k?g|[cmμ]m)'

    # Regex tested at https://regex101.com/r/qL8u8s/1 67/80
    #_title_regex_pattern = r'^(?P<name>.*) (-\s)?(?P<quantity>[0-9,]+)(?P<uom>[cmkμ]?[mlg])'

    # Regex tested at https://regex101.com/r/bLWC2b/2 (matches 80-ish/80)
    # NOTE: The group names here should match keys in the self._product dictionary, as the 
    #       regex results will be merged into it.
    _title_regex_pattern = r'^(?P<name>[a-zA-Z\s\-\(\)]+)[-\s]+(?P<purity>[0-9,]+%)?[-\s]*(?:(?P<quantity>[0-9,]+)(?P<uom>[cmkμ]?[mlg]))?'

    # If any extra init logic needs to be called... uncmment the below and add changes
    # def __init__(self, query):
    #     super().__init__(id, query)
        # Do extra stuff here

    def _query_product(self, query):
        # Example request url for Onyxmet Supplier
        # https://onyxmet.com/index.php?route=product/search/json&term={query}
        # 
        get_params = {
            'route':'product/search/json',
            'term': query
        }    

        query_result_list = self.http_get_json('index.php', get_params)

        return self.http_get_html(query_result_list[0]['href'])

    def _set_values(self):
        product_soup = BeautifulSoup(self._query_result, 'html.parser')

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
        # (Set the self._product_name here to default it, we ca re-set it to the parsed value down below)
        self._product['title'] = title_elem.contents[0]
        self._product['name'] = title_elem.contents[0]
        self._product['price'] = price_elem.contents[0]

        # Use the regex pattern to parse the name for some useful data. 
        title_pattern = re.compile(self._title_regex_pattern)
        title_matches = title_pattern.search(self._product['name'])

        # If something is matched, then just merge the key/names into the self._product property
        if title_matches:
            self._product.update(title_matches.groupdict())

if __name__ == '__main__' and __package__ is None:
    __package__ = 'suppliers.supplier_3schem.Supplier3SChem'


