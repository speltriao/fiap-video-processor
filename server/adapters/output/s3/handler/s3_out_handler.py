import traceback

from server import logger
from server.adapters.abc_base_s3 import ABCBaseS3
from server.domain.entity.conversion_entity import ConversionEntity
from server.env import Environment
from server.exception_handler import CustomException, exception_handler


class S3OutHandler(ABCBaseS3):
    def __init__(self, env: Environment):
        super().__init__(env)

    @exception_handler
    async def upload_file_to_s3(self, conversion: ConversionEntity) -> str:
        """Asynchronously upload a file from local file system to S3."""
        s3_file_location: str = "output_zip/" + conversion.local_zip_file_name
        try:
            await self._perform_s3_operation(
                lambda client: client.upload_file(conversion.local_zip_path, self._bucket_name, s3_file_location)
            )
            logger.info(f"Uploaded file to S3: {conversion.local_zip_path} to {s3_file_location}")
            return s3_file_location
        except Exception as e:
            logger.error(f"Failed to upload file to S3: {conversion.local_zip_path} to {s3_file_location}")
            logger.error(f"Exception: {str(e)}")
            logger.error("Traceback: %s", traceback.format_exc())
            raise CustomException(id=conversion.id, message=e)
