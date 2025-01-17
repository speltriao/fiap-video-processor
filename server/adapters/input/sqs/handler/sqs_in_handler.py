import asyncio
import json
from typing import Any

from aiobotocore import client

from server import adapters, logger
from server.adapters.aws_services_enum import AWSServicesEnum
from server.adapters.input.s3.handler.s3_in_handler import S3InHandler
from server.adapters.input.sqs.dto.conversion_in_dto import ConversionInDTO
from server.adapters.input.sqs.mapper.conversion_in_mapper import ConversionInMapper
from server.adapters.output.s3.handler.s3_out_handler import S3OutHandler
from server.adapters.output.sqs.handler.sqs_out_handler import SQSOutHandler
from server.domain.entity.conversion_entity import ConversionEntity
from server.domain.usecase.abc_conversion_usecase import ABCConversionUseCase
from server.env import Environment
from server.exception_handler import CustomException


class SQSInHandler:
    id: int | None = None

    def __init__(self, env: Environment, conversion_use_case: ABCConversionUseCase):
        self._queue_url = env.AWS_SQS_INPUT_QUEUE
        self._sqs_out_handler = SQSOutHandler(env)
        self._conversion_use_case = conversion_use_case
        self._env = env

    async def receive_messages(self) -> None:
        """
        Receive and process messages from SQS.
        """
        async with adapters.session.client(service_name=AWSServicesEnum.SQS.value) as sqs_client:
            while True:
                response: dict[str, Any] = await sqs_client.receive_message(
                    QueueUrl=self._queue_url,
                    MaxNumberOfMessages=1,  # Receive one message at a time
                    WaitTimeSeconds=5,
                    VisibilityTimeout=30,
                )

                messages: list[dict] = response.get("Messages", [])
                if not messages:
                    logger.info("No messages received. Waiting...")
                    await asyncio.sleep(5)
                    continue

                logger.info(f"Received {len(messages)} messages.")

                # Process current message
                message = messages[0]
                await self._process_message(message)

                # After processing, delete the message
                await self._delete_processed_message(message, sqs_client)

    async def _process_message(self, message: dict) -> None:
        """
        Process a single SQS message.
        """
        logger.info(f"Processing message: {message['MessageId']}")
        conversion_in: ConversionInDTO | None = None
        try:
            body: dict = json.loads(message["Body"])
            logger.debug(f"Message body: {body}")
            conversion_in: ConversionInDTO = ConversionInDTO(**body)
            self.id = conversion_in.id  # Storing the request ID for error notification
            completed_conversion, s3_video_path = await self._convert(conversion_in)

            return await self._sqs_out_handler.send_success_message(completed_conversion, s3_video_path)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode message body: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error while processing message {message['MessageId']}: {e}")
            if conversion_in:
                raise CustomException(id=conversion_in.id, message=e)
            else:
                raise

    async def _convert(self, conversion_in: ConversionInDTO) -> tuple[ConversionEntity, str]:
        conversion_entity: ConversionEntity = ConversionInMapper.convert_to_entity(conversion_in)
        conversion_entity.local_video_path = await S3InHandler(self._env).download_file_from_s3(
            conversion_entity, conversion_in.s3_file_key
        )
        complete_conversion: ConversionEntity = await self._conversion_use_case.create_conversion(conversion_entity)
        s3_video_path: str = await S3OutHandler(self._env).upload_file_to_s3(complete_conversion)
        return complete_conversion, s3_video_path

    async def _delete_processed_message(self, message: dict, sqs_client: client) -> None:
        """
        Delete a single processed message from the SQS queue.
        """
        try:
            await sqs_client.delete_message(QueueUrl=self._queue_url, ReceiptHandle=message["ReceiptHandle"])
            logger.info(f"Deleted message: {message['MessageId']}")
        except Exception as e:
            logger.warning(f"Failed to delete message {message['MessageId']}: {e}")
            raise
