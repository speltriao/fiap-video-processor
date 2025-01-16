from datetime import datetime

from server.adapters.input.sqs.dto.conversion_in_dto import ConversionInDTO


class ConversionOutDTO(ConversionInDTO):
    finished_date: datetime
    s3_zip_file_key: str
