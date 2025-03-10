if __debug__:
    from pathlib import Path
    print('Running' if __name__ == '__main__' else 'Importing', Path(__file__).resolve())

import os
import sys

path = os.path.dirname(os.path.abspath(__file__))

__ignorable_files = [
    '__init__.py',
    # Trying out using a __disabled__ property check instead of using this array.
    'supplier_base.py',
    'supplier_template.py',
    #'supplier_warchem.py'
]

__all__ = []

suppliers_dir_files = [f[:-3] for f in os.listdir(path) if f.endswith('.py') and f.startswith('supplier_') and f not in __ignorable_files]

for supplier_file in suppliers_dir_files:
    supplier_module = __import__('.'.join([__name__, supplier_file]), fromlist=[supplier_file])
    if hasattr(supplier_module, '__disabled__') and supplier_module.__disabled__ is True:
        if __debug__:
            print(f'Skipping module {supplier_file} (disabled)')
        continue
    classes = [getattr(supplier_module, x) for x in dir(supplier_module) if isinstance(getattr(supplier_module, x), type)]
    for cls in classes:
        setattr(sys.modules[__name__], cls.__name__, cls)
        if cls.__name__.startswith('Supplier') and cls.__name__ != 'SupplierBase':
            __all__.append(cls.__name__)
