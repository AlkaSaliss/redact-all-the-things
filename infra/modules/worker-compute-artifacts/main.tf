module "app" {
  source = "../app-edge-auth-api"

  aws_region         = var.aws_region
  deployment_mode    = var.deployment_mode
  environment        = var.environment
  floci_endpoint_url = var.floci_endpoint_url
  project_name       = var.project_name
}

locals {
  use_floci_compatibility = var.deployment_mode == "floci"
  name_prefix             = module.app.name_prefix
  worker_image            = "${aws_ecr_repository.worker.repository_url}:stub"
}

resource "aws_ecr_repository" "worker" {
  name                 = "${local.name_prefix}-worker"
  image_tag_mutability = "IMMUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  encryption_configuration {
    encryption_type = "AES256"
  }
}

resource "aws_cloudwatch_log_group" "worker" {
  name              = "/aws/batch/${local.name_prefix}-worker"
  retention_in_days = 7
}

resource "aws_vpc" "worker" {
  cidr_block           = "10.42.0.0/24"
  enable_dns_hostnames = true
  enable_dns_support   = true
}

resource "aws_subnet" "worker_a" {
  vpc_id                  = aws_vpc.worker.id
  cidr_block              = "10.42.0.0/25"
  availability_zone       = "${var.aws_region}a"
  map_public_ip_on_launch = false
}

resource "aws_subnet" "worker_b" {
  vpc_id                  = aws_vpc.worker.id
  cidr_block              = "10.42.0.128/25"
  availability_zone       = "${var.aws_region}b"
  map_public_ip_on_launch = false
}

resource "aws_security_group" "worker" {
  name        = "${local.name_prefix}-worker"
  description = "Worker tasks have no inbound access."
  vpc_id      = aws_vpc.worker.id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_iam_role" "batch_service" {
  name = "${local.name_prefix}-batch-service"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "batch.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      },
    ]
  })
}

resource "aws_iam_role_policy" "batch_service" {
  count = local.use_floci_compatibility ? 1 : 0

  name = "${local.name_prefix}-batch-service"
  role = aws_iam_role.batch_service.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "batch:*",
          "ec2:*",
          "ecs:*",
          "iam:PassRole",
          "logs:*",
        ]
        Resource = "*"
      },
    ]
  })
}

resource "aws_iam_role_policy_attachment" "batch_service" {
  count = local.use_floci_compatibility ? 0 : 1

  role       = aws_iam_role.batch_service.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSBatchServiceRole"
}

resource "aws_iam_role" "task_execution" {
  name = "${local.name_prefix}-worker-execution"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      },
    ]
  })
}

resource "aws_iam_role_policy" "task_execution" {
  name = "${local.name_prefix}-worker-execution"
  role = aws_iam_role.task_execution.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ecr:BatchCheckLayerAvailability",
          "ecr:BatchGetImage",
          "ecr:GetDownloadUrlForLayer",
        ]
        Resource = aws_ecr_repository.worker.arn
      },
      {
        Effect   = "Allow"
        Action   = "ecr:GetAuthorizationToken"
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogStream",
          "logs:PutLogEvents",
        ]
        Resource = "${aws_cloudwatch_log_group.worker.arn}:*"
      },
    ]
  })
}

resource "aws_iam_role" "worker_job" {
  name = "${local.name_prefix}-worker-job"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      },
    ]
  })
}

resource "aws_iam_role_policy" "worker_job" {
  name = "${local.name_prefix}-worker-job"
  role = aws_iam_role.worker_job.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:UpdateItem",
        ]
        Resource = module.app.jobs_table_arn
      },
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:ListBucket",
          "s3:PutObject",
        ]
        Resource = [
          module.app.artifact_bucket_arn,
          "${module.app.artifact_bucket_arn}/*",
        ]
      },
    ]
  })
}

resource "aws_batch_compute_environment" "worker" {
  name         = "${local.name_prefix}-worker"
  service_role = aws_iam_role.batch_service.arn
  type         = "MANAGED"

  compute_resources {
    max_vcpus          = 2
    security_group_ids = [aws_security_group.worker.id]
    subnets            = [aws_subnet.worker_a.id, aws_subnet.worker_b.id]
    type               = "FARGATE_SPOT"
  }

  depends_on = [
    aws_iam_role_policy.batch_service,
    aws_iam_role_policy_attachment.batch_service,
  ]
}

resource "aws_batch_job_queue" "worker" {
  name     = "${local.name_prefix}-worker"
  priority = 1
  state    = "ENABLED"

  compute_environment_order {
    compute_environment = aws_batch_compute_environment.worker.arn
    order               = 1
  }
}

resource "aws_batch_job_definition" "analyze" {
  name                  = "${local.name_prefix}-analyze"
  type                  = "container"
  platform_capabilities = ["FARGATE"]

  container_properties = jsonencode({
    command = [
      "python",
      "/app/worker_stub.py",
      "analyze",
    ]
    environment = [
      {
        name  = "FILES_BUCKET"
        value = module.app.artifact_bucket
      },
      {
        name  = "JOBS_TABLE"
        value = module.app.jobs_table
      },
    ]
    executionRoleArn       = aws_iam_role.task_execution.arn
    image                  = local.worker_image
    jobRoleArn             = aws_iam_role.worker_job.arn
    readonlyRootFilesystem = true
    logConfiguration = {
      logDriver = "awslogs"
      options = {
        "awslogs-group"         = aws_cloudwatch_log_group.worker.name
        "awslogs-region"        = var.aws_region
        "awslogs-stream-prefix" = "analyze"
      }
    }
    networkConfiguration = {
      assignPublicIp = "DISABLED"
    }
    resourceRequirements = [
      {
        type  = "VCPU"
        value = "2"
      },
      {
        type  = "MEMORY"
        value = "8192"
      },
    ]
  })
}

resource "aws_batch_job_definition" "render" {
  name                  = "${local.name_prefix}-render"
  type                  = "container"
  platform_capabilities = ["FARGATE"]

  container_properties = jsonencode({
    command = [
      "python",
      "/app/worker_stub.py",
      "render",
    ]
    environment = [
      {
        name  = "FILES_BUCKET"
        value = module.app.artifact_bucket
      },
      {
        name  = "JOBS_TABLE"
        value = module.app.jobs_table
      },
    ]
    executionRoleArn       = aws_iam_role.task_execution.arn
    image                  = local.worker_image
    jobRoleArn             = aws_iam_role.worker_job.arn
    readonlyRootFilesystem = true
    logConfiguration = {
      logDriver = "awslogs"
      options = {
        "awslogs-group"         = aws_cloudwatch_log_group.worker.name
        "awslogs-region"        = var.aws_region
        "awslogs-stream-prefix" = "render"
      }
    }
    networkConfiguration = {
      assignPublicIp = "DISABLED"
    }
    resourceRequirements = [
      {
        type  = "VCPU"
        value = "2"
      },
      {
        type  = "MEMORY"
        value = "8192"
      },
    ]
  })
}
