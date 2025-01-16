import asyncio

from server import env
from server.adapters.input.sqs.handler.sqs_in_handler import SQSInHandler
from server.domain.service.conversion_service import ConversionService


def main():
    sqs_input_handler = SQSInHandler(env.Environment(), ConversionService())

    loop = asyncio.get_event_loop()
    loop.run_until_complete(sqs_input_handler.receive_messages())


if __name__ == "__main__":
    main()
