"""Suppliers init"""
from __future__ import annotations

from importlib import import_module
from inspect import isclass
from pathlib import Path
from pkgutil import iter_modules

from chempare.suppliers.supplier_base import SupplierBase

__subclasses__ = []
# iterate through the modules in the current package
package_dir = str(Path(__file__).resolve().parent)
for _, module_name, _ in iter_modules([package_dir]):

    # import the module and iterate through its attributes
    module = import_module(f"{__name__}.{module_name}")
    for attribute_name in dir(module):
        attribute = getattr(module, attribute_name)

        # Skip anything that isn't a subclass of SupplierBase (including SupplierBase itself)
        if not isclass(attribute) or not issubclass(attribute, SupplierBase) or attribute_name.endswith("Base"):
            continue

        globals()[attribute_name] = attribute
        if attribute_name not in __subclasses__:
            __subclasses__.append(attribute_name)
