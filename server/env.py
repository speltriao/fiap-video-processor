import os


class Environment:
    AWS_REGION_NAME = os.getenv("AWS_ACCESS_KEY_ID", default="us-east-1")
    AWS_ACCESS_KEY_ID = (os.getenv("AWS_ACCESS_KEY_ID"),)
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN")
    AWS_SQS_INPUT_QUEUE = os.getenv("AWS_SQS_INPUT_QUEUE")
    AWS_SQS_OUTPUT_QUEUE = os.getenv("AWS_SQS_OUTPUT_QUEUE")
