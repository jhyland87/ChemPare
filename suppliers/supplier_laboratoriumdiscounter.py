from suppliers.supplier_base import SupplierBase

# File: /suppliers/supplier_laboratoriumdiscounter.py
class SupplierLaboratoriumDiscounter(SupplierBase):
    _supplier = 'Laboratorium Discounter'
    _base_url = 'https://www.laboratoriumdiscounter.nl'

    # If any extra init logic needs to be called... uncmment the below and add changes
    # def __init__(self, query):
    #     super().__init__(id, query)
        # Do extra stuff here

    def _query_product(self, query):
        # Example request url for Laboratorium Discounter
        # https://www.laboratoriumdiscounter.nl/en/search/{search_query}/page1.ajax?limit=100
        # 
        get_params = {
            'limit': 1000
        }        
        search_result = self.http_get_json(f'en/search/{query}/page1.ajax?', get_params)
        return search_result['products']
    
    def _set_values(self):
        selected_product = self._query_result[0]
        self._product_name = selected_product['fulltitle']
        self._product_price = selected_product['price']['price']

if __name__ == "__main__" and __package__ is None:
    __package__ = "suppliers.supplier_laboratoriumdiscounter.SupplierLaboratoriumDiscounter"