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
  nullable    = false
}

variable "project_name" {
  description = "Project name used for resource naming."
  type        = string
  default     = "redact-all-the-things"
}
