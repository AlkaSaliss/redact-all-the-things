## Context

The SPA currently keeps one manifest in `Workspace`, always loads page 1, and renders several toolbar/sidebar controls without handlers. Manual drawing is a fixed-position add button, and region movement is simulated by double-clicking. The API already exposes page manifests, retry, export, and download authorization, so the missing work is predominantly client-side state and interaction behavior.

The technical scope requires per-page persistence, normalized geometry, upload cancellation, keyboard interactions, and status-aware resume/export behavior. The implementation must remain dependency-free and preserve the existing backend contracts.

## Goals / Non-Goals

**Goals:**

- Provide a complete, accessible desktop MVP path from upload through review to download.
- Keep page manifests, history, autosave, and save status isolated by page.
- Use normalized pointer geometry so drawing, moving, and resizing remain correct at every supported zoom.
- Make job and upload navigation reflect actual application state rather than decorative links.
- Cover the user-visible behavior with deterministic component and helper tests.

**Non-Goals:**

- Change control-plane routes, job contracts, authentication, worker rendering, or infrastructure.
- Add mobile editor support, collaborative editing, batch upload, or new redaction tools.
- Introduce a routing, state-management, or canvas dependency.

## Decisions

### Keep workflow state in the existing React component tree

`Workspace` will own the active primary view, selected job, page summaries, a manifest cache keyed by page number, per-page save state, and operation errors. `Editor` will own transient interaction state and page-keyed undo/redo histories. This keeps API lifecycle state close to the API client while avoiding a new state library.

Alternative considered: add a router and global store. Rejected because there are only three local views and no URL contract in the approved scope.

### Cache and save manifests by page

Selecting a thumbnail will load that page's manifest once, then reuse its cached state. Autosave callbacks will carry the job ID, page number, expected version, and regions rather than reading whichever page happens to be active. Successful saves update only the matching cached manifest; failures retain local edits and expose a retry action.

Alternative considered: flush and replace a single manifest on every navigation. Rejected because it creates races between delayed saves and page changes and cannot provide independent per-page recovery.

### Model edits as page-keyed snapshots

Each committed edit stores a complete region-array snapshot in a bounded in-memory past/present/future history. Pointer movement uses a transient draft and commits one snapshot on pointer release, so undo reverses one user gesture rather than every pointer event. Successful autosave does not clear session history.

Alternative considered: command objects per edit. Rejected because the page region arrays are small and snapshots are simpler and less error-prone for mixed selection, draw, resize, delete, and toggle operations.

### Derive normalized geometry from the rendered region layer

Pointer coordinates and deltas will be divided by the layer's current bounding rectangle. Browser layout already includes the CSS zoom transform in that rectangle, keeping stored coordinates independent of visual scale. Geometry helpers will clamp minimum size and page bounds.

Alternative considered: an HTML canvas or third-party interaction library. Rejected because DOM overlays already exist and the required gestures are small enough to implement directly.

### Use abortable API-directed multipart upload with explicit UI state

`Workspace` will upload every API-provided 5 MB part in part-number order and complete the job with the collected ETags. `uploadMultipartPart` will accept an `AbortSignal`; the workspace will keep the active controller and expose Cancel while a transfer is pending. Because Fetch does not expose portable byte-level upload progress, the UI will report aggregate completed-part progress and explicit status text without adding an XHR abstraction.

### Refresh asynchronous job state while work is active

The workspace will periodically refresh while jobs are uploading, queued, analyzing, or exporting, and stop when none are active. Completed rows expose a Download action that requests a fresh owner-scoped URL immediately before navigation.

## Risks / Trade-offs

- [Whole-array history can grow during long sessions] → Bound history per page and commit only completed gestures.
- [Autosave requests can overlap during rapid edits] → Serialize saves per page through expected manifest versions and keep later local regions available for retry.
- [Presigned preview URLs can expire during a long review] → Reload page summaries when resuming a ready job and reload a manifest on first page visit.
- [Fetch cannot report portable byte-level upload progress] → Report aggregate completed-part progress, show an uploading state, and provide cancellation without adding an XHR abstraction.
- [Desktop pointer behavior differs across browsers] → Use standard Pointer Events, pointer capture, keyboard fallbacks, and browser smoke coverage.
