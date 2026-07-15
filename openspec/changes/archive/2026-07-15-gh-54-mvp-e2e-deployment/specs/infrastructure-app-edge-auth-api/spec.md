## ADDED Requirements

### Requirement: Publish real frontend application

The frontend deployment workflow SHALL publish the tested React build to the
private frontend bucket using the Terraform toolchain supported by the live
stack.

#### Scenario: Resolve live outputs with pinned Terraform

- **WHEN** the frontend deployment job resolves Terragrunt outputs
- **THEN** it installs the repository-supported Terraform version explicitly
- **AND** it obtains the frontend bucket and CloudFront distribution outputs
  from the selected live environment.

#### Scenario: Publish and invalidate frontend assets

- **WHEN** the frontend build and deployment jobs succeed
- **THEN** the published build embeds the selected environment's API endpoint,
  AWS region, Cognito user pool, browser client, and hosted UI URL
- **AND** the built assets are synchronized to the private frontend bucket
- **AND** the CloudFront distribution is invalidated so the new application is
  served.
