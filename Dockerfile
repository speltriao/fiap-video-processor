# Use the Python 3.12 slim image as the base image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# AWS Secrets #
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_SESSION_TOKEN

# Set environment variables for AWS secrets
ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
ENV AWS_SESSION_TOKEN=$AWS_SESSION_TOKEN

# AWS Configs #
ARG AWS_REGION_NAME
ARG AWS_SQS_INPUT_QUEUE
ARG AWS_SQS_OUTPUT_QUEUE
ARG AWS_S3_BUCKET_NAME
ARG AWS_S3_BUCKET_OUTPUT_FOLDER

# Set environment variables for AWS configs
ENV AWS_REGION_NAME=$AWS_REGION_NAME
ENV AWS_SQS_INPUT_QUEUE=$AWS_SQS_INPUT_QUEUE
ENV AWS_SQS_OUTPUT_QUEUE=$AWS_SQS_OUTPUT_QUEUE
ENV AWS_S3_BUCKET_NAME=$AWS_S3_BUCKET_NAME
ENV AWS_S3_BUCKET_OUTPUT_FOLDER=$AWS_S3_BUCKET_OUTPUT_FOLDER

# Application vars #
ARG TEMP_FOLDER
ENV TEMP_FOLDER=$TEMP_FOLDER


RUN apt update && \
    apt install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "-m", "server"]
