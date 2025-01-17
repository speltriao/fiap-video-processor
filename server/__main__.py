import asyncio

from server import env
from server.adapters.input.sqs.handler.sqs_in_handler import SQSInHandler
from server.domain.service.conversion_service import ConversionService


async def main():
    sqs_input_handler = SQSInHandler(env.Environment(), ConversionService())
    await sqs_input_handler.receive_messages()


if __name__ == "__main__":
    asyncio.run(main())
