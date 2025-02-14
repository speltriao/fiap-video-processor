provider "aws" {
  region = var.aws_region
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
  token = var.aws_session_token
}

resource "aws_ecs_cluster" "frameshot_cluster" {
  name = "frameshot-cluster"
}

resource "aws_ecs_task_definition" "frameshot-app-task" {
  family                   = "frameshot-app-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "1024"
  memory                   = "2048"
  execution_role_arn       = var.ecs_task_execution_role_arn
  task_role_arn            = var.ecs_task_execution_role_arn

  container_definitions = jsonencode([
    {
      name      = "frameshot-app"
      image     = var.ecr_image_url
      essential = true
      environment = [
        { name = "HTTP_ALLOWED_ORIGINS", value = "*" },
        { name = "AWS_REGION_NAME", value = var.aws_region },
        { name = "AWS_ACCESS_KEY_ID", value = var.aws_access_key },
        { name = "AWS_SECRET_ACCESS_KEY", value = var.aws_secret_key },
        { name = "AWS_SESSION_TOKEN", value = var.aws_session_token },
        { name = "AWS_SQS_INPUT_QUEUE", value = var.aws_sqs_input_queue },
        { name = "AWS_SQS_OUTPUT_QUEUE", value = var.aws_sqs_output_queue },
        { name = "AWS_S3_BUCKET_NAME", value = var.aws_s3_bucket_name },
        { name = "AWS_S3_BUCKET_OUTPUT_FOLDER", value = var.aws_s3_bucket_output_folder },
        { name = "TEMP_FOLDER", value = var.temp_folder }
      ]
      portMappings = [
        {
          containerPort = 6666
          hostPort      = 6666
          protocol      = "tcp"
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = "/ecs/frameshot-app"
          awslogs-region        = var.aws_region
          awslogs-stream-prefix = "ecs"
        }
      }
    }
  ])
}

resource "aws_ecs_service" "frameshot_service" {
  name            = "frameshot-app"
  cluster         = aws_ecs_cluster.frameshot_cluster.id
  task_definition = aws_ecs_task_definition.frameshot-app-task.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets         = var.private_subnets
    security_groups = var.security_groups
    assign_public_ip = true
  }
}