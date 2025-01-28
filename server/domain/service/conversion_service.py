import asyncio
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZipFile

import ffmpeg

from server import logger
from server.domain.entity.conversion_entity import ConversionEntity
from server.domain.usecase.abc_conversion_usecase import ABCConversionUseCase
from server.env import Environment
from server.exception_handler import CustomException, exception_handler


class ConversionService(ABCConversionUseCase):
    _id: int | None

    def __init__(self):
        self._local_temp_folder = Environment.TEMP_FOLDER
        self._zip_file_name: str | None = None

    async def create_conversion(self, conversion: ConversionEntity) -> ConversionEntity:
        logger.info("Initializing conversion")
        self._id = conversion.id
        file_name: str = conversion.file_name
        file_name_no_extension: str = file_name.split(".")[0]
        temp_images_output_folder = self._local_temp_folder + "/Images_" + file_name_no_extension

        os.makedirs(self._local_temp_folder, exist_ok=True)
        os.makedirs(temp_images_output_folder, exist_ok=True)

        await self._convert_video(conversion.local_video_path, temp_images_output_folder)
        conversion.local_zip_path = await self._create_images_zip(file_name_no_extension, temp_images_output_folder)
        conversion.finished_date = datetime.now(timezone.utc).isoformat()
        conversion.local_zip_file_name = self._zip_file_name
        logger.info("Conversion finished.")
        await self._delete_directory(temp_images_output_folder)

        return conversion

    @exception_handler
    async def _convert_video(self, video_temp_file_location: str, temp_images_output_folder: str) -> None:
        duration: float = self._get_video_duration(video_temp_file_location)
        interval: float = 20
        current_time: float = 0

        while current_time < duration:
            try:
                logger.info(f"Processing frame: {current_time} seconds")

                output_path: str = os.path.join(temp_images_output_folder, f"frame_at_{int(current_time)}.jpg")

                await asyncio.to_thread(
                    ffmpeg.input(video_temp_file_location, ss=current_time)
                    .filter("scale", 1920, 1080)
                    .output(output_path, vframes=1)
                    .run,
                    capture_stdout=True,
                    capture_stderr=True,
                )
            except Exception as e:
                logger.error(f"Error processing frame at {current_time} seconds: {e}")
                raise CustomException(id=self._id, message=e)
            else:
                logger.info(f"Frame successfully processed at {current_time} seconds")

            current_time += interval

    def _get_video_duration(self, local_video_path: str) -> float:
        """Obtains the video time lenght"""
        try:
            probe = ffmpeg.probe(local_video_path)
            return float(probe["format"]["duration"])
        except Exception as e:
            raise CustomException(id=self._id, message=e)

    @exception_handler
    async def _create_images_zip(self, file_name_no_extension: str, temp_images_output_folder: str) -> str:
        """Asynchronously creates the zip with all images
        and returns the temp location of the zip
        """
        try:
            return await asyncio.to_thread(self._zip_files, file_name_no_extension, temp_images_output_folder)
        except Exception as e:
            raise CustomException(id=self._id, message=e)

    def _zip_files(self, file_name_no_extension: str, folder_to_be_compreesed: str) -> str:
        """Creates the zip with images"""
        self._zip_file_name = f"{file_name_no_extension}.zip"
        zip_file_path: str = f"{self._local_temp_folder}/{self._zip_file_name}"
        with ZipFile(zip_file_path, "w") as zipf:
            for root, _, files in os.walk(folder_to_be_compreesed):
                for file in files:
                    zipf.write(os.path.join(root, file), arcname=file)
        return zip_file_path

    async def _delete_directory(self, path: str):
        """Asynchronously deletes a directory and its contents"""
        dir_path = Path(path)

        if not dir_path.exists():
            logger.warn(f"The directory '{dir_path}' does not exist.")
            return
        try:
            if dir_path.is_dir():
                await asyncio.to_thread(shutil.rmtree, dir_path, ignore_errors=False, onerror=None)
                logger.info(f"Directory '{dir_path}' and all its contents have been deleted.")
            else:
                logger.warn(f"The path '{dir_path}' is not a directory.")
        except Exception as e:
            logger.error(f"An error occurred while deleting the directory '{dir_path}': {e}")
