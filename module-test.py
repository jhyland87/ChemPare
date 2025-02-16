from suppliers.supplier_3schem import Supplier3SChem
from suppliers.supplier_laboratoriumdiscounter import SupplierLaboratoriumDiscounter

test_labdiscounter = SupplierLaboratoriumDiscounter('acetone')
print('LaboratoriumDiscounter')
print('\tName:',test_labdiscounter.name)
print('\tPrice:',test_labdiscounter.price)

test_3schem = Supplier3SChem('clean')
print('3SChem')
print('\tName:',test_3schem.name)
print('\tPrice:',test_3schem.price)