import os, sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from suppliers.supplier_3schem import Supplier3SChem
from suppliers.supplier_laboratoriumdiscounter import SupplierLaboratoriumDiscounter
from suppliers.supplier_onyxmet import SupplierOnyxmet

test_labdiscounter = SupplierLaboratoriumDiscounter('acetone')
print('LaboratoriumDiscounter')
print('  Name:',test_labdiscounter.name)
print('  Price:',test_labdiscounter.price)

print('-------')

test_3schem = Supplier3SChem('clean')
print('3SChem')
print('  Name:',test_3schem.name)
print('  Price:',test_3schem.price)

print('-------')

test_onyxmet = SupplierOnyxmet('mercury')
print('Onyxmet')
print('  Title:',test_onyxmet.title)
print('  Name:',test_onyxmet.name)
print('  Price:',test_onyxmet.price)
print('  Purity:',test_onyxmet.purity)
print('  Quantity:',test_onyxmet.quantity)
print('  UOM:',test_onyxmet.uom)
