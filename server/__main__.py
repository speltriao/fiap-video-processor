import asyncio

from server import env, logger
from server.adapters.input.sqs.handler.sqs_in_handler import SQSInHandler
from server.domain.service.conversion_service import ConversionService


async def main() -> None:
    sqs_input_handler: SQSInHandler = SQSInHandler(env.Environment(), ConversionService())
    await sqs_input_handler.receive_messages()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Application interrupted by user.")
