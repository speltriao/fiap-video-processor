import os
from datetime import datetime
from zipfile import ZipFile

import ffmpeg

from server import logger
from server.adapters import session
from server.adapters.aws_services_enum import AWSServicesEnum
from server.adapters.output.database.conversions_repository import ConversionRepository
from server.domain.entity.conversion_entity import ConversionEntity
from server.domain.repository.abc_conversion_repository import ABCConversionRepository
from server.domain.usecase.abc_conversion_usecase import ABCConversionUseCase


class ConversionService(ABCConversionUseCase):
    bucket_name = "your-bucket-name"  # TODO: define bucket name

    def __init__(self):
        self.conversion_repository: ABCConversionRepository = ConversionRepository()
        self.s3_client = session.client(service_name=AWSServicesEnum.S3)

    async def create_conversion(self, conversion: ConversionEntity) -> ConversionEntity:
        conversion: ConversionEntity = await self._convert_video(conversion)
        conversion_with_id: ConversionEntity = self.conversion_repository.insert_conversion(conversion)
        return conversion_with_id

    async def _download_file_from_s3(self, path: str, s3_link: str):
        """Asynchronously download a file from S3 to local file system."""
        async with self.s3_client as s3_client:
            await s3_client.download_file(self.bucket_name, s3_link, path)
            logger.info(f"Downloaded file from S3: {s3_link} to {path}")

    async def _upload_file_to_s3(self, path: str, s3_link: str):
        """Asynchronously upload a file from local file system to S3."""
        async with self.s3_client as s3_client:
            await s3_client.upload_file(path, self.bucket_name, s3_link)
            logger.info(f"Uploaded file to S3: {path} to {s3_link}")

    def _get_video_duration(self, video_path: str):
        probe = ffmpeg.probe(video_path)
        return float(probe["format"]["duration"])

    async def _create_images_zip(self, temp_output_folder: str, s3_link: str):
        temp_zip_file_path = "/tmp/images.zip"

        with ZipFile(temp_zip_file_path, "w") as zipf:
            for root, _, files in os.walk(temp_output_folder):
                for file in files:
                    zipf.write(os.path.join(root, file), arcname=file)

        await self._upload_file_to_s3(temp_zip_file_path, s3_link)

    async def _convert_video(self, conversion: ConversionEntity):
        logger.info("Processo iniciado:")
        await self._download_file_from_s3(conversion.file_name, conversion.s3_link)

        temp_video_path = "/tmp/" + conversion.file_name  # Temporary path for video
        temp_output_folder = "/tmp/Images"  # Temporary folder for images

        os.makedirs(temp_output_folder, exist_ok=True)

        duration = self._get_video_duration(temp_video_path)
        interval = 20
        current_time = 0
        while current_time < duration:
            logger.info(f"Processando frame: {current_time} segundos")

            output_path = os.path.join(temp_output_folder, f"frame_at_{int(current_time)}.jpg")
            (
                ffmpeg.input(temp_video_path, ss=current_time)
                .filter("scale", 1920, 1080)
                .output(output_path, vframes=1)
                .run(capture_stdout=True, capture_stderr=True)
            )
            current_time += interval

        await self._create_images_zip(temp_output_folder, conversion.s3_link)

        logger.info("Processo finalizado.")
        conversion.finished_date = datetime.now()
        return conversion
