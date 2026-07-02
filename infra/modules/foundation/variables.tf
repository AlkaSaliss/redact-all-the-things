variable "aws_region" {
  description = "AWS region to model for the infrastructure stack."
  type        = string
  default     = "eu-west-1"

  validation {
    condition     = var.aws_region == "eu-west-1"
    error_message = "The initial infrastructure target must remain eu-west-1."
  }
}

variable "environment" {
  description = "Deployment environment name."
  type        = string
  default     = "floci"

  validation {
    condition     = var.environment == "floci"
    error_message = "This foundation slice only supports the floci environment."
  }
}

variable "floci_endpoint_url" {
  description = "AWS-compatible endpoint exposed by the local Floci emulator."
  type        = string
  nullable    = false

  validation {
    condition     = startswith(var.floci_endpoint_url, "http://") || startswith(var.floci_endpoint_url, "https://")
    error_message = "FLOCI_ENDPOINT_URL must be an http:// or https:// URL."
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
