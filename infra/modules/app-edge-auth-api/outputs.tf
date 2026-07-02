output "api_endpoint" {
  description = "HTTP API endpoint for the control-plane stub."
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
  description = "Control-plane Lambda stub function name."
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

output "name_prefix" {
  description = "Shared infrastructure resource prefix."
  value       = module.foundation.name_prefix
}
