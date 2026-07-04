# Worker Checkpoint Manifest Integration Specification

## Purpose

Define how analysis workers persist page-level progress, resume from durable
checkpoints, and create review-ready page manifests.

## Requirements

### Requirement: Worker persists analysis lifecycle progress
The analysis worker SHALL persist analysis start, page count, completed page
progress, model versions, and review-ready completion through the shared job
contract.

#### Scenario: Start analysis
- **WHEN** a queued analysis job passes source validation
- **THEN** the worker persists the job with status `analyzing`, the validated page count, model versions for configured OCR and PII engines, and unchanged completed page count

#### Scenario: Checkpoint completed page
- **WHEN** OCR extraction, PII mapping, and initial page-manifest creation succeed for one page
- **THEN** the worker increments `completed_pages` to that page number with an optimistic job update

#### Scenario: Complete analysis
- **WHEN** every page has a completed checkpoint
- **THEN** the worker transitions the job to `ready`

### Requirement: Worker resumes from completed page checkpoints
The analysis worker SHALL use `completed_pages` as the durable checkpoint
cursor and skip completed pages on retry.

#### Scenario: Resume pending pages
- **WHEN** an analysis job is retried with `completed_pages` less than `page_count`
- **THEN** the worker processes only pages with page numbers greater than `completed_pages`

#### Scenario: Reuse page artifact index
- **WHEN** a retried job already has completed pages
- **THEN** the worker loads the existing page-artifact index instead of rerasterizing completed pages

#### Scenario: Reject invalid resume artifacts
- **WHEN** resume requires an existing page-artifact index but it is missing, invalid, or inconsistent with the job
- **THEN** the worker transitions the job to `failed` with safe failure code `processing_failed`

### Requirement: Initial manifest writes are retry safe
The analysis worker SHALL treat existing matching initial page manifests as
idempotent success when resuming after an interrupted checkpoint write.

#### Scenario: Existing initial manifest matches
- **WHEN** the worker attempts to create an initial page manifest that already exists and the stored manifest matches the worker-generated initial manifest
- **THEN** the worker accepts the page manifest and may checkpoint the page

#### Scenario: Existing initial manifest does not match
- **WHEN** the stored manifest differs from the worker-generated initial manifest
- **THEN** the worker transitions the job to `failed` with safe failure code `processing_failed`

### Requirement: Checkpoint failures are safe
The analysis worker SHALL preserve safe failure behavior for validation,
processing, artifact, manifest, and progress persistence failures.

#### Scenario: Preserve prior completed progress
- **WHEN** a page after the last checkpoint fails during OCR, PII mapping, manifest creation, or progress persistence
- **THEN** the worker records `processing_failed` without reducing the previously persisted completed page count

#### Scenario: Validation fails before analysis start
- **WHEN** source validation fails
- **THEN** the worker records the validation failure code and does not write analysis artifacts or page checkpoints
