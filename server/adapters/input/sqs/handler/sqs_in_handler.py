import asyncio
import json
from typing import Any, Coroutine

from aiobotocore import client  # For typing only

from server import adapters, logger
from server.adapters.aws_services_enum import AWSServicesEnum
from server.adapters.input.s3.handler.s3_in_handler import S3InHandler
from server.adapters.input.sqs.dto.conversion_in_dto import ConversionInDTO
from server.adapters.input.sqs.mapper.conversion_in_mapper import ConversionInMapper
from server.adapters.output.s3.handler.s3_out_handler import S3OutHandler
from server.adapters.output.sqs.dto.conversion_out_dto import ConversionOutDTO
from server.adapters.output.sqs.handler.sqs_out_handler import SQSOutHandler
from server.adapters.output.sqs.mapper.conversion_out_mapper import ConversionOutMapper
from server.domain.entity.conversion_entity import ConversionEntity
from server.domain.usecase.abc_conversion_usecase import ABCConversionUseCase
from server.env import Environment


class SQSInHandler:
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
                try:
                    response: dict[str, Any] = await sqs_client.receive_message(
                        QueueUrl=self._queue_url,
                        MaxNumberOfMessages=10,
                        WaitTimeSeconds=5,
                        VisibilityTimeout=30,
                    )

                    messages: list[dict] = response.get("Messages", [])
                    if not messages:
                        logger.info("No messages received. Waiting...")
                        await asyncio.sleep(5)
                        continue

                    logger.info(f"Received {len(messages)} messages.")

                    # Process messages concurrently
                    tasks = [self._process_message(message) for message in messages]
                    await asyncio.gather(*tasks)
                    await self.__delete_processed_messages(messages, sqs_client)

                except Exception as e:
                    logger.error(f"Error while receiving messages: {e}")
                    await asyncio.sleep(5)

    async def _process_message(self, message: dict) -> None:
        """
        Process a single SQS message.
        """
        logger.info(f"Processing message: {message['MessageId']}")
        try:
            body: dict = json.loads(message["Body"])
            logger.debug(f"Message body: {body}")
            conversion_in: ConversionInDTO = ConversionInDTO(**body)
            completed_conversion, s3_video_path = await self._convert(conversion_in)
            return await self._sqs_out_handler.send_message(completed_conversion, s3_video_path)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode message body: {e}")
        except Exception as e:
            logger.error(f"Unexpected error while processing message {message['MessageId']}: {e}")

    async def _convert(self, conversion_in: ConversionInDTO) -> tuple[ConversionEntity, str]:
        conversion_entity: ConversionEntity = ConversionInMapper.convert_to_entity(conversion_in)
        conversion_entity.local_video_path = await S3InHandler(self._env).download_file_from_s3(
            conversion_entity, conversion_in.s3_file_key
        )
        complete_conversion: ConversionEntity = await self._conversion_use_case.create_conversion(conversion_entity)
        s3_video_path: str = await S3OutHandler(self._env).upload_file_to_s3(complete_conversion)
        return complete_conversion, s3_video_path

    async def __delete_processed_messages(self, messages: list[dict], sqs_client: client) -> None:
        """
        Delete all processed messages from the sqs.
        """
        for message in messages:
            try:
                await sqs_client.delete_message(QueueUrl=self._queue_url, ReceiptHandle=message["ReceiptHandle"])
                logger.info(f"Deleted message: {message['MessageId']}")
            except Exception as e:
                logger.warning(f"Failed to delete message {message['MessageId']}: {e}")
