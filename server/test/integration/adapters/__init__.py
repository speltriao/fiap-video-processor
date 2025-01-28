from abc import ABC
from datetime import datetime

from server.adapters.output.sqs.enum.conversion_status_enum import ConversionStatusEnum
from server.domain.entity.conversion_entity import ConversionEntity


class ABCAdaptersTestBase(ABC):
    _mock_conversion = ConversionEntity(
        id=1,
        id_user="user123",
        file_name="test.mp4",
        creation_date=datetime.now(),
        local_video_path="/path/to/test.mp4",
        local_zip_file_name="test.zip",
        finished_date=datetime.now(),
        status=ConversionStatusEnum.ok.value,
    )
    _s3_key = "output_zip/test.zip"
