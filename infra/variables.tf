variable "aws_region" {
  description = "AWS region"
  type        = string
}

variable "aws_access_key" {
  description = "AWS aws_access_key"
  type        = string
}

variable "aws_secret_key" {
  description = "AWS aws_secret_key"
  type        = string
}

variable "aws_session_token" {
  description = "AWS aws_session_token"
  type        = string
}

variable "ecr_image_url" {
  description = "URL da imagem no ECR"
  type        = string
}

variable "ecs_task_execution_role_arn" {
  description = "ARN da role de execução do ECS"
  type        = string
}

variable "vpc_id" {
  description = "ID da VPC"
  type        = string
}

variable "public_subnets" {
  description = "Lista de public subnets"
  type        = list(string)
}

variable "private_subnets" {
  description = "Lista de private subnets"
  type        = list(string)
}

variable "security_groups" {
  description = "Lista de security groups"
  type        = list(string)
}

variable "aws_sqs_input_queue" {
  description = "Nome da fila de entrada"
  type        = string
}

variable "aws_sqs_output_queue" {
  description = "Nome da fila de saída"
  type        = string
}

variable "aws_s3_bucket_name" {
  description = "Nome do bucket S3"
  type        = string
}

variable "aws_s3_bucket_output_folder" {
  description = "Nome da pasta do bucket S3"
  type        = string
}

variable "temp_folder" {
  description = "Nome da pasta do bucket S3"
  type        = string
}
