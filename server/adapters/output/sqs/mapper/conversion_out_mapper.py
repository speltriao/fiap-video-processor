from server.adapters.input.sqs.dto.conversion_in_dto import ConversionInDTO
from server.adapters.output.sqs.dto.conversion_out_dto import ConversionErrorOutDTO, ConversionOutDTO
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
            status=ConversionStatusEnum.ok.value,
        )

    @staticmethod
    def convert_on_error(id_request: id) -> ConversionErrorOutDTO:
        return ConversionErrorOutDTO(
            id=id_request,
            status=ConversionStatusEnum.error.value,
        )
