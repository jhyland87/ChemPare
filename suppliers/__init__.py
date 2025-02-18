#from pathlib import Path

if __debug__:
    print('Running' if __name__ == '__main__' else 'Importing', Path(__file__).resolve())

import os, sys

path = os.path.dirname(os.path.abspath(__file__))

__all__ = []
for py in [f[:-3] for f in os.listdir(path) if f.endswith('.py') and f != '__init__.py' and f != 'supplier_base.py' and f.startswith('supplier_')]:
    mod = __import__('.'.join([__name__, py]), fromlist=[py])
    classes = [getattr(mod, x) for x in dir(mod) if isinstance(getattr(mod, x), type)]
    for cls in classes:
        setattr(sys.modules[__name__], cls.__name__, cls)
        if cls.__name__.startswith('Supplier') and cls.__name__ != 'SupplierBase':
            __all__.append(cls.__name__)
        