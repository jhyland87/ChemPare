from suppliers.supplier_base import SupplierBase, Product

# File: /suppliers/supplier_laboratoriumdiscounter.py
class SupplierLaboratoriumDiscounter(SupplierBase):

     # Supplier specific data
    _supplier = dict(
        name = 'Laboratorium Discounter',
        location = None,
        base_url = 'https://www.laboratoriumdiscounter.nl'
    )

    # If any extra init logic needs to be called... uncmment the below and add changes
    # def __init__(self, query, limit=123):
    #     super().__init__(id, query, limit)
        # Do extra stuff here

    def _query_product(self, query):
        # Example request url for Laboratorium Discounter
        # https://www.laboratoriumdiscounter.nl/en/search/{search_query}/page1.ajax?limit=100
        # 
        get_params = {
            # Setting the limit here to 1000, since the limit parameter should apply to
            # results returned from Supplier3SChem, not the rquests made by it. 
            'limit': 1000
        }        
        search_result = self.http_get_json(f'en/search/{query}/page1.ajax?', get_params)

        if not search_result: 
            return False
        
        self._query_results = search_result['products'][0:self._limit]
    
    # Method iterates over the product query results stored at self._query_results and 
    # returns a list of Product objects.
    def _parse_products(self):
        for product in self._query_results: 
            # Skip unavailable
            if product['available'] is False:
                next

            # Add each product to the self._products list in the form of a Product
            # object.
            self._products.append(Product(
                uuid = product['id'],
                name = product['title'],
                title = product['fulltitle'],
                cas = self._get_cas_from_variant(product['variant']),
                description = product['description'],
                price = product['price']['price'],
                currency = product['price']['currency'],
                url = product['url'],
                supplier = self._supplier['name']
            ))
    
    """ LABORATORIUMDISCOUNTER SPECIFIC METHODS """
    
    def _get_cas_from_variant(self, variant):
        """Get the CAS number from the variant, if applicable
        
        
        """
        variant_dict = self._nested_arr_to_dict(variant.split(','))

        if variant_dict is not None and 'CAS' in variant_dict:
            return variant_dict['CAS']


# print("SupplierLaboratoriumDiscounter")
# print('   __name__:', __name__)
# print('   __package__:', __package__)

if __name__ == '__main__' and __package__ is None:
    __name__ = 'suppliers.supplier_laboratoriumdiscounter'
    __package__ = 'suppliers'
    __module__ = 'SupplierLaboratoriumDiscounter'