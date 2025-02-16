from suppliers.supplier_base import SupplierBase

# File: /suppliers/supplier_3schem.py
class Supplier3SChem(SupplierBase):
    _supplier = '3S Chemicals LLC'
    _base_url = 'https://3schemicalsllc.com'

    def _query_product(self, query):
        # Example request url for 3S Supplier
        # https://3schemicalsllc.com/search/suggest.json?q=clean&resources[type]=product&resources[limit]=6&resources[options][unavailable_products]=last
        # 
        get_params = {
            'q': query,
            'resources[type]':'product',
            'resources[limit]':1000,
            'resources[options][unavailable_products]':'last'
        }        
        search_result = self.http_get_json('search/suggest.json', get_params)
        return search_result['resources']['results']['products']

    def _set_values(self):
        selected_product = self._query_result[0]
        self._price = selected_product['price']
        self._name = selected_product['title']

if __name__ == "__main__" and __package__ is None:
    __package__ = "suppliers.supplier_3schem.Supplier3SChem"