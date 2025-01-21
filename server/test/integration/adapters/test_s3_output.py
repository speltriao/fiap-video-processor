import pytest
from mockito import any as ANY
from mockito import verify, when

from server import test
from server.adapters.output.s3.handler.s3_out_handler import S3OutHandler
from server.env import Environment
from server.exception_handler import CustomException
from server.test.integration.adapters import ABCAdaptersTestBase


class TestS3Output(ABCAdaptersTestBase):
    _handler = S3OutHandler(Environment())

    @pytest.mark.asyncio
    async def test_upload_file_to_s3_success(self):
        when(self._handler)._perform_s3_operation(ANY()).thenReturn(test.future_none)
        result = await self._handler.upload_file_to_s3(self._mock_conversion)

        expected_s3_file_location = "output_zip/test.zip"
        assert result == expected_s3_file_location
        verify(self._handler, times=1)._perform_s3_operation(ANY())

    @pytest.mark.asyncio
    async def test_upload_file_to_s3_fail(self):
        mock_conversion = self._mock_conversion
        handler = S3OutHandler(Environment())
        exception_message = "S3 upload failed"

        when(handler)._perform_s3_operation(ANY()).thenRaise(Exception(exception_message))
        with pytest.raises(CustomException, match=exception_message):
            await handler.upload_file_to_s3(mock_conversion)

        verify(handler, times=1)._perform_s3_operation(ANY())
