from server import adapters, logger
from server.adapters.aws_services_enum import AWSServicesEnum
from server.adapters.output.sqs.dto.conversion_out_dto import ConversionOutDTO
from server.env import Environment


class SQSOutHandler:
    def __init__(self, env: Environment):
        self.queue_url = env.AWS_SQS_OUTPUT_QUEUE

    async def send_message(self, message_body: ConversionOutDTO):
        """
        Send message to SQS Queue.
        """
        try:
            logger.info(f"Preparing to send message to SQS. Queue URL: {self.queue_url}")
            async with adapters.session.client(service_name=AWSServicesEnum.SQS) as sqs_client:
                response = await sqs_client.send_message(
                    QueueUrl=self.queue_url, MessageBody=message_body.json()  # Ensure `message_body` is serialized
                )
                logger.info(f"Message sent successfully to SQS. Message ID: {response.get('MessageId')}")
                return response
        except Exception as e:
            logger.error(f"Failed to send message to SQS. Error: {e}")
            raise
