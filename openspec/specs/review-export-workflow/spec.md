## Purpose

Define the review, redaction editing, and raster export workflow that connects
the browser client, control-plane API, and worker render path.

## Requirements

### Requirement: Page preview authorization

The control-plane API SHALL expose owner-checked page preview authorization for
reviewable jobs.

#### Scenario: List review pages

- **WHEN** an authenticated owner requests pages for a ready or failed job
- **THEN** the API returns page dimensions, manifest counts, manifest version,
  and a short-lived preview URL for each raster page artifact

#### Scenario: Refresh one page preview

- **WHEN** an authenticated owner requests a single page preview
- **THEN** the API returns a short-lived URL for the matching page artifact

### Requirement: Browser review workflow

The frontend SHALL provide an authenticated desktop review workflow using the
shared job, page summary, and manifest contracts.

#### Scenario: Authenticated API-backed runtime

- **WHEN** the app runs locally or from CloudFront
- **THEN** it uses configured dev-stack API and Cognito Hosted UI settings

#### Scenario: Autosave page edits

- **WHEN** a user edits redaction regions on a page
- **THEN** the frontend saves the page manifest with the expected version and
  displays saving, saved, or failed state

#### Scenario: Confirm export

- **WHEN** a user asks to export a reviewed job
- **THEN** the frontend requires acknowledgement that automated detection may
  miss PII before calling the export API

### Requirement: Raster-only render export

The worker SHALL render selected redaction regions into raster output artifacts
without copying source document metadata or text layers.

#### Scenario: Render PDF output

- **WHEN** a PDF job is exporting
- **THEN** the worker burns selected regions into raster page images, rebuilds
  a PDF from those images, writes the output object, and marks the job complete

#### Scenario: Render image output

- **WHEN** a JPEG or PNG job is exporting
- **THEN** the worker burns selected regions into a clean image in the source
  format, writes the output object, and marks the job complete
