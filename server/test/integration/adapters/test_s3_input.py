from unittest.mock import AsyncMock

import pytest
from mockito import any as ANY
from mockito import verify, when

from server import test
from server.adapters.input.s3.handler.s3_in_handler import S3InHandler
from server.env import Environment
from server.exception_handler import CustomException
from server.test import return_none
from server.test.integration.adapters import ABCAdaptersTestBase


class TestS3Input(ABCAdaptersTestBase):
    _handler = S3InHandler(Environment())

    @pytest.mark.asyncio
    async def test_download_file_from_s3_success(self):
        when(self._handler)._perform_s3_operation(ANY()).thenReturn(return_none())
        result = await self._handler.download_file_from_s3(self._mock_conversion, self._s3_key)

        assert result == "/tmp/test.mp4"
        verify(self._handler, times=1)._perform_s3_operation(ANY())

    @pytest.mark.asyncio
    async def test_download_file_from_s3_fail(self):
        # Mock the S3 operation to simulate a successful download
        when(self._handler)._perform_s3_operation(ANY()).thenRaise(Exception("exception_message"))
        # Run the test
        with pytest.raises(CustomException, match="exception_message"):
            await self._handler.download_file_from_s3(self._mock_conversion, self._s3_key)
