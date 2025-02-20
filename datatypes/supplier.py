from dataclasses import dataclass, astuple
from typing import List, Set, Tuple, Dict, Any


@dataclass
class Supplier:
    """Custom data class for suppliers"""

    # Name of supplier
    name: str = None

    # Location of supplier
    location: str = None

    # Base URL for supplier
    base_url: str = None

    def update(self, data):
        self.__dict__.update(data)