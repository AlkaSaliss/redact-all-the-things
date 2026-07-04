## Why

The worker can validate sources, rasterize pages, extract OCR text, detect PII,
and create review manifests, but it still treats analysis as one uninterrupted
run. Interrupted worker runs can repeat completed work, and successful analysis
does not yet persist progress or transition jobs to review-ready state.

This combined slice implements the checkpoint/resume work from #20 together
with the manifest and lifecycle integration from #21.

## What Changes

- Use the existing `Job.completed_pages` field as the durable checkpoint cursor.
- Transition analysis jobs from `queued` to `analyzing`, persist page count and
  model versions, checkpoint after each fully completed page, and transition to
  `ready` when all page manifests are available.
- Resume analysis by skipping pages at or below `completed_pages` and reusing
  deterministic page, OCR, and manifest keys.
- Treat an already-created matching initial manifest as an idempotent success
  when checkpoint persistence was interrupted after the manifest write.
- Preserve safe failure behavior for validation, rasterization, OCR, PII,
  manifest, and progress persistence errors.
- Keep export rendering, frontend review UI, and new public APIs out of scope.

## Capabilities

### New Capabilities

- `worker-checkpoint-manifest-integration`: Worker analysis checkpointing,
  resume behavior, progress persistence, and review-ready lifecycle completion.

### Modified Capabilities

- `job-contracts`: Existing job fields are used more fully for analysis
  progress and ready-state completion.

## Impact

- Updates worker orchestration, persistence protocols, worker tests, shared
  job lifecycle tests, architecture documentation, and OpenSpec artifacts.
- Reuses existing job fields and S3-style owner/job artifact namespaces.
- Does not add a new checkpoint schema, HTTP route, or production
  infrastructure resource.
