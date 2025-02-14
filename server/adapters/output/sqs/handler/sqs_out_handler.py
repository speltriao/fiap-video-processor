import aioboto3
from pydantic import BaseModel

from server import adapters, logger
from server.adapters.aws_services_enum import AWSServicesEnum
from server.adapters.output.sqs.dto.conversion_out_dto import ConversionErrorOutDTO
from server.adapters.output.sqs.mapper.conversion_out_mapper import ConversionOutMapper
from server.domain.entity.conversion_entity import ConversionEntity
from server.env import Environment


class SQSOutHandler:
    def __init__(self, env: Environment):
        self._queue_url = env.AWS_SQS_OUTPUT_QUEUE
        self._session = adapters.session

    async def send_success_message(self, completed_conversion: ConversionEntity, s3_video_path: str) -> None:
        """
        Send message to SQS Queue.
        """
        message_body = ConversionOutMapper.convert_from_entity(completed_conversion, s3_video_path)
        logger.info(f"Preparing to send message to SQS. Queue URL: {self._queue_url}")
        await self._send_message(message_body)

    async def send_error_message(self, id_request: id) -> None:
        """
        Send error message to SQS Queue (will notify the user via e-mail).
        """
        message_body: ConversionErrorOutDTO = ConversionOutMapper.convert_on_error(id_request)
        logger.info(f"Preparing to send error message to SQS. Queue URL: {self._queue_url}")

        await self._send_message(message_body, is_error=True)

    async def _send_message(self, message_body: BaseModel, is_error=False) -> None:
        async with self._session.client(service_name=AWSServicesEnum.SQS.value) as sqs_client:
            response = await sqs_client.send_message(QueueUrl=self._queue_url, MessageBody=message_body.json())
            logger.info(
                f"Message {'error' if is_error else ''} sent successfully to SQS. Message ID: {response.get('MessageId')}"
            )
