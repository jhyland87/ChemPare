from suppliers.supplier_3schem import Supplier3SChem
from suppliers.supplier_laboratoriumdiscounter import SupplierLaboratoriumDiscounter

test_labdiscounter = SupplierLaboratoriumDiscounter('acetone')
print('LaboratoriumDiscounter Price:',test_labdiscounter.price)


test_3schem = Supplier3SChem('clean')
print('3SChem Price:',test_3schem.price)