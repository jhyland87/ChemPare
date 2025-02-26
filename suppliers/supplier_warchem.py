from suppliers.supplier_base import SupplierBase, TypeProduct, TypeSupplier
from typing import List, Set, Tuple, Dict, Any, NoReturn, Union
from threading import Thread
from bs4 import BeautifulSoup
import re

# File: /suppliers/supplier_warchem.py
class SupplierWarchem(SupplierBase):

    _limit = 5

    _supplier: TypeSupplier = dict(
        name = 'WarChem',
        location = None,
        base_url = 'https://warchem.pl',
        api_url = 'https://warchem.pl'
    )
    """Supplier specific data"""

    allow_cas_search: bool = True
    """Determines if the supplier allows CAS searches in addition to name searches"""

    def _setup(self, query: str=None):
        # This eGold cookie seems to be what they use to keep track of your settings
        self._cookies['eGold']=self._random_string(26)

        # Make the request to keep the product listing limit at 36 (max)
        self.http_post(path=f'szukaj.html/szukaj={query}', data=dict(ilosc_na_stronie=36))

    def _query_products(self, query: str):
        """Query products from supplier

        Args:
            query (str): Query string to use
        """

        # https://warchem.pl/szukaj.html/szukaj=ACET/s=2

        search_result = self.http_get_html(path=f'szukaj.html/szukaj={query}/opis=tak/fraza=nie/nrkat=tak/kodprod=tak/ean=tak/kategoria=1/podkat=tak')

        search_result_soup = BeautifulSoup(search_result, 'html.parser')
        product_container = search_result_soup.find('div', class_='ListingWierszeKontener')
        product_elements = product_container.find_all('div', class_='LiniaDolna')
        self._query_results = product_elements[:self._limit]
    
    # Method iterates over the product query results stored at self._query_results and 
    # returns a list of TypeProduct objects.
    def _parse_products(self):
        """Iterate over the self._query_results list, running the parser for each and adding the
        returned TypeProduct object to self._products
        """

        threads = []
        for product_elem in self._query_results: 
            # Add each product to the self._products list in the form of a TypeProduct
            # object.
           
            link = product_elem.find('h3').find('a')
            thread = Thread(target=self.__query_and_parse_product, kwargs=dict(href=link.attrs['href']))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()  
    
    def __query_and_parse_product(self, href:str) -> None:
        """Query specific product page and parse results

        Args:
            href (str): The path of the web page to query and parse using BeautifulSoup

        Returns:
            TypeProduct: Single instance of TypeProduct
        """
       
        product_page_html = self.http_get_html(href)
        product_soup = BeautifulSoup(product_page_html, 'html.parser')

        product = TypeProduct(
            title=product_soup.find('h1').get_text(strip=True),
            supplier=self._supplier['name'],
            url=href
        )

        details = product_soup.find('div', class_='DodatkowyProduktuOpis').find_all('tr')

        translated_keys = {
            'Nazwa (ang.):':'name',
            'Numer CAS:':'cas'
        }

        for tr in details:
            td = tr.find_all('td')
            attr = td[0].get_text(strip=True)
            val = td[1].get_text(strip=True)

            if attr.strip() not in translated_keys:
                continue
            
            attr_key = translated_keys[attr.strip()]
            product.set(attr_key, val)

        price_elem = product_soup.find('span', {'itemprop':'price'})

        product.price = price_elem.attrs['content']
        product.currency = price_elem.get_text(strip=True).split(' ')[-1]

        quantity_elem_container = product_soup.find('div', id='nr_cechy_1')
        quantity_options = quantity_elem_container.find_all('div', class_='PoleWyboruCechy')

        quantity = quantity_options[0].find('label').find('span')
        if quantity:
            product.update(self._parse_quantity(quantity.get_text(strip=True)))

        self._products.append(product.cast_properties())
    
if __package__ == 'suppliers':
    __disabled__ = True