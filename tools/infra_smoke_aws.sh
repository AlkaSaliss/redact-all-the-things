#!/usr/bin/env bash
set -euo pipefail

if ! command -v terragrunt >/dev/null 2>&1; then
  echo "terragrunt is required for AWS infrastructure smoke checks." >&2
  exit 1
fi

if ! command -v aws >/dev/null 2>&1; then
  echo "aws CLI is required for AWS infrastructure smoke checks." >&2
  exit 1
fi

if ! command -v jq >/dev/null 2>&1; then
  echo "jq is required for AWS infrastructure smoke checks." >&2
  exit 1
fi

required_env=(
  TG_STATE_BUCKET
  TG_LOCK_TABLE
)

missing=()
for name in "${required_env[@]}"; do
  if [[ -z "${!name:-}" ]]; then
    missing+=("$name")
  fi
done

if (( ${#missing[@]} > 0 )); then
  printf 'Missing required AWS smoke configuration: %s\n' "${missing[*]}" >&2
  exit 1
fi

aws_region="${AWS_REGION:-eu-west-1}"
aws_environment="${AWS_LIVE_ENVIRONMENT:-dev}"
live_stack="infra/live/${aws_environment}/${aws_region}/worker-compute-artifacts"

aws sts get-caller-identity >/dev/null

pushd "$live_stack" >/dev/null
outputs="$(terragrunt output -json)"
popd >/dev/null

required_outputs=(
  api_endpoint
  artifact_bucket
  frontend_bucket
  jobs_table_name
  worker_repository_url
  worker_job_queue_name
)

missing_outputs=()
for name in "${required_outputs[@]}"; do
  if ! printf '%s' "$outputs" | jq -e --arg name "$name" '.[$name].value != null and .[$name].value != ""' >/dev/null; then
    missing_outputs+=("$name")
  fi
done

if (( ${#missing_outputs[@]} > 0 )); then
  printf 'Missing required Terragrunt outputs: %s\n' "${missing_outputs[*]}" >&2
  exit 1
fi

jobs_table="$(printf '%s' "$outputs" | jq -r '.jobs_table_name.value')"
artifact_bucket="$(printf '%s' "$outputs" | jq -r '.artifact_bucket.value')"
frontend_bucket="$(printf '%s' "$outputs" | jq -r '.frontend_bucket.value')"
worker_queue="$(printf '%s' "$outputs" | jq -r '.worker_job_queue_name.value')"
worker_repository_url="$(printf '%s' "$outputs" | jq -r '.worker_repository_url.value')"
worker_repository="${worker_repository_url#*.amazonaws.com/}"

aws dynamodb describe-table --table-name "$jobs_table" --region "$aws_region" >/dev/null
aws s3api get-bucket-encryption --bucket "$artifact_bucket" --region "$aws_region" >/dev/null
aws s3api get-public-access-block --bucket "$artifact_bucket" --region "$aws_region" >/dev/null
aws s3api get-bucket-encryption --bucket "$frontend_bucket" --region "$aws_region" >/dev/null
aws s3api get-public-access-block --bucket "$frontend_bucket" --region "$aws_region" >/dev/null
aws batch describe-job-queues --job-queues "$worker_queue" --region "$aws_region" >/dev/null
aws ecr describe-repositories --repository-names "$worker_repository" --region "$aws_region" >/dev/null

cat <<EOF
AWS infrastructure smoke check passed in ${aws_region}.

Verified deployed DynamoDB, S3 encryption/public-access blocks, AWS Batch job
queue, and ECR repository outputs from the real AWS live stack.
EOF
