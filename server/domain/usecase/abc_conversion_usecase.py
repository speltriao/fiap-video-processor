from abc import ABC, abstractmethod
from typing import List

from server.domain.entity.conversion_entity import ConversionModel


class ABCConversionUseCase(ABC):
    @abstractmethod
    def list_all_conversions(self) -> List[ConversionModel]:
        """List all the conversions"""
        pass

    @abstractmethod
    def create_conversion(self, conversion: ConversionModel) -> ConversionModel:
        """Create a new conversion and save its details to the DB"""
        pass

    # TODO: complete use case(s)
