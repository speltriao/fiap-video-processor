import asyncio
import os
from datetime import datetime
from zipfile import ZipFile

import ffmpeg

from server import logger
from server.domain.entity.conversion_entity import ConversionEntity
from server.domain.usecase.abc_conversion_usecase import ABCConversionUseCase
from server.env import Environment


class ConversionService(ABCConversionUseCase):
    def __init__(self):
        self._local_temp_folder = Environment.TEMP_FOLDER
        self._temp_images_output_folder = self._local_temp_folder + "/Images"  # Temporary folder for images
        self._zip_file_name: str | None

    async def create_conversion(self, conversion: ConversionEntity) -> ConversionEntity:
        logger.info("Initializing conversion")
        file_name: str = conversion.file_name
        file_name_no_extension: str = file_name.split(".")[0]
        self._temp_images_output_folder += "_" + file_name_no_extension

        os.makedirs(self._local_temp_folder, exist_ok=True)
        os.makedirs(self._temp_images_output_folder, exist_ok=True)

        await self._convert_video(conversion.local_video_path)
        conversion.local_zip_path = await self._create_images_zip(file_name_no_extension)
        conversion.finished_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        conversion.local_zip_file_name = self._zip_file_name
        logger.info("Conversion finished.")
        # await self.__delete_folders_async([self._temp_images_output_folder,])

        return conversion

    import logging

    logger = logging.getLogger(__name__)

    async def _convert_video(self, video_temp_file_location: str) -> None:
        duration: float = self._get_video_duration(video_temp_file_location)
        interval: float = 20
        current_time: float = 0

        while current_time < duration:
            try:
                logger.info(f"Processing frame: {current_time} seconds")

                output_path: str = os.path.join(self._temp_images_output_folder, f"frame_at_{int(current_time)}.jpg")
                (
                    ffmpeg.input(video_temp_file_location, ss=current_time)
                    .filter("scale", 1920, 1080)
                    .output(output_path, vframes=1)
                    .run(capture_stdout=True, capture_stderr=True)
                )
            except Exception as e:
                logger.error(f"Error processing frame at {current_time} seconds: {e}")
            else:
                logger.info(f"Frame successfully processed at {current_time} seconds")

            current_time += interval

    def _get_video_duration(self, local_video_path: str) -> float:
        probe = ffmpeg.probe(local_video_path)
        return float(probe["format"]["duration"])

    async def _create_images_zip(self, file_name_no_extension: str) -> str:
        """Asynchronously creates the zip with all images
        and returns the temp location of the zip
        """
        return await asyncio.to_thread(self._zip_files, file_name_no_extension)

    def _zip_files(self, file_name_no_extension: str) -> str:
        """Creates the zip with images"""
        folder_to_be_compreesed = self._temp_images_output_folder
        self._zip_file_name = f"{file_name_no_extension}.zip"
        zip_file_path: str = f"{self._local_temp_folder}/{self._zip_file_name}"
        with ZipFile(zip_file_path, "w") as zipf:
            for root, _, files in os.walk(folder_to_be_compreesed):
                for file in files:
                    zipf.write(os.path.join(root, file), arcname=file)
        return zip_file_path

    # async def __delete_local_files_folders(self, paths: list[str]):
    # Asynchronously deletes local temp files and folders.
    #     type
    #     for path in paths:
    #         folder = Path(path)
    #
    #         if not folder.exists():
    #             logger.warn(f"The folder '{folder_path}' does not exist.")
    #             continue
    #
    #         try:
    #             await asyncio.to_thread(shutil.rmtree, folder_path, ignore_errors=False, onerror=None)
    #             logger.info(f"Folder '{folder_path}' and all its contents have been deleted.")
    #         except PermissionError:
    #             logger.error(f"Permission denied: Unable to delete the folder '{folder_path}'.")
    #         except Exception as e:
    #             logger.error(f"An error occurred while deleting the folder: {e}")
