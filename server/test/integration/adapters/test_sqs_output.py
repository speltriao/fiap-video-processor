from unittest.mock import AsyncMock, patch

import pytest

from server.adapters import SQSOutHandler
from server.domain.entity.conversion_entity import ConversionEntity
from server.test.integration.adapters import ABCAdaptersTestBase


class TestSQSOutputHandler(ABCAdaptersTestBase):
    # Mock ConversionEntity and ConversionOutMapper for the test
    @pytest.fixture
    def mock_conversion_entity(self):
        return AsyncMock(spec=ConversionEntity)

    @pytest.fixture
    def mock_conversion_out_mapper(self):
        with patch(
            "server.adapters.output.sqs.mapper.conversion_out_mapper.ConversionOutMapper.convert_from_entity"
        ) as mock_mapper:
            yield mock_mapper

    @pytest.mark.asyncio
    async def test_send_success_message(self, mock_conversion_entity, mock_conversion_out_mapper):
        # Mock queue URL and response
        mock_queue_url = "https://sqs.fake-queue-url.amazonaws.com/123456789012/MyQueue"
        mock_message_id = "12345"

        # Mock SQS client and its methods
        mock_sqs_client = AsyncMock()
        mock_sqs_client.send_message.return_value = {"MessageId": mock_message_id}

        # Patch adapters.session.client to return the mock SQS client
        with patch("server.adapters.session.client", return_value=mock_sqs_client):
            # Initialize SQSOutHandler with mocked environment
            handler = SQSOutHandler(env=AsyncMock(AWS_SQS_OUTPUT_QUEUE=mock_queue_url))

            # Set up the mock for the conversion mapper
            mock_conversion_out_mapper.return_value.json.return_value = '{"mocked_key": "mocked_value"}'

            # Call the method under test
            await handler.send_success_message(mock_conversion_entity, "s3://mocked-bucket/mock-video-path")

            # Assertions
            mock_conversion_out_mapper.assert_called_once_with(
                mock_conversion_entity, "s3://mocked-bucket/mock-video-path"
            )
