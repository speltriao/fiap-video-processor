import json
from unittest.mock import AsyncMock, MagicMock, PropertyMock, patch

import pytest
from mockito import any as ANY
from mockito import when

from server import adapters
from server.adapters import SQSOutHandler
from server.adapters.aws_services_enum import AWSServicesEnum
from server.adapters.input.s3.handler.s3_in_handler import S3InHandler
from server.adapters.input.sqs.handler.sqs_in_handler import SQSInHandler
from server.adapters.output.s3.handler.s3_out_handler import S3OutHandler
from server.domain.service.conversion_service import ConversionService
from server.env import Environment
from server.test import to_future
from server.test.integration.adapters import ABCAdaptersTestBase


class TestSQSInHandler(ABCAdaptersTestBase):
    @pytest.mark.asyncio
    async def test_receive_messages_success(self):
        mock_sqs_client = AsyncMock()
        mock_sqs_client.receive_message.return_value = {
            "Messages": [
                {
                    "MessageId": "12345",
                    "Body": json.dumps(
                        {
                            "id": self._mock_conversion.id,
                            "id_user": self._mock_conversion.id_user,
                            "creation_date": "2025-01-27T18:47:39.566249",
                            "s3_file_key": "a/t.zip",
                        }
                    ),
                }
            ]
        }

        mock_context_manager = MagicMock()
        mock_context_manager.__aenter__.return_value = mock_sqs_client
        mock_context_manager.__aexit__.return_value = None

        when(adapters.session).client(service_name=AWSServicesEnum.SQS.value).thenReturn(mock_context_manager)

        when(ConversionService).create_conversion(self._mock_conversion).thenReturn(self._mock_conversion)
        when(S3InHandler).download_file_from_s3(ANY(), ANY()).thenReturn(to_future("/path/to/test.mp4"))
        when(SQSOutHandler).send_success_message(ANY(), ANY()).thenReturn(to_future("/pa1th/to/test.mp4"))
        when(ConversionService).create_conversion(ANY()).thenReturn(to_future(self._mock_conversion))
        when(S3OutHandler).upload_file_to_s3(ANY()).thenReturn(to_future("/pathad/to/test.mp4"))
        mock_sqs_client.delete_message.return_value = None

        sentinel = PropertyMock(side_effect=[True, False])

        with patch.object(SQSInHandler, "RUNNING", sentinel):
            sqs_in = SQSInHandler(Environment(), ConversionService())

            await sqs_in.receive_messages()

        # Verify calls to receive_message
        mock_sqs_client.receive_message.assert_called_once
