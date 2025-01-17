import traceback
from typing import Callable

from server import adapters, logger
from server.adapters.abc_base_s3 import ABCBaseS3
from server.adapters.aws_services_enum import AWSServicesEnum
from server.adapters.input.sqs.dto.conversion_in_dto import ConversionInDTO
from server.domain.entity.conversion_entity import ConversionEntity
from server.env import Environment


class S3InHandler(ABCBaseS3):
    def __init__(self, env: Environment):
        super().__init__(env)

    async def download_file_from_s3(self, conversion_entity: ConversionEntity, s3_file_key: str) -> str:
        """Asynchronously download a file from S3 to local file system."""
        video_temp_file_location: str = self._local_temp_folder + "/" + conversion_entity.file_name
        try:
            await self._perform_s3_operation(
                lambda op, l_path=video_temp_file_location, s_key=s3_file_key: op.download_file(
                    self._bucket_name, s_key, video_temp_file_location
                )
            )
            logger.info(f"Downloaded file from S3: {s3_file_key} to {video_temp_file_location}")
        except Exception as e:
            logger.error(f"Error downloading file from S3: {s3_file_key} to {video_temp_file_location}. Error: {e}")
            raise
        return video_temp_file_location
