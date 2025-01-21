import asyncio
import os
from datetime import datetime

import pytest
from mockito import any as ANY
from mockito import mock, unstub, verify, when

from server import test
from server.adapters.output.s3.handler.s3_out_handler import S3OutHandler
from server.domain.entity.conversion_entity import ConversionEntity
from server.env import Environment


class TestS3Integration:
    mock_conversion = ConversionEntity(
        id=1,
        id_user="user123",
        file_name="test.mp4",
        creation_date=datetime.now(),
        local_video_path="/path/to/test.mp4",
        local_zip_file_name="test.zip",
    )

    @pytest.mark.asyncio
    async def test_upload_file_to_s3_success(self):
        mock_conversion = self.mock_conversion
        handler = S3OutHandler(Environment())

        when(handler)._perform_s3_operation(ANY()).thenReturn(test.future_none)
        result = await handler.upload_file_to_s3(mock_conversion)

        expected_s3_file_location = "output_zip/test.zip"
        assert result == expected_s3_file_location
        verify(handler, times=1)._perform_s3_operation(ANY())
