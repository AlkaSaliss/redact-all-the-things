locals {
  aws_region  = get_env("AWS_REGION", "eu-west-1")
  environment = get_env("AWS_ENVIRONMENT", "prod")
}

terraform {
  source = "../../modules//worker-compute-artifacts"
}

generate "provider" {
  path      = "provider.tf"
  if_exists = "overwrite_terragrunt"
  contents  = <<EOF
provider "aws" {
  region = "${local.aws_region}"
}
EOF
}

inputs = {
  aws_region      = local.aws_region
  deployment_mode = "aws"
  environment     = local.environment
  project_name    = "redact-all-the-things"
}
