from server.adapters.output.sqs.dto.conversion_out_dto import ConversionOutDTO
from server.domain.entity.conversion_entity import ConversionEntity


class ConversionOutMapper:
    @staticmethod
    def convert_from_entity(entity: ConversionEntity) -> ConversionOutDTO:
        return ConversionOutDTO(
            id=entity.id,
            file_name=entity.file_name,
            file_size=entity.file_size,
            s3_link=entity.s3_link,
            creation_date=entity.creation_date,
            finished_date=entity.finished_date,
        )
