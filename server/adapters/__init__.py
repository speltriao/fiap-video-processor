import aioboto3

from server.adapters.output.sqs.handler.sqs_out_handler import SQSOutHandler
from server.env import Environment

session = aioboto3.session.Session(
    aws_access_key_id=Environment.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=Environment.AWS_SECRET_ACCESS_KEY,
    aws_session_token=Environment.AWS_SESSION_TOKEN,
    region_name=Environment.AWS_REGION_NAME,
)
