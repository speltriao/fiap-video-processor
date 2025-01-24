from datetime import datetime
from unittest.mock import AsyncMock

import pytest
from mockito import any as ANY
from mockito import mock, unstub, verify, when

from server.adapters import SQSOutHandler
from server.adapters.output.sqs.dto.conversion_out_dto import ConversionOutDTO
from server.adapters.output.sqs.enum.conversion_status_enum import ConversionStatusEnum
from server.adapters.output.sqs.mapper.conversion_out_mapper import ConversionOutMapper
from server.domain.entity.conversion_entity import ConversionEntity
from server.env import Environment
from server.test.integration.adapters import ABCAdaptersTestBase


class TestSQSOutputHandler(ABCAdaptersTestBase):
    @pytest.mark.asyncio
    async def test_send_success_message(self):
        mocked_sqs_client = AsyncMock()  # Use AsyncMock instead of mock
        mocked_response = {"MessageId": "test-message-id"}

        handler = SQSOutHandler(Environment())
        conversion_out_dto_instance = ConversionOutDTO(
            id=1,
            id_user="user_123",
            creation_date=datetime(2025, 1, 22, 10, 30),
            finished_date=datetime(2025, 1, 22, 15, 45),
            s3_zip_file_key="s3://bucket/key/to/zipfile.zip",
            status=ConversionStatusEnum.ok,
        )
        handler._sqs_client = mocked_sqs_client
        when(ConversionOutMapper).convert_from_entity(ANY(), ANY()).thenReturn(conversion_out_dto_instance)
        when(mocked_sqs_client).send_message(
            QueueUrl=handler._queue_url,
            MessageBody=mock().json(),
        ).thenReturn(mocked_response)

        completed_conversion = mock(ConversionEntity)
        s3_video_path = "s3://example-bucket/example-path"

        await handler.send_success_message(completed_conversion, s3_video_path)

        verify(mocked_sqs_client).send_message(
            QueueUrl=handler._queue_url,
            MessageBody=mock().json(),
        )
        unstub()
