## 1. OpenSpec

- [x] 1.1 Add checkpoint/resume and manifest lifecycle capability requirements.
- [x] 1.2 Capture combined #20/#21 design decisions and task plan.

## 2. Worker Tests

- [x] 2.1 Cover queued-to-analyzing-to-ready analysis with page-count and per-page progress checkpoints.
- [x] 2.2 Cover resume from `completed_pages` skipping completed pages.
- [x] 2.3 Cover later-page processing failure preserving prior completed progress.
- [x] 2.4 Cover idempotent existing initial manifest after interrupted checkpoint persistence.
- [x] 2.5 Cover invalid or missing resume artifacts failing safely.
- [x] 2.6 Update existing worker expectations from queued success to ready success where full analysis runs.

## 3. Worker Implementation

- [x] 3.1 Add artifact index loading and manifest confirmation protocol methods.
- [x] 3.2 Persist analysis start state with page count and model versions.
- [x] 3.3 Process pending pages after `completed_pages` and checkpoint only after full page completion.
- [x] 3.4 Transition to `ready` after all pages are complete.
- [x] 3.5 Preserve validation, processing, and retry-safe failure behavior.

## 4. Documentation and Verification

- [x] 4.1 Update worker architecture documentation for checkpoints, resume, and lifecycle integration.
- [x] 4.2 Run focused worker/domain/service tests.
- [x] 4.3 Run strict MkDocs and OpenSpec validation.
- [x] 4.4 Run `graphify update .`.
