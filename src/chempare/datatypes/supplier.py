"""SupplierType datatype"""

from dataclasses import dataclass


@dataclass
class SupplierType:
    """
    SupplierType dataclass for supplier specific data


    :param name: Name of the supplier
    :type name: str
    :param base_url: Base URL of suppliers website
    :type base_url: str
    :param api_url: Base URL of suppliers API resource, defaults to None
    :type api_url: str | None, optional
    :param api_key: API key for supplier, if there is one found, defaults to None
    :type api_key: str | None, optional
    :param location: Location the supplier is based out of, defaults to None
    :type location: str | None, optional
    """

    name: str
    """Name of supplier"""

    base_url: str
    """Base URL for supplier"""

    api_url: str | None = None
    """URL for public facing API - may not be the same as base_url"""

    api_key: str | None = None
    """Key for API calls, if needed"""

    location: str | None = None
    """Location of supplier"""

    # def update(self, data: dict) -> None:
    #     """Update the SupplierType instance

    #     Args:
    #         data (dict): Dictionary to merge into current dictioary
    #     """
    #     if data:
    #         self.__dict__.update(data)
