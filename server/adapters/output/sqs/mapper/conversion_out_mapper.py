from server.adapters.output.sqs.dto.conversion_out_dto import ConversionOutDTO
from server.adapters.output.sqs.enum.conversion_status_enum import ConversionStatusEnum
from server.domain.entity.conversion_entity import ConversionEntity


class ConversionOutMapper:
    @staticmethod
    def convert_from_entity(entity: ConversionEntity, s3_video_path: str) -> ConversionOutDTO:
        return ConversionOutDTO(
            id=entity.id,
            id_user=entity.id_user,
            s3_zip_file_key=s3_video_path,
            creation_date=entity.creation_date,
            finished_date=entity.finished_date,
            status=ConversionStatusEnum.success.value,  # Error will come as exceptions
        )
