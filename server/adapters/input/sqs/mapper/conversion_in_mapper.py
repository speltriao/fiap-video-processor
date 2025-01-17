from server.adapters.input.sqs.dto.conversion_in_dto import ConversionInDTO
from server.domain.entity.conversion_entity import ConversionEntity


class ConversionInMapper:
    @staticmethod
    def convert_to_entity(dto: ConversionInDTO) -> ConversionEntity:
        return ConversionEntity(
            id=dto.id,
            id_user=dto.id_user,
            file_name=dto.file_name if dto.file_name else dto.s3_file_key.split("/", 1)[1],
            s3_file_key=dto.s3_file_key,
            creation_date=dto.creation_date,
        )
