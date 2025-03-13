from dataclasses import dataclass
from typing import NoReturn, Dict


@dataclass
class TypeSupplier:
    """Custom data class for suppliers"""

    name: str = None
    """Name of supplier"""

    location: str = None
    """Location of supplier"""

    base_url: str = None
    """Base URL for supplier"""

    api_url: str = None
    """URL for public facing API - may not be the same as base_url"""

    api_key: str = None
    """Key for API calls, if needed"""

    def update(self, data) -> NoReturn:
        self.__dict__.update(data)
