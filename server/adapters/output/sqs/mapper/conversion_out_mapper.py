from server.adapters.output.sqs.dto.conversion_out_dto import ConversionOutDTO
from server.domain.entity.conversion_entity import ConversionEntity


class ConversionOutMapper:
    @staticmethod
    def convert_from_entity(entity: ConversionEntity) -> ConversionOutDTO:
        return ConversionOutDTO(
            id_user=entity.id_user,
            file_name=entity.file_name,
            file_size=entity.file_size,
            s3_file_key=entity.s3_file_key,
            s3_zip_file_key=entity.s3_zip_file_key,
            creation_date=entity.creation_date,
            finished_date=entity.finished_date,
        )
