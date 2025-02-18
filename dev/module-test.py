import os, sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from suppliers.supplier_3schem import Supplier3SChem
from suppliers.supplier_laboratoriumdiscounter import SupplierLaboratoriumDiscounter
from suppliers.supplier_onyxmet import SupplierOnyxmet


test_3schem = Supplier3SChem('clean')
print('3SChem')
for product in test_3schem.products:
    if product.name: print("    Name:", product.name) 
    if product.price: print("    Price:", product.price)
    if product.url: print("    URL:", product.url)
    print("")

print('-------')

test_laboratoriumdiscounter = SupplierLaboratoriumDiscounter('mercury')
print('LaboratoriumDiscounter')
for product in test_laboratoriumdiscounter.products:
    if product.name: print("    Name:", product.name) 
    if product.price: print("    Price:", product.price)
    if product.url: print("    URL:", product.url)
    if product.cas: print("    CAS:", product.cas)
    print("")

print('-------')

test_onyxmet = SupplierOnyxmet('mercury', 5)
print('Onyxmet')
for product in test_onyxmet.products:
    if product.name: print("    Name:", product.name) 
    if product.price: print("    Price:", product.price)
    if product.url: print("    URL:", product.url)
    if product.cas: print("    CAS:", product.cas)
    print("")

print('-------')