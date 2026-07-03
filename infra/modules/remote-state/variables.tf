variable "aws_region" {
  description = "AWS region for the remote-state resources."
  type        = string
  default     = "eu-west-1"

  validation {
    condition     = var.aws_region == "eu-west-1"
    error_message = "The initial infrastructure target must remain eu-west-1."
  }
}

variable "environment" {
  description = "Deployment environment name used for resource naming."
  type        = string
  default     = "prod"

  validation {
    condition     = can(regex("^[a-z0-9-]+$", var.environment))
    error_message = "Environment must use lowercase letters, numbers, and hyphens."
  }
}

variable "project_name" {
  description = "Project name used for resource naming."
  type        = string
  default     = "redact-all-the-things"

  validation {
    condition     = var.project_name == "redact-all-the-things"
    error_message = "Project name is fixed for this repository."
  }
}
