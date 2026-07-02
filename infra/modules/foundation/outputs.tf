output "aws_region" {
  description = "AWS region used for the Floci infrastructure phase."
  value       = var.aws_region
}

output "environment" {
  description = "Infrastructure environment name."
  value       = var.environment
}

output "floci_endpoint_url" {
  description = "AWS-compatible Floci endpoint targeted by Terragrunt."
  value       = var.floci_endpoint_url
}

output "name_prefix" {
  description = "Shared prefix for later AWS resources."
  value       = local.name_prefix
}
