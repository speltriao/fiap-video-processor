import asyncio

from server import env
from server.adapters.input.sqs.handler.sqs_in_handler import SQSInHandler


def main():
    sqs_input_handler = SQSInHandler(env)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(sqs_input_handler.receive_messages())


if __name__ == "__main__":
    main()
