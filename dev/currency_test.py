"""SupplierBase module to be inherited by any supplier modules"""
from __future__ import annotations

from chempare import ClassUtils


class Foo(ClassUtils):
    def __init__(self, **kwargs):

        result = self._to_usd(**kwargs)
        print("result:", kwargs, result)


# Foo(from_currency="EUR", amount=100)
Foo(from_currency="EUR", amount=100234.10)
print("----")
Foo(from_currency="GBP", amount=321)
print("----")
Foo(from_currency="GBP", amount=321346.64)
print("----")
Foo(from_currency="JPY", amount=321)
print("----")
Foo(from_currency="AUD", amount=123)
print("----")
Foo(from_currency="CAD", amount=123234.12)
print("----")


# "€100 (EUR) to USD",
# "€100.234,10 (EUR) to USD",
# "£321 (GBP) to USD",
# "£321.346,64 (GBP) to USD",
# "¥321 (JPY) to USD",
# "AU$123 (AUD) to USD",
# "CA$123,234.12 (CAD) to USD",
# "error",
