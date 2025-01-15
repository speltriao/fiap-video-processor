from abc import ABC, abstractmethod
from typing import List

from server.domain.entity.conversion_entity import ConversionEntity


class ABCConversionRepository(ABC):
    @abstractmethod
    def insert_conversion(self, conversion: ConversionEntity) -> ConversionEntity:
        """Add a conversion to the DB and return it (with ID)."""
        pass
