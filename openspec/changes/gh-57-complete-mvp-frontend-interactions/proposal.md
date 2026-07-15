## Why

The frontend renders the shape of the MVP workflow, but several controls are inert and important technical-scope behaviors are absent. Users cannot reliably navigate multi-page documents, edit redactions, recover changes, complete uploads, or download finished exports, so the deployed application is not yet usable as an MVP.

## What Changes

- Make Jobs, Upload, Back to Jobs, job selection, retry, and resume actions functional and accessible.
- Implement page-specific loading and autosave, page navigation, suggestion navigation, selection controls, and session undo/redo.
- Replace the placeholder manual-region control with pointer-based rectangle drawing and add pointer-based move and resize behavior with zoom-stable normalized geometry.
- Add upload validation, status, progress, error, and cancellation behavior.
- Add export polling/status refresh and an authorized download action for completed jobs.
- Add explicit loading, empty, failed, exporting, complete, and expired UI states with behavioral tests.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `review-export-workflow`: Expand the browser review workflow requirements to cover the already-approved MVP interactions in the technical scope.

## Impact

The change affects the React workspace/editor, client-side state and geometry helpers, API client upload cancellation, UI tests, and frontend documentation. It uses existing control-plane routes and contracts; there are no backend API, data-model, infrastructure, dependency, or architecture changes.
