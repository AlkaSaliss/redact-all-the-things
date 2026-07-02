## Context

The control plane already expects `BATCH_JOB_QUEUE` and
`BATCH_JOB_DEFINITION`. The infrastructure stack must provide concrete Batch
queue and job-definition names while the final worker image and CI publishing
workflow are still deferred to later slices.

## Decisions

### Compose the app edge/auth/API module

Create `infra/modules/worker-compute-artifacts` and source the app module from
it. This preserves a single Floci live stack while adding worker resources on
top of the app resources.

### Model Batch/Fargate Spot with one-worker capacity

Use AWS Batch with a Fargate Spot compute environment capped at 2 vCPU. The
analyze and render job definitions each request 2 vCPU and 8192 MiB, which
models the documented one-active-worker global concurrency limit.

### Include minimal worker networking

Add a small VPC, two private subnets, and a worker security group with no
ingress. This avoids depending on a default VPC and keeps the no-inbound-worker
boundary visible. Egress remains open for emulator/static modeling and can be
tightened when real AWS networking endpoints are finalized.

### Keep worker stubs separate from product worker code

Add a minimal worker Dockerfile and script under `infra/stubs/worker`. Terraform
references the ECR repository/tag shape, but this slice does not publish images.
The real worker image build/publish workflow remains a later slice.

## Risks

- Floci's coverage of AWS Batch, ECS/Fargate, ECR, and EC2 networking
  resources may not match AWS exactly. Static Terraform validation and plan
  are the primary checks for this slice.
- A future provider version may require DynamoDB key-schema syntax changes
  inherited from the app module. This slice keeps the currently validated
  provider shape.
- Network endpoint and image-pull details may need refinement during the real
  AWS swap.

## Rollout

1. Add worker module and stubs.
2. Point Floci Terragrunt at the worker module.
3. Extend validation to include the worker module.
4. Update docs and smoke guidance.
5. Validate OpenSpec, docs, Terraform/Terragrunt, plan, smoke, and tests.
