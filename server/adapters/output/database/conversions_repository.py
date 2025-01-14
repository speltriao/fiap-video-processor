from typing import List

from sqlalchemy import select

from server.adapters.output.database import async_session
from server.adapters.output.database.conversion_model import ConversionModel
from server.domain.entity.conversion_entity import ConversionModel
from server.domain.repository.abc_conversion_repository import ABCConversionRepository


class ConversionRepository(ABCConversionRepository):
    async def list_all_conversions(self) -> List[ConversionModel]:
        async with async_session() as session:
            result = await session.execute(select(ConversionModel))
            conversions = result.mappings().all()

            return [ConversionModel(**conversion) for conversion in conversions]

    async def insert_conversion(self, conversion: ConversionModel) -> ConversionModel:
        async with async_session() as session:
            session.add(conversion)
            await session.flush()  # You can use flush to push changes to the DB
            await session.commit()  # Commit the changes
            return conversion
