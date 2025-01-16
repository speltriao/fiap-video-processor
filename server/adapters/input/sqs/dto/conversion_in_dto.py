from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ConversionInDTO(BaseModel):
    id_user: int
    file_name: Optional[str] = None
    file_size: int
    s3_file_key: str
    creation_date: datetime
    model_config = {"extra": "ignore"}
