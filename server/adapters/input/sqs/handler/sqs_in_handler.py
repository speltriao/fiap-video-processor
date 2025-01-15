import asyncio
import json

from aiobotocore import client  # For typing only

from server import adapters, logger
from server.adapters.aws_services_enum import AWSServicesEnum
from server.adapters.input.sqs.dto.conversion_in_dto import ConversionInDTO
from server.adapters.input.sqs.mapper.conversion_in_mapper import ConversionInMapper
from server.domain.entity.conversion_entity import ConversionEntity
from server.domain.usecase.abc_conversion_usecase import ABCConversionUseCase
from server.env import Environment


class SQSInHandler:
    def __init__(self, env: Environment):
        self.queue_url = env.AWS_SQS_INPUT_QUEUE

    async def receive_messages(self):
        """
        Receive and process messages from SQS.
        """
        async with adapters.session.client(service_name=AWSServicesEnum.SQS) as sqs_client:
            while True:
                try:
                    response = await sqs_client.receive_message(
                        QueueUrl=self.queue_url,
                        MaxNumberOfMessages=10,  # Batch size (up to 10)
                        WaitTimeSeconds=5,  # Long-polling
                        VisibilityTimeout=30,  # Time before the message becomes visible again
                    )

                    messages = response.get("Messages", [])
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

    async def _process_message(self, message: dict):
        """
        Process a single SQS message.
        """
        logger.info(f"Processing message: {message['MessageId']}")
        try:
            body: dict = json.loads(message["Body"])
            logger.debug(f"Message body: {body}")

            conversion_dto: ConversionInDTO = ConversionInDTO(**body)
            conversion: ConversionEntity = ConversionInMapper.convert_to_entity(conversion_dto)
            await ABCConversionUseCase().create_conversion(conversion)

        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode message body: {e}")
        except Exception as e:
            logger.warning(f"Unexpected error while processing message {message['MessageId']}: {e}")

    async def __delete_processed_messages(self, messages: list[dict], sqs_client: client):
        """
        Delete all processed messages from the sqs.
        """
        for message in messages:
            try:
                await sqs_client.delete_message(QueueUrl=self.queue_url, ReceiptHandle=message["ReceiptHandle"])
                logger.info(f"Deleted message: {message['MessageId']}")
            except Exception as e:
                logger.warning(f"Failed to delete message {message['MessageId']}: {e}")
