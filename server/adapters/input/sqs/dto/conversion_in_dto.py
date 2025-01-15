from datetime import datetime

from pydantic import BaseModel


class ConversionInDTO(BaseModel):
    file_name: str
    file_size: int
    s3_link: str
    creation_date: datetime
