import os
import traceback
from datetime import datetime
from typing import Callable, Coroutine
from zipfile import ZipFile

import ffmpeg

from server import adapters, logger
from server.adapters.aws_services_enum import AWSServicesEnum
from server.domain.entity.conversion_entity import ConversionEntity
from server.domain.usecase.abc_conversion_usecase import ABCConversionUseCase
from server.env import Environment


class ConversionService(ABCConversionUseCase):
    def __init__(self):
        self.bucket_name = Environment.AWS_S3_BUCKET_NAME
        self.bucket_output_folder = Environment.AWS_S3_BUCKET_OUTPUT_FOLDER
        self.local_temp_folder = Environment.TEMP_FOLDER
        self.temp_images_output_folder = self.local_temp_folder + "/Images"  # Temporary folder for images

    async def create_conversion(self, conversion: ConversionEntity) -> ConversionEntity:
        logger.info("Processo iniciado:")

        file_name: str = (
            conversion.s3_file_key.split("/", 0)[1] if conversion.file_name is None else conversion.file_name
        )
        file_name_no_extension: str = file_name.split(".")[0]
        self.temp_images_output_folder += "_" + file_name_no_extension
        video_temp_file_location: str = self.local_temp_folder + "/" + file_name

        os.makedirs(self.local_temp_folder, exist_ok=True)
        os.makedirs(self.temp_images_output_folder, exist_ok=True)

        await self._download_file_from_s3(conversion.s3_file_key, video_temp_file_location)
        await self._convert_video(video_temp_file_location)
        temp_zip_file_path: str = await self._create_images_zip(self.temp_images_output_folder)
        output_s3_file_key: str = self.bucket_output_folder + file_name_no_extension + ".zip"
        await self._upload_file_to_s3(temp_zip_file_path, output_s3_file_key)

        logger.info("Processo finalizado.")
        conversion.finished_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        conversion.s3_zip_file_key = output_s3_file_key
        return conversion

    async def _convert_video(self, video_temp_file_location: str):
        duration: float = self._get_video_duration(video_temp_file_location)
        interval: float = 20
        current_time: float = 0
        while current_time < duration:
            logger.info(f"Processando frame: {current_time} segundos")

            output_path: str = os.path.join(self.temp_images_output_folder, f"frame_at_{int(current_time)}.jpg")
            (
                ffmpeg.input(video_temp_file_location, ss=current_time)
                .filter("scale", 1920, 1080)
                .output(output_path, vframes=1)
                .run(capture_stdout=True, capture_stderr=True)
            )
            current_time += interval

    async def _perform_s3_operation(self, operation: Callable) -> None:
        """Helper method to perform an operation on S3 using the same client."""
        try:
            async with adapters.session.client(service_name=AWSServicesEnum.S3.value) as s3_client:
                await operation(s3_client)
        except Exception as e:
            logger.error(f"Error performing S3 operation: {e}")
            trace = traceback.format_exc()
            logger.error(trace)

    async def _download_file_from_s3(self, s3_file_key: str, video_temp_file_location: str) -> None:
        """Asynchronously download a file from S3 to local file system."""
        try:
            await self._perform_s3_operation(
                lambda op, l_path=video_temp_file_location, s_key=s3_file_key: op.download_file(
                    self.bucket_name, s_key, video_temp_file_location
                )
            )
            logger.info(f"Downloaded file from S3: {s3_file_key} to {video_temp_file_location}")
        except Exception as e:
            logger.error(f"Error downloading file from S3: {s3_file_key} to {video_temp_file_location}. Error: {e}")
            raise  # Re-raise the exception after logging it

    async def _upload_file_to_s3(self, local_path: str, s3_file_key: str) -> None:
        """Asynchronously upload a file from local file system to S3."""
        await self._perform_s3_operation(
            lambda op, l_path=local_path, s_key=s3_file_key: op.upload_file(l_path, self.bucket_name, s_key)
        )
        logger.info(f"Uploaded file to S3: {local_path} to {s3_file_key}")

    def _get_video_duration(self, local_video_path: str) -> float:
        probe = ffmpeg.probe(local_video_path)
        return float(probe["format"]["duration"])

    async def _create_images_zip(self, temp_output_folder: str) -> str:
        temp_zip_file_path: str = temp_output_folder + ".zip"

        with ZipFile(temp_zip_file_path, "w") as zipf:
            for root, _, files in os.walk(temp_output_folder):
                for file in files:
                    zipf.write(os.path.join(root, file), arcname=file)
        return temp_zip_file_path
