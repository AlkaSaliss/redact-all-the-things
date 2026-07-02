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
    condition     = can(regex("^[a-z0-9-]+$", var.environment))
    error_message = "Environment must use lowercase letters, numbers, and hyphens."
  }
}

variable "floci_endpoint_url" {
  description = "AWS-compatible endpoint exposed by the local Floci emulator."
  type        = string
  default     = null
  nullable    = true

  validation {
    condition = (
      var.deployment_mode != "floci" ||
      (
        var.floci_endpoint_url != null &&
        (startswith(var.floci_endpoint_url, "http://") || startswith(var.floci_endpoint_url, "https://"))
      )
    )
    error_message = "FLOCI_ENDPOINT_URL must be an http:// or https:// URL when deployment_mode is floci."
  }
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

  validation {
    condition     = var.project_name == "redact-all-the-things"
    error_message = "Project name is fixed for this repository."
  }
}
