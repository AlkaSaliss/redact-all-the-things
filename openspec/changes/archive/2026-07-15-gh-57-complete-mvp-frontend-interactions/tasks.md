## 1. Behavioral Coverage

- [x] 1.1 Add unit tests for normalized draw, move, resize, and bounded page history behavior.
- [x] 1.2 Add API client tests for retry, download authorization, and abortable upload behavior.
- [x] 1.3 Add workspace/editor interaction tests for navigation, per-page manifests, undo/redo, selection, autosave recovery, upload states, and completed downloads.

## 2. Editing Workflow

- [x] 2.1 Implement normalized pointer drawing, movement, resizing, deletion, and zoom-stable geometry.
- [x] 2.2 Implement page-keyed undo/redo, keyboard controls, suggestion navigation, and select/deselect-all.
- [x] 2.3 Implement page navigation with cached manifests, independent autosave state, and retry without edit loss.

## 3. Job and Upload Workflow

- [x] 3.1 Make Jobs, Upload, Back to Jobs, job resume, and status-aware empty/detail views interactive and accessible.
- [x] 3.2 Implement upload validation feedback, active progress/status, cancellation, completion reset, and error recovery.
- [x] 3.3 Implement active-job refresh, eligible failed-job retry, export-state feedback, and authorized completed download.

## 4. Documentation and Verification

- [x] 4.1 Update frontend/development documentation to describe the complete MVP interactions and recovery behavior.
- [x] 4.2 Run frontend tests and build, relevant Python tests, and strict MkDocs validation.
- [x] 4.3 Run browser smoke coverage, OpenSpec verification, diff review, and Graphify refresh.
