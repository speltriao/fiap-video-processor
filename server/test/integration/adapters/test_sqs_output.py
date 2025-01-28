from datetime import datetime
from unittest.mock import AsyncMock, patch

import pytest

from server.adapters import SQSOutHandler
from server.adapters.output.sqs.dto.conversion_out_dto import ConversionOutDTO
from server.adapters.output.sqs.enum.conversion_status_enum import ConversionStatusEnum
from server.adapters.output.sqs.mapper.conversion_out_mapper import ConversionOutMapper
from server.domain.entity.conversion_entity import ConversionEntity
from server.env import Environment
from server.test.integration import ABCTestBase


class TestSQSOutputHandler(ABCTestBase):
    @pytest.mark.asyncio
    async def test_send_success_message(self):
        mocked_sqs_client = AsyncMock()
        mocked_response = {"MessageId": "test-message-id"}

        # Create an instance of the handler
        handler = SQSOutHandler(Environment())

        # Prepare mock data for ConversionOutDTO
        conversion_out_dto_instance = ConversionOutDTO(
            id=1,
            id_user="user_123",
            creation_date=datetime(2025, 1, 22, 10, 30),
            finished_date=datetime(2025, 1, 22, 15, 45),
            s3_zip_file_key="s3://bucket/key/to/zipfile.zip",
            status=ConversionStatusEnum.ok,
        )

        # Mock the SQS client
        handler._sqs_client = mocked_sqs_client

        # Mock the ConversionOutMapper's convert_from_entity method
        with patch.object(ConversionOutMapper, "convert_from_entity", return_value=conversion_out_dto_instance):
            # Mock the actual _send_message method
            with patch.object(SQSOutHandler, "_send_message", new_callable=AsyncMock) as mock_send_message:
                # Mock the send_message response
                mock_send_message.return_value = mocked_response

                completed_conversion = AsyncMock(spec=ConversionEntity)
                s3_video_path = "s3://example-bucket/example-path"

                # Call the method under test
                await handler.send_success_message(completed_conversion, s3_video_path)

                # Assert _send_message was called with the expected arguments
                mock_send_message.assert_called_once_with(conversion_out_dto_instance)
