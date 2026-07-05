output "api_endpoint" {
  description = "HTTP API endpoint for the control plane."
  value       = aws_apigatewayv2_api.http.api_endpoint
}

output "artifact_bucket" {
  description = "S3 bucket for source files, manifests, and exports."
  value       = aws_s3_bucket.artifacts.bucket
}

output "artifact_bucket_arn" {
  description = "ARN of the S3 bucket for source files, manifests, and exports."
  value       = aws_s3_bucket.artifacts.arn
}

output "cloudfront_domain_name" {
  description = "CloudFront generated domain for the frontend placeholder."
  value       = local.create_cloudfront_distribution ? aws_cloudfront_distribution.frontend[0].domain_name : null
}

output "cloudfront_distribution_id" {
  description = "CloudFront distribution ID for frontend cache invalidation."
  value       = local.create_cloudfront_distribution ? aws_cloudfront_distribution.frontend[0].id : null
}

output "frontend_bucket" {
  description = "S3 bucket for the static frontend placeholder."
  value       = aws_s3_bucket.frontend.bucket
}

output "jobs_table" {
  description = "DynamoDB table storing job metadata."
  value       = aws_dynamodb_table.jobs.name
}

output "jobs_table_arn" {
  description = "ARN of the DynamoDB table storing job metadata."
  value       = aws_dynamodb_table.jobs.arn
}

output "lambda_function_name" {
  description = "Control-plane Lambda function name."
  value       = aws_lambda_function.api.function_name
}

output "user_pool_id" {
  description = "Cognito user pool ID for invited users."
  value       = aws_cognito_user_pool.users.id
}

output "web_client_id" {
  description = "Cognito user pool client ID for the browser app."
  value       = aws_cognito_user_pool_client.web.id
}

output "hosted_ui_domain" {
  description = "Cognito hosted UI domain for browser sign-in."
  value       = aws_cognito_user_pool_domain.hosted_ui.domain
}

output "hosted_ui_url" {
  description = "Cognito hosted UI base URL for browser sign-in."
  value       = "https://${aws_cognito_user_pool_domain.hosted_ui.domain}.auth.${var.aws_region}.amazoncognito.com"
}

output "frontend_allowed_origins" {
  description = "Browser origins allowed to call the API and artifact upload paths."
  value       = local.frontend_allowed_origins
}

output "name_prefix" {
  description = "Shared infrastructure resource prefix."
  value       = module.foundation.name_prefix
}
