# pylint: disable=too-many-arguments
# pylint: disable=missing-class-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=too-many-positional-arguments
# pylint: disable=broad-exception-caught

import os
import suppliers

__ignorable_files = [
    "__init__.py",
    # Trying out using a __disabled__ property check instead of using this array.
    "supplier_base.py",
    "test_supplier_base",
    "__init__.py",
    "supplier_file",
    "supplier_module",
    "supplier_base",
]


def test_suppliers_unit_test_presence():
    test_files = [
        f"tests/suppliers/test_{f}.py"
        for f in suppliers.__dict__.keys()
        if f.startswith("supplier_") and f not in __ignorable_files
    ]

    missing = [
        test_file
        for test_file in test_files
        if os.path.exists(test_file) is False
    ]

    assert len(missing) == 0
