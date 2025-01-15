from datetime import datetime

from server.adapters.input.sqs.dto.conversion_in_dto import ConversionInDTO


class ConversionOutDTO(ConversionInDTO):
    id: int
    finished_date: datetime
