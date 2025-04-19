"""TypeSupplier datatype"""

from dataclasses import dataclass
from typing import Dict

@dataclass
class TypeSupplier(Dict):
    """Custom data class for suppliers"""

    name: str
    """Name of supplier"""

    base_url: str
    """Base URL for supplier"""

    location: str | None = None
    """Location of supplier"""

    api_url: str | None = None
    """URL for public facing API - may not be the same as base_url"""

    api_key: str | None = None
    """Key for API calls, if needed"""

    # def update(self, data: Dict) -> None:
    #     """Update the TypeSupplier instance

    #     Args:
    #         data (Dict): Dictionary to merge into current dictioary
    #     """
    #     if data:
    #         self.__dict__.update(data)
