"""Search factory"""

from typing import List

# from curl_cffi import requests
import requests
from abcplus import finalmethod

from chempare import ClassUtils
from chempare import suppliers
from chempare.datatypes import TypeProduct

# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
from chempare.suppliers import *


class SearchFactory(ClassUtils, object):
    suppliers = suppliers.__all__
    """suppliers property lets scripts call 'SearchFactory.suppliers' to get a
    list of suppliers"""

    __results: List | None = None
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

    def __iter__(self):
        """Simple iterator, making this object usable in for loops"""

        return self

    def __next__(self) -> TypeProduct:
        """Next dunder method for for loop iterations

        Raises:
            StopIteration: When the results are done

        Returns:
            TypeProduct: Individual products
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
        for supplier in suppliers.__all__:
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
            except Exception as e:  # pylint: disable=broad-exception-caught
                if __debug__:
                    print("ERROR:", e)
                print("ERROR, skipping")
                continue

            if __debug__:
                print(f"found {len(res.products)} products")

            if not res:
                continue

            # If there were some results found, then extend the self.__results
            # list with those products
            self.__results.extend(res.products)

    def __get_cas(self, chem_name: str) -> str | None:
        """Search for the CAS value(s) given a chemical name

        Args:
            chem_name (str): Name of chemical to search for

        Returns:
            Optional[str]: CAS value of chemical
        """

        cas = None
        try:
            # Send a GET request to the API
            cas_request = requests.get(f"https://cactus.nci.nih.gov/chemical/structure/{chem_name}/cas")
            # Check if the request was successful
            if cas_request.status_code != 200:
                return None

            # Decode the bytes to a string
            cas_response = cas_request.content.decode("utf-8")

            if not cas_response:
                return None

            cas_list = cas_response.split("\n")
            cas = cas_list[0]
        except Exception as e:
            print("Failed to get CAS #", e)

        return cas

        # # Should only be one line/value, so just strip it before returning,
        # if a value was found
        # return str(cas_response).strip() if cas_response else None

    def __get_popular_name(self, query: str) -> str:
        """Get the most frequently used name for a chemical from a list of
        its aliases

        Args:
            query (str): Chemical name or CAS

        Returns:
            str: The most frequently found name
        """
        # Send a GET request to the API
        name_request = requests.get(f"https://cactus.nci.nih.gov/chemical/structure/{query}/names")

        # Check if the request was successful
        if name_request.status_code != 200:
            raise SystemError(f"Error: {name_request.status_code}")

        name_response = name_request.content.decode("utf-8")  # Decode the bytes to a string
        name_lines = name_response.split("\n")  # Split by newline

        highest_val = self._filter_highest_item_value(self._get_common_phrases(name_lines))

        keys = list(highest_val.keys())
        return keys[0][0]

    @property
    @finalmethod
    def results(self) -> List[TypeProduct]:
        """Results getter

        Returns:
            List[TypeProduct]: List of the aggregated TypeProduct objects from
                               each supplier
        """
        return self.__results
