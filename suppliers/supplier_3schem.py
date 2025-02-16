from suppliers.supplier_base import SupplierBase

# File: /suppliers/supplier_3schem.py
class Supplier3SChem(SupplierBase):
    _name = '3S Chemicals LLC'
    _base_url = 'https://3schemicalsllc.com'

    def search_products(self, query):
        # Example request url for 3S Supplier
        # https://3schemicalsllc.com/search/suggest.json?q=clean&resources[type]=product&resources[limit]=6&resources[options][unavailable_products]=last
        # 
        get_params = {
            'q': query,
            'resources[type]':'product',
            'resources[limit]':'100',
            'resources[options][unavailable_products]':'last'
        }        
        search_result = self.http_get_json('search/suggest.json', get_params)
        return search_result['resources']['results']['products']

    def get_product(self, name):
        product_listing = self.search_products(name)
        return product_listing[0]
    
    def get_product_price(self, name):
        product_json = self.get_product(name)
        return product_json['price']

if __name__ == "__main__" and __package__ is None:
    __package__ = "suppliers.supplier_3schem.Supplier3SChem"