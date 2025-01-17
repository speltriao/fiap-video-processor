from typing import Optional

from server.adapters.input.sqs.dto.conversion_base_dto import ConversionBaseDTO


class ConversionInDTO(ConversionBaseDTO):
    file_name: Optional[str] = None
    s3_file_key: str
