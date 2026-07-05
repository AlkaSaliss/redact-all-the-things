## MODIFIED Requirements

### Requirement: Complete real multipart uploads robustly
The control-plane API SHALL complete real S3 multipart uploads from browser or
smoke clients that report uploaded parts in any order.

#### Scenario: Complete unordered uploaded parts
- **WHEN** an upload completion request includes unique uploaded parts in any
  order
- **THEN** the service sends the parts to S3 sorted by part number and submits
  analysis after the source object exists.

#### Scenario: Reject duplicate uploaded parts
- **WHEN** an upload completion request contains duplicate part numbers
- **THEN** the service rejects the request without completing the upload.
