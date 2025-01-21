import json

from mockito import verify, when

from server.adapters import SQSOutHandler
from server.adapters.input.s3.handler.s3_in_handler import S3InHandler
from server.adapters.input.sqs.handler.sqs_in_handler import SQSInHandler
from server.domain.service.conversion_service import ConversionService
from server.env import Environment
from server.test import future_none, to_future
from server.test.integration.adapters import ABCAdaptersTestBase


class TestSQSInHandler(ABCAdaptersTestBase):
    import pytest

    @pytest.mark.asyncio
    async def test_receive_messages_success(self):
        # Mock environment and other dependencies
        when(ConversionService).create_conversion(self._mock_conversion).thenReturn(self._mock_conversion)

        when(SQSInHandler).receive_messages().thenReturn(
            to_future(
                {
                    "Messages": [
                        {
                            "MessageId": "12345",
                            "Body": json.dumps(
                                {
                                    "id": self._mock_conversion.id,
                                    "s3_file_key": self._mock_conversion.local_zip_file_name,
                                }
                            ),
                        }
                    ]
                }
            )
        )

        when(S3InHandler).download_file_from_s3(self._mock_conversion, self._s3_key).thenReturn(
            to_future("/path/to/test.mp4")
        )
        when(SQSOutHandler).send_success_message(self._mock_conversion, self._s3_key).thenReturn(future_none)

        # Run the message receiving method asynchronously
        await SQSInHandler(Environment(), ConversionService()).receive_messages()
        verify(SQSInHandler, times=1).receive_messages()
