output "analyze_job_definition" {
  description = "AWS Batch job definition for analysis workers."
  value       = aws_batch_job_definition.analyze.name
}

output "api_endpoint" {
  description = "HTTP API endpoint for the control-plane stub."
  value       = module.app.api_endpoint
}

output "artifact_bucket" {
  description = "S3 bucket for source files, manifests, and exports."
  value       = module.app.artifact_bucket
}

output "frontend_bucket" {
  description = "S3 bucket for the static frontend placeholder."
  value       = module.app.frontend_bucket
}

output "cloudfront_domain_name" {
  description = "CloudFront generated domain for the frontend app."
  value       = module.app.cloudfront_domain_name
}

output "cloudfront_distribution_id" {
  description = "CloudFront distribution ID for frontend cache invalidation."
  value       = module.app.cloudfront_distribution_id
}

output "frontend_allowed_origins" {
  description = "Browser origins allowed to call API and artifact paths."
  value       = module.app.frontend_allowed_origins
}

output "hosted_ui_url" {
  description = "Cognito hosted UI base URL for browser sign-in."
  value       = module.app.hosted_ui_url
}

output "jobs_table_name" {
  description = "DynamoDB table storing job metadata."
  value       = module.app.jobs_table
}

output "lambda_function_name" {
  description = "Control-plane Lambda function name."
  value       = module.app.lambda_function_name
}

output "render_job_definition" {
  description = "AWS Batch job definition for render workers."
  value       = aws_batch_job_definition.render.name
}

output "user_pool_id" {
  description = "Cognito user pool ID for invited users."
  value       = module.app.user_pool_id
}

output "web_client_id" {
  description = "Cognito user pool client ID for the browser app."
  value       = module.app.web_client_id
}

output "worker_image_repository" {
  description = "ECR repository URL for the worker image."
  value       = aws_ecr_repository.worker.repository_url
}

output "worker_job_queue_name" {
  description = "AWS Batch worker job queue name."
  value       = aws_batch_job_queue.worker.name
}

output "worker_repository_url" {
  description = "ECR repository URL for the worker image."
  value       = aws_ecr_repository.worker.repository_url
}

output "worker_job_queue" {
  description = "AWS Batch worker job queue name."
  value       = aws_batch_job_queue.worker.name
}

output "worker_log_group" {
  description = "CloudWatch log group for worker jobs."
  value       = aws_cloudwatch_log_group.worker.name
}
