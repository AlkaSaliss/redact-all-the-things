locals {
  aws_region   = get_env("AWS_REGION", "eu-west-1")
  environment  = get_env("AWS_ENVIRONMENT", "prod")
  state_region = get_env("TG_STATE_REGION", local.aws_region)
}

terraform {
  source = "../../modules//worker-compute-artifacts"
}

remote_state {
  backend = "s3"
  config = {
    bucket         = get_env("TG_STATE_BUCKET")
    dynamodb_table = get_env("TG_LOCK_TABLE")
    encrypt        = true
    key            = "redact-all-the-things/${local.environment}/terraform.tfstate"
    region         = local.state_region
  }
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
