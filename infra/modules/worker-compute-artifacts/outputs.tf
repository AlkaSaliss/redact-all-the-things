output "analyze_job_definition" {
  description = "AWS Batch job definition for analysis workers."
  value       = aws_batch_job_definition.analyze.name
}

output "render_job_definition" {
  description = "AWS Batch job definition for render workers."
  value       = aws_batch_job_definition.render.name
}

output "worker_image_repository" {
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
