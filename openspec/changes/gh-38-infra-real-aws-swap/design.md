## Context

The infrastructure milestone has completed the Floci foundation, app
edge/auth/API, and worker compute slices. The AWS live stack already selects
`deployment_mode = "aws"` and omits provider endpoint overrides, but it still
uses local Terraform state and the workflow does not publish a reviewed plan
artifact before apply.

Issue #38 is the production-account swap slice. The approved account-specific
values are intentionally not stored in the repository.

## Goals / Non-Goals

**Goals:**

- Configure the AWS live stack for S3 remote state and DynamoDB locking.
- Keep all account-specific backend identifiers in environment or GitHub
  configuration.
- Make manual GitHub Actions plan/apply runs produce reviewable plan artifacts.
- Add an AWS-only smoke entrypoint for production services that Floci cannot
  cover.
- Document remote-state bootstrap and cost-model revalidation.

**Non-Goals:**

- Provision the remote-state bucket or lock table.
- Commit AWS account IDs, backend names, notification emails, or SNS ARNs.
- Manage AWS Budgets alerts in this slice.
- Change the Floci local validation path.

## Decisions

### Read remote-state identifiers from environment

`infra/live/aws/terragrunt.hcl` will read `TG_STATE_BUCKET`,
`TG_LOCK_TABLE`, and an optional `TG_STATE_REGION`. Terragrunt will fail with a
direct message when the bucket or table is missing. This keeps the repository
portable across the approved account while still making remote state mandatory
for the real AWS stack.

Alternative considered: hard-code bucket and table names. That would make local
plans simpler but would commit account-specific configuration and require a code
change for account migration.

### Keep the Floci and AWS live stacks separate

The Floci stack keeps local state, fake credentials, and endpoint overrides.
The AWS stack uses the default AWS provider and remote state. Make targets
continue to select the stack through `INFRA_TARGET`.

Alternative considered: one Terragrunt stack with conditional provider/backend
behavior. Separate live directories are easier to validate and reduce the risk
of leaking emulator settings into production.

### Publish plan artifacts before apply

The workflow will run `terragrunt plan -out=tfplan` and `terragrunt show
-no-color tfplan`, then upload the text plan and binary plan from the AWS live
stack. Apply will use the saved plan file in the gated apply job.

Alternative considered: keep applying with a fresh `terragrunt apply`. Reusing
the saved plan better matches the manual review requirement.

### Defer AWS budget alerts to a follow-up issue

This slice will document cost-model revalidation and link issue #42 for budget
alerts. Terraform-managed alerts require a notification target that is not
available in the repository and should not be invented in this change.

## Risks / Trade-offs

- Missing backend variables block AWS planning. Mitigation: fail early with
  explicit variable names and document the required GitHub configuration.
- Applying a saved plan requires the apply job to download artifacts from the
  same workflow run. Mitigation: keep plan and apply in one workflow and make
  apply depend on the plan job.
- AWS smoke checks cannot verify real service health without deployed account
  access during local development. Mitigation: keep the script read-only and
  parameterized by Terragrunt outputs.

## Migration Plan

1. Bootstrap the approved account with an S3 state bucket and DynamoDB lock
   table outside this repository.
2. Configure GitHub `AWS_ROLE_TO_ASSUME`, `TG_STATE_BUCKET`, `TG_LOCK_TABLE`,
   and optional region variables/secrets.
3. Dispatch the infrastructure workflow with `plan` and review the uploaded
   plan artifact.
4. Dispatch with `apply`; approve the `aws-production` environment gate.
5. Run the AWS smoke entrypoint after apply.
