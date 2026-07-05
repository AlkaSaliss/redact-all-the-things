variable "aws_region" {
  description = "AWS region to model for the infrastructure stack."
  type        = string
  default     = "eu-west-1"
}

variable "environment" {
  description = "Deployment environment name."
  type        = string
  default     = "floci"
}

variable "floci_endpoint_url" {
  description = "AWS-compatible endpoint exposed by the local Floci emulator."
  type        = string
  default     = null
  nullable    = true
}

variable "deployment_mode" {
  description = "Infrastructure deployment mode: floci for emulator-compatible local resources or aws for the full AWS graph."
  type        = string
  default     = "aws"

  validation {
    condition     = contains(["floci", "aws"], var.deployment_mode)
    error_message = "deployment_mode must be either floci or aws."
  }
}

variable "project_name" {
  description = "Project name used for resource naming."
  type        = string
  default     = "redact-all-the-things"
}

variable "lambda_package_path" {
  description = "Path to the built control-plane Lambda ZIP package."
  type        = string
  default     = null
  nullable    = true
}

variable "worker_image_tag" {
  description = "Immutable ECR image tag used by worker Batch job definitions."
  type        = string
  default     = "latest"
}
