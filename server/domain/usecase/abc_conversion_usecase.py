from abc import ABC, abstractmethod
from typing import List

from server.domain.entity.conversion_entity import ConversionEntity


class ABCConversionUseCase(ABC):
    @abstractmethod
    async def create_conversion(self, conversion: ConversionEntity) -> ConversionEntity:
        """Create a new video conversion into images"""
        pass
