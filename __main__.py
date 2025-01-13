import asyncio
import os

from server.adapters.input.sqs_in_handler import SQSInHandler


def main():
    sqs_input_handler = SQSInHandler(
        queue_url=os.getenv("queue_url"),
        region_name="us-east-1",
        aws_session_token=os.getenv("aws_session_token"),
        aws_access_key_id=os.getenv("aws_access_key_id"),
        aws_secret_access_key=os.getenv("aws_secret_access_key"),
    )

    loop = asyncio.get_event_loop()
    loop.run_until_complete(sqs_input_handler.receive_messages())


if __name__ == "__main__":
    main()
