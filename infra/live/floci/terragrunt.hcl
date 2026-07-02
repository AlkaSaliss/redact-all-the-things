locals {
  aws_access_key     = get_env("AWS_ACCESS_KEY_ID", "floci")
  aws_region         = get_env("AWS_REGION", "eu-west-1")
  aws_secret_key     = get_env("AWS_SECRET_ACCESS_KEY", "floci")
  floci_endpoint_url = get_env("FLOCI_ENDPOINT_URL", "")
}

terraform {
  source = "../../modules//app-edge-auth-api"
}

generate "provider" {
  path      = "provider.tf"
  if_exists = "overwrite_terragrunt"
  contents  = <<EOF
provider "aws" {
  region                      = "${local.aws_region}"
  access_key                  = "${local.aws_access_key}"
  secret_key                  = "${local.aws_secret_key}"
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
    ecr          = "${local.floci_endpoint_url}"
    iam          = "${local.floci_endpoint_url}"
    lambda       = "${local.floci_endpoint_url}"
    logs         = "${local.floci_endpoint_url}"
    s3           = "${local.floci_endpoint_url}"
    sts          = "${local.floci_endpoint_url}"
  }
}
EOF
}

inputs = {
  aws_region         = local.aws_region
  environment        = "floci"
  floci_endpoint_url = local.floci_endpoint_url
  project_name       = "redact-all-the-things"
}
