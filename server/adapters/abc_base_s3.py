import traceback
from abc import ABC
from typing import Callable

from server import adapters, logger
from server.adapters.aws_services_enum import AWSServicesEnum
from server.env import Environment


class ABCBaseS3(ABC):
    def __init__(self, env: Environment):
        self._bucket_name = env.AWS_S3_BUCKET_NAME
        self._bucket_output_folder = env.AWS_S3_BUCKET_OUTPUT_FOLDER
        self._local_temp_folder = env.TEMP_FOLDER
        self._temp_images_output_folder = self._local_temp_folder + "/Images"  # Temporary folder for images

    async def _perform_s3_operation(self, operation: Callable) -> None:
        """Helper method to perform an operation on S3 using the same client."""
        try:
            async with adapters.session.client(service_name=AWSServicesEnum.S3.value) as s3_client:
                await operation(s3_client)
        except Exception as e:
            logger.error(f"Error performing S3 operation: {e}")
            logger.error(traceback.format_exc())
            raise e
