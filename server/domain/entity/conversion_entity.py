from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ConversionEntity(BaseModel):
    id_user: int
    file_name: Optional[str] = None
    file_size: int
    s3_file_key: str
    s3_zip_file_key: Optional[str] = None  # Only exists after the conversion finishes
    creation_date: datetime
    finished_date: Optional[datetime] = None  # Only exists after the conversion finishes
