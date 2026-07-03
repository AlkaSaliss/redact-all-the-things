## 1. AWS Live Stack

- [x] 1.1 Configure AWS Terragrunt remote state and DynamoDB locking from environment values.
- [x] 1.2 Keep the AWS provider production-only and free of Floci endpoint overrides.

## 2. Deployment Workflow

- [x] 2.1 Update the infrastructure workflow to pass remote-state configuration to AWS plan/apply jobs.
- [x] 2.2 Publish reviewed AWS plan artifacts and apply the saved plan after `aws-production` approval.

## 3. Smoke, Docs, and Follow-up

- [x] 3.1 Add an AWS-only smoke entrypoint for production services not covered by Floci.
- [x] 3.2 Document real AWS setup, remote-state bootstrap, smoke usage, and deferred budget alerts.
- [x] 3.3 Create and link the budget-alert follow-up issue.

## 4. Verification

- [ ] 4.1 Run OpenSpec validation, infrastructure validation, docs build, and Graphify refresh.
