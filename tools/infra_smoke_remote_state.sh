#!/usr/bin/env bash
set -euo pipefail

if ! command -v terragrunt >/dev/null 2>&1; then
  echo "terragrunt is required for remote-state smoke checks." >&2
  exit 1
fi

if ! command -v aws >/dev/null 2>&1; then
  echo "aws CLI is required for remote-state smoke checks." >&2
  exit 1
fi

if ! command -v jq >/dev/null 2>&1; then
  echo "jq is required for remote-state smoke checks." >&2
  exit 1
fi

aws_region="${AWS_REGION:-eu-west-1}"

aws sts get-caller-identity >/dev/null

pushd infra/live/remote-state >/dev/null
outputs="$(terragrunt output -json)"
popd >/dev/null

state_bucket="$(printf '%s' "$outputs" | jq -r '.state_bucket.value')"
lock_table="$(printf '%s' "$outputs" | jq -r '.lock_table.value')"

echo "State bucket: $state_bucket"
echo "Lock table: $lock_table"

aws s3api get-bucket-encryption --bucket "$state_bucket" --region "$aws_region" >/dev/null
aws s3api get-public-access-block --bucket "$state_bucket" --region "$aws_region" >/dev/null
aws s3api get-bucket-versioning --bucket "$state_bucket" --region "$aws_region" \
  | jq -e '.Status == "Enabled"' >/dev/null
aws dynamodb describe-table --table-name "$lock_table" --region "$aws_region" \
  | jq -e '.Table.SSEDescription.Status == "ENABLED"' >/dev/null

cat <<EOF
Remote-state smoke check passed in ${aws_region}.

Verified S3 state bucket encryption, public-access block, versioning, and
DynamoDB lock table encryption.
EOF
