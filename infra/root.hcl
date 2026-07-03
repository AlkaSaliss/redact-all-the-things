locals {
  project_name = "redact-all-the-things"

  environment_vars = read_terragrunt_config(find_in_parent_folders("env.hcl"))
  region_vars      = read_terragrunt_config(find_in_parent_folders("region.hcl"))

  environment        = local.environment_vars.locals.environment
  deployment_mode    = lookup(local.environment_vars.locals, "deployment_mode", "aws")
  state_backend      = lookup(local.environment_vars.locals, "state_backend", "s3")
  floci_endpoint_url = lookup(local.environment_vars.locals, "floci_endpoint_url", "")
  aws_region         = local.region_vars.locals.aws_region
  state_region       = local.state_backend == "s3" ? get_env("TG_STATE_REGION", local.aws_region) : local.aws_region
  state_bucket       = local.state_backend == "s3" ? get_env("TG_STATE_BUCKET") : ""
  lock_table         = local.state_backend == "s3" ? get_env("TG_LOCK_TABLE") : ""
  component          = basename(get_terragrunt_dir())

  common_tags = merge(
    lookup(local.environment_vars.locals, "default_tags", {}),
    {
      ManagedBy   = "terragrunt"
      Environment = local.environment
      Region      = local.aws_region
      Component   = local.component
    }
  )
}

generate "backend_s3" {
  path      = "backend.tf"
  if_exists = "overwrite_terragrunt"
  disable   = local.state_backend != "s3"
  contents  = <<EOF
terraform {
  backend "s3" {
    bucket         = "${local.state_bucket}"
    dynamodb_table = "${local.lock_table}"
    encrypt        = true
    key            = "${local.project_name}/${path_relative_to_include()}/terraform.tfstate"
    region         = "${local.state_region}"
  }
}
EOF
}

generate "backend_local" {
  path      = "backend.tf"
  if_exists = "overwrite_terragrunt"
  disable   = local.state_backend == "s3"
  contents  = ""
}

generate "provider_floci" {
  path      = "provider.tf"
  if_exists = "overwrite_terragrunt"
  disable   = local.deployment_mode != "floci"
  contents  = <<EOF
provider "aws" {
  region                      = "${local.aws_region}"
  access_key                  = "test"
  secret_key                  = "test"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true
  s3_use_path_style           = true

  endpoints {
    apigateway   = "${local.floci_endpoint_url}"
    apigatewayv2 = "${local.floci_endpoint_url}"
    batch        = "${local.floci_endpoint_url}"
    budgets      = "${local.floci_endpoint_url}"
    cloudfront   = "${local.floci_endpoint_url}"
    cognitoidp   = "${local.floci_endpoint_url}"
    dynamodb     = "${local.floci_endpoint_url}"
    ec2          = "${local.floci_endpoint_url}"
    ecs          = "${local.floci_endpoint_url}"
    ecr          = "${local.floci_endpoint_url}"
    iam          = "${local.floci_endpoint_url}"
    lambda       = "${local.floci_endpoint_url}"
    logs         = "${local.floci_endpoint_url}"
    s3           = "${local.floci_endpoint_url}"
    sts          = "${local.floci_endpoint_url}"
  }

  default_tags {
    tags = ${jsonencode(local.common_tags)}
  }
}
EOF
}

generate "provider_aws" {
  path      = "provider.tf"
  if_exists = "overwrite_terragrunt"
  disable   = local.deployment_mode == "floci"
  contents  = <<EOF
provider "aws" {
  region = "${local.aws_region}"

  default_tags {
    tags = ${jsonencode(local.common_tags)}
  }
}
EOF
}

# Configure retry and error handling
retry_max_attempts       = 3
retry_sleep_interval_sec = 5

# Terragrunt will copy the Terraform configurations specified by the source parameter
terraform {
  extra_arguments "common_vars" {
    commands = get_terraform_commands_that_need_vars()

    optional_var_files = [
      find_in_parent_folders("account.tfvars", "ignore"),
      find_in_parent_folders("region.tfvars", "ignore"),
      find_in_parent_folders("env.tfvars", "ignore")
    ]
  }

  extra_arguments "disable_input" {
    commands  = get_terraform_commands_that_need_input()
    arguments = ["-input=false"]
  }

  extra_arguments "parallelism" {
    commands  = ["apply", "plan", "destroy"]
    arguments = ["-parallelism=10"]
  }
}

inputs = {
  aws_region         = local.aws_region
  deployment_mode    = local.deployment_mode
  environment        = local.environment
  floci_endpoint_url = local.floci_endpoint_url
  project_name       = local.project_name
}
