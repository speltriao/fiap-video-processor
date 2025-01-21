from abc import ABC
from datetime import datetime

from server.adapters.output.s3.handler.s3_out_handler import S3OutHandler
from server.domain.entity.conversion_entity import ConversionEntity
from server.env import Environment


class ABCAdaptersTestBase(ABC):
    _mock_conversion = ConversionEntity(
        id=1,
        id_user="user123",
        file_name="test.mp4",
        creation_date=datetime.now(),
        local_video_path="/path/to/test.mp4",
        local_zip_file_name="test.zip",
    )
    _s3_key = "output_zip/test.zip"
