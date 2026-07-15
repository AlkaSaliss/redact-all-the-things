## MODIFIED Requirements

### Requirement: Browser review workflow
The frontend SHALL provide an authenticated desktop workflow for upload, job status, page review, redaction editing, export, and download using the shared job, page summary, and manifest contracts.

#### Scenario: Authenticated API-backed runtime
- **WHEN** the app runs locally or from CloudFront
- **THEN** it uses configured dev-stack API and Cognito Hosted UI settings

#### Scenario: Navigate primary workflows
- **WHEN** a user activates Jobs, Upload, Back to Jobs, or a reviewable job
- **THEN** the corresponding dashboard, upload panel, or resumable editor becomes active and the control exposes accessible button semantics

#### Scenario: Upload with feedback and cancellation
- **WHEN** a user selects a supported file within the documented limits
- **THEN** the frontend displays upload state and progress, permits cancellation while the transfer is active, and refreshes the job dashboard after completion

#### Scenario: Reject invalid upload
- **WHEN** a user selects an unsupported or oversized file
- **THEN** the frontend explains why the file was rejected without creating a job

#### Scenario: Navigate review pages
- **WHEN** a user activates a page thumbnail
- **THEN** the frontend loads and displays that page's preview and manifest while preserving edits and save status for other visited pages

#### Scenario: Edit normalized regions
- **WHEN** a user draws, selects, moves, resizes, deletes, or toggles redaction regions at any supported zoom
- **THEN** the frontend updates normalized page-bounded geometry and exposes PII details for the selected region

#### Scenario: Navigate and select suggestions
- **WHEN** a user activates previous suggestion, next suggestion, select all, or deselect all
- **THEN** the frontend updates the active suggestion or page selection without changing unrelated pages

#### Scenario: Undo and redo page edits
- **WHEN** a user activates toolbar controls or standard keyboard shortcuts for undo or redo
- **THEN** the frontend traverses the current page's bounded session history one committed edit at a time

#### Scenario: Autosave page edits
- **WHEN** a user commits a redaction edit on a page
- **THEN** the frontend saves that page manifest with its expected version and displays saving, saved, or failed state independently of other pages

#### Scenario: Recover failed autosave
- **WHEN** an autosave fails and the user retries
- **THEN** the frontend retries the current local regions for that page without discarding the edit

#### Scenario: Display actionable job states
- **WHEN** a job is loading, processing, failed, exporting, complete, expired, or absent
- **THEN** the frontend displays the relevant status and offers only valid resume, retry, download, or upload actions

#### Scenario: Confirm export
- **WHEN** a user asks to export a reviewed job
- **THEN** the frontend requires acknowledgement that automated detection may miss PII before calling the export API

#### Scenario: Download completed export
- **WHEN** an owner activates Download for a complete unexpired job
- **THEN** the frontend requests a fresh short-lived download authorization and opens the returned output URL
