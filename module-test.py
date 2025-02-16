from suppliers.supplier_3schem import Supplier3SChem
from suppliers.supplier_laboratoriumdiscounter import SupplierLaboratoriumDiscounter

# File: Some other file that includes the supplier classes.
test_3schem = Supplier3SChem()
product_price = test_3schem.get_product_price('clean')
print('clean price:',product_price)

test_labdiscounter = SupplierLaboratoriumDiscounter()
product_price = test_labdiscounter.get_product_price('acetone')
print('acetone:',product_price)