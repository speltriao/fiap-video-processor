from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ConversionEntity(BaseModel):
    id: int
    id_user: str
    file_name: str  # Video file name (with extension)
    creation_date: datetime
    local_video_path: Optional[str] = None  # Only exists after the download finishes
    local_zip_path: Optional[str] = None  # Only exists after the conversion finishes
    local_zip_file_name: Optional[str] = None  # Only exists after the conversion finishes
    finished_date: Optional[datetime] = None  # Only exists after the conversion finishes
