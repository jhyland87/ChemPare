from suppliers.supplier_base import SupplierBase, TypeProduct, TypeSupplier
from typing import List, Set, Tuple, Dict, Any
from bs4 import BeautifulSoup
import re

# File: /suppliers/supplier_tcichemicals.py
class SupplierTciChemicals(SupplierBase):

    allow_cas_search = True
    
    _limit = 20

    _supplier: TypeSupplier = dict(
        name = 'TCI Chemicals',
        #location = 'Eu',
        base_url = 'https://www.tcichemicals.com/',
    )
    """Supplier specific data"""

    allow_cas_search: bool = True
    """Determines if the supplier allows CAS searches in addition to name searches"""

    # # If any extra init logic needs to be called... uncmment the below and add changes
    # def __init__(self, query):
    #     super().__init__(query)
        # Do extra stuff here

    def _query_products(self, query: str):
        """Query products from supplier

        Args:
            query (str): Query string to use
        """

        # Example request url for Synthetika
        # JSON (limited search results)
        # https://synthetikaeu.com/webapi/front/en_US/search/short-list/products?text=borohydride&org=borohydride&page=1
        # HTML
        # https://www.tcichemicals.com/US/en/search/?text=benz'
        # 
        def __query_search_page(query:str, page_idx:int=0):
            """Handles the pagination on the search page"""
            get_params = {
                # Setting the limit here to 1000, since the limit parameter should apply to
                # results returned from Supplier3SChem, not the rquests made by it. 
                #'q': f'{query}:productNameExactMatch',
                'text':query,
                'page':page_idx
            }

            search_result = self.http_get_html(f'US/en/search/', params=get_params)
            
            if not search_result: 
                return
            
            product_soup = BeautifulSoup(search_result, 'html.parser')

            # Since we know the element is a <h3 class=product-price /> element, search for H3's
            product_basic = product_soup.find('div', id='product-basic-wrap')

            if product_basic is None:
                # No product wrapper found
                return
            
            self._query_results.extend(product_basic.find_all('div', class_='prductlist'))

            if self._limit == len(self._query_results):
                return
            
            if self._limit < len(self._query_results):
                self._query_results = self._query_results[:self._limit]
                return 

            if self._limit > len(self._query_results):
                __query_search_page(query, page_idx+1)
                return
       
        __query_search_page(query, 0)
    
    # Method iterates over the product query results stored at self._query_results and 
    # returns a list of TypeProduct objects.
    def _parse_products(self):
        #print('_query_results:',self._query_results)
        for product_elem in self._query_results:
            self.__parse_product(product_elem)

    def __parse_product(self, product_obj:BeautifulSoup) -> None:
        """Parse single product and return single TypeProduct object

        Args:
            product_obj (Tuple[List, Dict]): Single product object from JSON body

        Todo:
            - It looks like each product has a shopify_variants array that stores data
              about the same product but in different quantities. This could maybe be
              included?
        """
     
        title = product_obj.find('a', class_='product-title')

        if not title.string:
            return

        quantity = product_obj.find(attrs={'data-attr':'Size:'})
        price = product_obj.find('div', class_='listPriceNoStrike')

        product = TypeProduct(
            title=title.string.strip(),
            quantity=quantity.string.strip(),
            price=price.string.strip()
        )

        description_container = product_obj.find('div', class_='product-description')
        data = description_container.find_all('td')

        for idx, d in enumerate(data):
            if d.string.strip() == 'Product Number':
                product.uuid = data[idx+1].string.strip()
                continue

            if d.string.strip() == 'CAS RN':
                product.cas  = data[idx+1].string.strip()
                continue

        quantity_pattern = re.compile(r'(?P<quantity>[0-9,\.x]+)\s?(?P<uom>[gG]allon|gal|k?g|[cmμ][mM]|[mM]?[lL]|[Mm][gG])$')
        quantity_matches = quantity_pattern.search(product.quantity)

        if quantity_matches: 
            product.update(quantity_matches.groupdict())

        price_pattern = re.compile(r'^(?P<currency>.)(?P<price>\d+\.\d+)$')
        price_matches = price_pattern.search(product.price)

        if price_matches: 
            product.update(price_matches.groupdict())

        self._products.append(product.cast_properties())

    
if __name__ == '__main__' and __package__ is None:
    __name__ = 'suppliers.supplier_tcichemicals'
    __package__ = 'suppliers'
    __module__ = 'SupplierTciChemicals'
    __disabled__ = True