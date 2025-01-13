import asyncio
import json

import aioboto3
from aiobotocore import client

from tools.logging import logger


class SQSInHandler:
    def __init__(
        self,
        queue_url: str,
        aws_access_key_id: str,
        aws_secret_access_key: str,
        aws_session_token: str,
        region_name="us-east-1",
    ):
        self.queue_url = queue_url
        self.region_name = region_name
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.aws_session_token = aws_session_token

    async def receive_messages(self):
        """
        Receive and process messages from SQS.
        """
        session = aioboto3.session.Session(
            aws_access_key_id="your_access_key",
            aws_secret_access_key="your_secret_access_key",
            aws_session_token="your_session_token",
        )
        async with session.client(service_name="sqs", region_name=self.region_name) as sqs_client:
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
                        await asyncio.sleep(5)  # Backoff
                        continue

                    logger.info(f"Received {len(messages)} messages.")

                    # Process messages concurrently
                    tasks = [self.process_message(message) for message in messages]
                    await asyncio.gather(*tasks)
                    await self.__delete_processed_messages(messages, sqs_client)

                except Exception as e:
                    logger.error(f"Error while receiving messages: {e}")
                    await asyncio.sleep(5)  # Backoff in case of failure

    async def __delete_processed_messages(self, messages: list[dict], sqs_client: client):
        for message in messages:
            try:
                await sqs_client.delete_message(QueueUrl=self.queue_url, ReceiptHandle=message["ReceiptHandle"])
                logger.info(f"Deleted message: {message['MessageId']}")
            except Exception as e:
                logger.warning(f"Failed to delete message {message['MessageId']}: {e}")

    async def process_message(self, message: dict):
        """
        Process a single SQS message.
        """
        logger.info(f"Processing message: {message['MessageId']}")
        try:
            body = json.loads(message["Body"])
            logger.debug(f"Message body: {body}")  # Log the message body for debugging
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode message body: {e}")
        except Exception as e:
            logger.warning(f"Unexpected error while processing message {message['MessageId']}: {e}")
