from typing import List

from server.adapters.output.database.conversions_repository import ConversionRepository
from server.domain.entity.conversion_entity import ConversionModel
from server.domain.repository.abc_conversion_repository import ABCConversionRepository
from server.domain.usecase.abc_conversion_usecase import ABCConversionUseCase


class ConversionService(ABCConversionUseCase):
    def __init__(self):
        self.conversion_repository: ABCConversionRepository = ConversionRepository()

    def list_all_conversions(self) -> List[ConversionModel]:
        return self.conversion_repository.list_all_conversions()

    def create_conversion(self, conversion: ConversionModel) -> ConversionModel:
        # TODO: Convert video
        return self.conversion_repository.insert_conversion(conversion)
