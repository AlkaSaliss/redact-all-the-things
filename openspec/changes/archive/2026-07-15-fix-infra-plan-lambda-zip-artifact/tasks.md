## 1. Implementation

- [x] 1.1 Stage Lambda ZIP packages in S3 and remove local ZIP paths from
  Lambda function state.
- [x] 1.2 Make Lambda ZIP creation deterministic for unchanged inputs.
- [x] 1.3 Default AWS plan/apply worker image tags to the current git commit.

## 2. Verification

- [x] 2.1 Run Terraform/Terragrunt validation.
- [x] 2.2 Run OpenSpec validation.
- [x] 2.3 Run real AWS smoke checks.
- [x] 2.4 Verify repeated Lambda package builds produce the same hash.
