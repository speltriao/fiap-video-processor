from server import adapters, logger
from server.adapters.aws_services_enum import AWSServicesEnum
from server.adapters.output.sqs.mapper.conversion_out_mapper import ConversionOutMapper
from server.domain.entity.conversion_entity import ConversionEntity
from server.env import Environment


class SQSOutHandler:
    def __init__(self, env: Environment):
        self.queue_url = env.AWS_SQS_OUTPUT_QUEUE

    async def send_message(self, completed_conversion: ConversionEntity) -> bool:
        """
        Send message to SQS Queue.
        """
        try:
            logger.info(f"Preparing to send message to SQS. Queue URL: {self.queue_url}")
            message_body = ConversionOutMapper.convert_from_entity(completed_conversion)
            async with adapters.session.client(service_name=AWSServicesEnum.SQS.value) as sqs_client:
                response = await sqs_client.send_message(QueueUrl=self.queue_url, MessageBody=message_body.json())
                logger.info(f"Message sent successfully to SQS. Message ID: {response.get('MessageId')}")
                return True
        except Exception as e:
            logger.error(f"Failed to send message to SQS. Error: {e}")
            return False
