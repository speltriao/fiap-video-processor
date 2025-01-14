from datetime import datetime

from pydantic import BaseModel


class ConversionModel(BaseModel):
    id: int
    file_name: str
    file_size: str
    date: datetime
    model_config = {"from_attributes": True}
