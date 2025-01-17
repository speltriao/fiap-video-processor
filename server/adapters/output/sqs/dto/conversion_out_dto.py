from datetime import datetime

from pydantic import BaseModel

from server.adapters.input.sqs.dto.conversion_base_dto import ConversionBaseDTO
from server.adapters.output.sqs.enum.conversion_status_enum import ConversionStatusEnum


class ConversionOutDTO(ConversionBaseDTO):
    finished_date: datetime
    s3_zip_file_key: str
    status: ConversionStatusEnum


class ConversionErrorOutDTO(BaseModel):
    id: int
    status: ConversionStatusEnum
