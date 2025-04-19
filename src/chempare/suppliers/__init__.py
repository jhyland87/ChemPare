"""Suppliers init"""

import logging
import os
import sys


_logger = logging.getLogger("suppliers/__init__")
logging.basicConfig(level=os.environ.get("LOG_LEVEL", "WARNING"))

path = os.path.dirname(os.path.abspath(__file__))


suppliers_dir_files = [f[:-3] for f in os.listdir(path) if f.endswith(".py") and f.startswith("supplier_")]

# I get it. This file looks like shit. Not sure what the best way to
# do dynamic imports in Python is though ¯\_(ツ)_/¯

__all__ = []

for supplier_file in suppliers_dir_files:
    supplier_module = __import__(".".join(["chempare", "suppliers", supplier_file]), fromlist=[supplier_file])
    if hasattr(supplier_module, "__disabled__") and supplier_module.__disabled__ is True:
        _logger.debug("Skipping module %s (disabled)", supplier_file)
        continue

    setattr(sys.modules[__name__], supplier_module.__supplier_class.__name__, supplier_module.__supplier_class)

    __all__.append(supplier_module.__supplier_class.__name__)  # type: ignore
