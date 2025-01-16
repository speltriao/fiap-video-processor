import os


class Environment:
    AWS_REGION_NAME = os.getenv("AWS_REGION_NAME", default="us-east-1")
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN")
    AWS_SQS_INPUT_QUEUE = os.getenv("AWS_SQS_INPUT_QUEUE", default="VideoProcessInput")
    AWS_SQS_OUTPUT_QUEUE = os.getenv("AWS_SQS_OUTPUT_QUEUE", default="VideoProcessOutput")
    AWS_S3_BUCKET_NAME = os.getenv("AWS_S3_BUCKET_NAME", default="frameshot")
    AWS_S3_BUCKET_OUTPUT_FOLDER = os.getenv("AWS_S3_BUCKET_OUTPUT_FOLDER", default="output_zip/")
    TEMP_FOLDER = os.getenv("TEMP_FOLDER", default="C:/Users/Public/Downloads")
