from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ConversionEntity(BaseModel):
    id: Optional[int] = None  # Only exists after being populated by the DB
    file_name: str
    file_size: int
    s3_link: str
    creation_date: datetime
    finished_date: Optional[datetime] = None  # Only exists after the conversion finishes
    model_config = {"from_attributes": True}
