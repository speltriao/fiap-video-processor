import json
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

import pytest
from mockito import any as ANY
from mockito import verify, when

from server.adapters import SQSOutHandler
from server.adapters.input.s3.handler.s3_in_handler import S3InHandler
from server.adapters.input.sqs.handler.sqs_in_handler import SQSInHandler
from server.adapters.output.s3.handler.s3_out_handler import S3OutHandler
from server.domain.entity.conversion_entity import ConversionEntity
from server.domain.service.conversion_service import ConversionService
from server.domain.usecase.abc_conversion_usecase import ABCConversionUseCase
from server.env import Environment
from server.exception_handler import CustomException
from server.test import future_none, to_future
from server.test.integration.adapters import ABCAdaptersTestBase


class TestSQSInHandler(ABCAdaptersTestBase):
    import json
    from unittest.mock import AsyncMock

    import pytest
    from mockito import mock, verify, when

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
