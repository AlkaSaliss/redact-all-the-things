## Context

Issues #20 and #21 are adjacent worker slices. #20 asks for checkpoint/resume
behavior so interrupted analysis can continue without reprocessing completed
pages unnecessarily. #21 asks the worker to integrate outputs with page
manifests and persistent job progress/status contracts.

The worker already writes deterministic page artifact, OCR artifact, and page
manifest keys. The shared `Job` contract already contains `page_count`,
`completed_pages`, `status`, `model_versions`, and optimistic `version`, so a
separate checkpoint artifact would duplicate existing durable job metadata.

## Goals / Non-Goals

**Goals:**

- Use `completed_pages` as the page-level checkpoint cursor.
- Persist `analyzing` state, page count, model versions, per-page progress, and
  final `ready` state.
- Resume from the first page after `completed_pages`.
- Make manifest creation idempotent when the manifest write succeeded but the
  checkpoint save did not.
- Keep validation and processing failures safe and privacy-preserving.

**Non-Goals:**

- Add a new checkpoint artifact or data model.
- Add frontend review UI, export rendering, or new HTTP APIs.
- Rework OCR, PII detection, or rasterization contracts beyond what resume
  requires.
- Add infrastructure deployment behavior.

## Decisions

### Use Job.completed_pages as the checkpoint

The worker will persist `completed_pages` only after a page's OCR artifact, PII
mapping, and initial page manifest are complete. That makes a checkpoint equal
to review readiness for that page and avoids partial review state.

Partial in-flight work for the current page may be repeated after retry. This
is acceptable because object keys are deterministic and it avoids a larger
per-stage checkpoint schema.

### Transition through analyzing to ready

Full analysis starts by moving eligible jobs to `analyzing` and persisting the
validated `page_count`. The worker then increments progress after each page and
marks the job `ready` only when `completed_pages == page_count`.

The control-plane retry path already moves retryable analyze failures back to
`queued`; this slice keeps that contract and lets the worker resume from the
saved cursor.

### Keep resume artifact reads narrow

Resume needs the page-artifact index when `completed_pages > 0` so the worker
can process remaining pages without rerasterizing completed pages. The worker
will read and validate the existing index, then process only pages greater
than the checkpoint.

### Treat existing matching initial manifests as idempotent

If manifest creation reports that a manifest already exists, the worker will
load it and accept it only when it matches the initial manifest the worker
would have written. This covers the interrupted window between manifest write
and progress checkpoint save without accepting user-edited or mismatched
review state as a worker-created checkpoint.

## Risks / Trade-offs

- **Current-page work can be repeated** -> The page checkpoint is intentionally
  coarse to avoid new schema and partial completion semantics.
- **Rerasterization after zero progress can overwrite artifacts** -> No page
  was checkpointed yet, so deterministic replacement is acceptable.
- **Manifest idempotency must not erase user edits** -> Existing manifests are
  accepted only when they match the initial worker-generated manifest.
- **Lifecycle integration broadens #20** -> This PR explicitly combines #20 and
  #21 so the backlog remains accurate.

## Migration Plan

1. Add OpenSpec requirements for checkpoint/resume and lifecycle integration.
2. Add deterministic worker tests for progress, resume, idempotent manifests,
   and safe failures.
3. Implement worker progress helpers, index loading, per-page processing, and
   idempotent manifest creation.
4. Update architecture documentation and relevant lifecycle tests.
5. Run focused tests, strict MkDocs, strict OpenSpec validation, and Graphify.

Rollback is reverting the OpenSpec change, worker orchestration updates, tests,
and docs. No data migration is required because the slice only uses existing
job fields and deterministic object keys.

## Open Questions

None.
