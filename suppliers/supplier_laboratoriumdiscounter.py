from suppliers.supplier_base import SupplierBase

# File: /suppliers/supplier_laboratoriumdiscounter.py
class SupplierLaboratoriumDiscounter(SupplierBase):
    _name = 'Laboratorium Discounter'
    _base_url = 'https://www.laboratoriumdiscounter.nl'

    def search_products(self, query):
        # Example request url for Laboratorium Discounter
        # https://www.laboratoriumdiscounter.nl/en/search/{search_query}/page1.ajax?limit=100
        # 
        get_params = {
            'limit': 1000
        }        
        search_result = self.http_get_json(f'en/search/{query}/page1.ajax?', get_params)
        return search_result['products']

    def get_product(self, name):
        product_listing = self.search_products(name)
        return product_listing[0]
    
    def get_product_price(self, name):
        product_json = self.get_product(name)
        return product_json['price']['price']

if __name__ == "__main__" and __package__ is None:
    __package__ = "suppliers.supplier_laboratoriumdiscounter.SupplierLaboratoriumDiscounter"