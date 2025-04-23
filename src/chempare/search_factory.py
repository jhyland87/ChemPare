"""Search factory"""
# from curl_cffi import requests
from __future__ import annotations

from typing import Self

from abcplus import finalmethod
from chempare import suppliers
from chempare.exceptions import NoProductsFoundError
from chempare.utils import ClassUtils
from datatypes import ProductType
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import


class SearchFactory(ClassUtils):
    """Simple factory to make searching easier"""

    suppliers = suppliers.__subclasses__
    """suppliers property lets scripts call 'SearchFactory.suppliers' to get a
    list of suppliers"""

    __results: list | None = None
    """Contains a list of all the product results"""

    __index: int = 0
    """Index used for __iter__ iterations"""

    def __init__(self, query: str, limit: int = 3) -> None:
        """Factory method for executing a search in all suppliers automatically

        Args:
            query (str): Search query
            limit (int, optional): Limit results to this. Defaults to 3.
        """

        self.__results = []

        self.__query(query, limit)

    def __iter__(self) -> Self:
        """Simple iterator, making this object usable in for loops"""

        return self

    def __next__(self) -> ProductType:
        """Next dunder method for for loop iterations

        Raises:
            StopIteration: When the results are done

        Returns:
            ProductType: Individual products
        """

        if self.__index >= len(self.__results):
            raise StopIteration

        value = self.__results[self.__index]
        self.__index += 1

        return value

    def __len__(self) -> int:
        """Result to return when len() is used

        Returns:
            int: Number of results from the last query
        """

        return len(self.__results)

    def __query(self, query: str, limit: int | None = None) -> None:
        """Iterates over the suppliers, running the query, then returning
        the results.

        Args:
            query (str): Search query
            limit (int, optional): Amount to limit the search by. Defaults
                                   to None.
        """

        query_is_cas = self._is_cas(query)

        if __debug__:
            print(f"Searching suppliers for '{query}'...\n")

        # Iterate over the modules in the suppliers package
        for supplier in suppliers.__subclasses__:
            if supplier == "SupplierBase":
                continue

            # Create a direct reference to this supplier class
            supplier_module = getattr(suppliers, supplier)

            if query_is_cas is True and supplier_module.allow_cas_search is False:
                if __debug__:
                    print(f"Skipping {supplier_module.__name__} CAS search")
                continue

            if __debug__:
                print(f"Searching {supplier_module.__name__}... ", end='')

            # Execute a search by initializing an instance of the supplier
            # class with the product query term as the first param
            try:
                res = supplier_module(query, limit)
            except NoProductsFoundError:
                print("No products found")
                continue
            except Exception as e:  # pylint: disable=broad-exception-caught
                if __debug__:
                    print("ERROR:", e)
                # print("ERROR, skipping")
                continue

            if __debug__:
                print(f"found {len(res.products)} products")

            if not res:
                continue

            # If there were some results found, then extend the self.__results
            # list with those products
            self.__results.extend(res.products)

    @property
    @finalmethod
    def results(self) -> list[ProductType]:
        """Results getter

        Returns:
            list[ProductType]: list of the aggregated ProductType objects from
                               each supplier
        """
        return self.__results
