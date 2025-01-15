from server.adapters.output.database import async_session
from server.adapters.output.database.conversion_model import ConversionModel
from server.domain.entity.conversion_entity import ConversionEntity
from server.domain.repository.abc_conversion_repository import ABCConversionRepository


class ConversionRepository(ABCConversionRepository):
    async def insert_conversion(self, entity: ConversionEntity) -> ConversionEntity:
        async with async_session() as session:
            model = ConversionModel(
                file_name=entity.file_name,
                file_size=entity.file_size,
                s3_link=entity.s3_link,
                creation_date=entity.creation_date,
                finished_date=entity.finished_date,
            )
            session.add(model)
            await session.flush()
            await session.commit()
            await session.refresh(model)

            return ConversionEntity.model_validate(model)
