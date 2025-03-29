"""Suppliers init"""

import logging
import os
import sys


_logger = logging.getLogger("suppliers/__init__")
logging.basicConfig(level=os.environ.get("LOG_LEVEL", "WARNING"))

path = os.path.dirname(os.path.abspath(__file__))

__ignorable_files = [
    "__init__.py",
    # Trying out using a __disabled__ property check instead of using this
    # array.
    # "supplier_base.py",
    # 'supplier_warchem.py'
]

__all__ = []

suppliers_dir_files = [
    f[:-3]
    for f in os.listdir(path)
    if f.endswith(".py")
    and f.startswith("supplier_")
    and f not in __ignorable_files
]

# I get it. This file looks like shit. Not sure what the best way to
# do dynamic imports in Python is though ¯\_(ツ)_/¯

for supplier_file in suppliers_dir_files:
    supplier_module = __import__(
        ".".join([__name__, supplier_file]), fromlist=[supplier_file]
    )
    if (
        hasattr(supplier_module, "__disabled__")
        and supplier_module.__disabled__ is True
    ):
        _logger.debug("Skipping module %s (disabled)", supplier_file)
        continue
    classes = [
        getattr(supplier_module, x)
        for x in dir(supplier_module)
        if isinstance(getattr(supplier_module, x), type)
    ]
    for cls in classes:
        setattr(sys.modules[__name__], cls.__name__, cls)
        if (
            cls.__name__.startswith("Supplier")
            #  and cls.__name__ != "SupplierBase"
        ):
            _logger.debug("Including supplier module %s", cls.__name__)
            __all__.append(cls.__name__)
