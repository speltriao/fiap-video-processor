from datetime import datetime

from pydantic import BaseModel


class ConversionBaseDTO(BaseModel):
    id: int
    id_user: str
    creation_date: datetime
    model_config = {"extra": "ignore"}
