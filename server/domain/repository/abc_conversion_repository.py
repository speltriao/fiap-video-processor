from abc import ABC, abstractmethod
from typing import List

from server.domain.entity.conversion_entity import ConversionModel


class ABCConversionRepository(ABC):
    @abstractmethod
    def list_all_conversions(self) -> List[ConversionModel]:
        """List all the conversions currently in the DB"""
        pass

    @abstractmethod
    def insert_conversion(self, conversion: ConversionModel) -> ConversionModel:
        """Add a conversion to the DB"""
        pass
