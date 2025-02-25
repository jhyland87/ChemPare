from suppliers.supplier_base import SupplierBase, TypeProduct, TypeSupplier
from typing import List, Set, Tuple, Dict, Any
import re

# File: /suppliers/supplier_ftfscientific.py
class SupplierFtfScientific(SupplierBase):

    _supplier: TypeSupplier = dict(
        name = 'FTF Scientific',
        location = None,
        base_url = 'https://www.ftfscientific.com',
        api_url = 'https://www.ftfscientific.com',
        #api_key = '8B7o0X1o7c'
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
        return
        # Example request url for FTF
        # https://www.ftfscientific.com/_api/search-services-sitesearch/v1/search
        # 
        body = {
            "documentType": "public/stores/products",
            "query": query,
            "paging": {
                "skip": 0,
                "limit": self._limit
            },
            "includeSeoHidden": False,
            "facets": {
                "clauses": [
                {
                    "aggregation": {
                    "name": "discountedPriceNumeric",
                    "aggregation": "MIN"
                    }
                },
                {
                    "aggregation": {
                    "name": "discountedPriceNumeric",
                    "aggregation": "MAX"
                    }
                },
                {
                    "term": {
                    "name": "collections",
                    "limit": 999
                    }
                }
                ]
            },
            "ordering": {
                "ordering": []
            },
            "language": "en",
            "properties": [],
            "fuzzy": True,
            "fields": [
                "description",
                "title",
                "id",
                "currency",
                "discountedPrice",
                "inStock"
            ]
        }

        search_result = self.http_post_json(path=f'_api/search-services-sitesearch/v1/search', json=body)

        if not search_result: 
            return
        
        self._query_results = search_result['documents'][0:self._limit]
    
    # Method iterates over the product query results stored at self._query_results and 
    # returns a list of TypeProduct objects.
    def _parse_products(self):
        return
        #print('self._query_results:',self._query_results)
        for product_obj in self._query_results: 

            # Add each product to the self._products list in the form of a TypeProduct
            # object.
            self._products.append(self._parse_product(product_obj))

    def _parse_product(self, product_obj:Dict) -> TypeProduct:
        """Parse single product and return single TypeProduct object

        Args:
            product_obj (Dict): Single product object from JSON body

        Returns:
            TypeProduct: Instance of TypeProduct

        Todo:
            - It looks like each product has a shopify_variants array that stores data
              about the same product but in different quantities. This could maybe be
              included?
        """
        product = TypeProduct(
            uuid=product_obj['id'],
            name=product_obj['title'],
            title=product_obj['title'],
            description=product_obj['description'],
            price=product_obj['discountedPrice'],
            url='{0}{1}'.format(self._supplier['base_url'], product_obj['url']),
            supplier=self._supplier['name'],
            currency=product_obj['currency']
        )

        # # SKU/Quantity regex pattern test:  https://regex101.com/r/A1e2C2/1
        # quantity_pattern = re.compile(r'^(?:[A-Z0-9]+)-(?P<quantity>[0-9\.]+)(?P<uom>[A-Za-z]+)$')
        # quantity_matches = quantity_pattern.search(product_obj['product_code'])

        # if quantity_matches: 
        #     product.update(quantity_matches.groupdict())

        return product
    
if __name__ == '__main__' and __package__ is None:
    __name__ = 'suppliers.supplier_ftfscientific'
    __package__ = 'suppliers'
    __module__ = 'SupplierFtfScientific'