import {
  ArrowLeft,
  CheckCircle2,
  CloudUpload,
  FileText,
  HelpCircle,
  Loader2,
  Lock,
  LogOut,
  MousePointer2,
  Plus,
  RotateCcw,
  RotateCw,
  SquareDashedMousePointer,
  Trash2,
  ZoomIn,
  ZoomOut,
} from "lucide-react";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import type { User, UserManager } from "oidc-client-ts";
import { RedactionApiClient, uploadMultipartPart } from "./api/client";
import { createUserManager, displayUser } from "./auth";
import { missingConfig, readConfig } from "./config";
import type {
  Job,
  PageManifest,
  PageSummary,
  RedactionRegion,
  SourceType,
} from "./contracts/types";
import { createManualRegion, moveRegion, regionStyle } from "./editor/geometry";

type SaveState = "idle" | "saving" | "saved" | "failed";
type Tool = "select" | "draw";

const ACCEPTED_TYPES = new Set(["application/pdf", "image/jpeg", "image/png"]);
const MAX_FILE_SIZE = 100 * 1024 * 1024;

export function App() {
  const config = useMemo(readConfig, []);
  const missing = useMemo(() => missingConfig(config), [config]);
  const [userManager, setUserManager] = useState<UserManager | null>(null);
  const [user, setUser] = useState<User | null>(null);
  const [authError, setAuthError] = useState<string | null>(null);

  useEffect(() => {
    if (missing.length > 0) return;
    const manager = createUserManager(config);
    setUserManager(manager);
    if (window.location.pathname === "/auth/callback") {
      manager
        .signinRedirectCallback()
        .then((nextUser) => {
          setUser(nextUser);
          window.history.replaceState({}, "", "/");
        })
        .catch((error: unknown) => setAuthError(String(error)));
      return;
    }
    manager.getUser().then(setUser).catch(() => setUser(null));
  }, [config, missing.length]);

  if (missing.length > 0 || !user) {
    return (
      <AuthShell
        missing={missing}
        onSignIn={() => userManager?.signinRedirect()}
        authError={authError}
      />
    );
  }

  const api = new RedactionApiClient(config.apiEndpoint, async () => {
    const current = await userManager?.getUser();
    if (!current?.access_token) throw new Error("missing access token");
    return current.access_token;
  });

  return (
    <Workspace
      api={api}
      userLabel={displayUser(user)}
      onSignOut={() => userManager?.signoutRedirect()}
    />
  );
}

function AuthShell({
  missing,
  onSignIn,
  authError,
}: {
  missing: string[];
  onSignIn: () => void;
  authError: string | null;
}) {
  const connected = missing.length === 0;
  return (
    <main className="auth-shell">
      <header className="auth-header">
        <div className="brand">
          <Lock size={28} />
          <span>Redact All The Things</span>
        </div>
        <span className="muted">Not signed in</span>
      </header>
      <section className="signin-panel">
        <Lock size={34} />
        <h1>Sign in to Redact All The Things</h1>
        <p>Invited users only</p>
        <button className="primary full" disabled={!connected} onClick={onSignIn}>
          Continue with Cognito
        </button>
        <div className="config-list">
          <ConfigRow label="API endpoint" ok={!missing.includes("apiEndpoint")} />
          <ConfigRow label="Region" ok={!missing.includes("awsRegion")} />
          <ConfigRow label="Hosted UI" ok={!missing.includes("hostedUiUrl")} />
        </div>
        {authError && <p className="error-text">{authError}</p>}
      </section>
    </main>
  );
}

function ConfigRow({ label, ok }: { label: string; ok: boolean }) {
  return (
    <div className="config-row">
      <span>{label}</span>
      <strong className={ok ? "ok" : "warn"}>{ok ? "Connected" : "Missing"}</strong>
    </div>
  );
}

function Workspace({
  api,
  userLabel,
  onSignOut,
}: {
  api: RedactionApiClient;
  userLabel: string;
  onSignOut: () => void;
}) {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [selectedJobId, setSelectedJobId] = useState("");
  const [pages, setPages] = useState<PageSummary[]>([]);
  const [manifest, setManifest] = useState<PageManifest | null>(null);
  const [apiError, setApiError] = useState<string | null>(null);
  const [saveState, setSaveState] = useState<SaveState>("idle");
  const [uploadProgress, setUploadProgress] = useState(0);
  const [exportOpen, setExportOpen] = useState(false);
  const [acknowledged, setAcknowledged] = useState(false);

  const selectedJob = jobs.find((job) => job.id === selectedJobId) ?? jobs[0];

  const refreshJobs = useCallback(async () => {
    try {
      const nextJobs = await api.listJobs();
      setJobs(nextJobs);
      setSelectedJobId((current) =>
        nextJobs.some((job) => job.id === current) ? current : nextJobs[0]?.id || "",
      );
      setApiError(null);
    } catch (error) {
      setJobs([]);
      setSelectedJobId("");
      setPages([]);
      setManifest(null);
      setApiError(error instanceof Error ? error.message : "Unable to load jobs");
    }
  }, [api]);

  useEffect(() => {
    void refreshJobs();
  }, [refreshJobs]);

  useEffect(() => {
    setPages([]);
    setManifest(null);
    if (!selectedJob || selectedJob.status !== "ready") return;
    Promise.all([
      api.listPages(selectedJob.id),
      api.getManifest(selectedJob.id, 1),
    ])
      .then(([nextPages, nextManifest]) => {
        setPages(nextPages);
        setManifest(nextManifest);
        setApiError(null);
      })
      .catch((error: unknown) => {
        setApiError(
          error instanceof Error ? error.message : "Unable to load page manifest",
        );
      });
  }, [api, selectedJob]);

  async function handleUpload(file: File) {
    if (!ACCEPTED_TYPES.has(file.type) || file.size > MAX_FILE_SIZE) {
      return;
    }
    const sourceType: SourceType =
      file.type === "application/pdf"
        ? "pdf"
        : file.type === "image/jpeg"
          ? "jpeg"
          : "png";
    const created = await api.createJob(sourceType, file.size);
    const etag = await uploadMultipartPart(
      created.upload_parts[0].upload_url,
      file,
      setUploadProgress,
    );
    await api.completeUpload(created.job.id, created.upload_id, [
      { part_number: 1, etag },
    ]);
    await refreshJobs();
  }

  async function handleSave(regions: RedactionRegion[]) {
    if (!selectedJob || !manifest) return;
    setSaveState("saving");
    try {
      const saved = await api.saveManifest(
        selectedJob.id,
        manifest.page_number,
        manifest.version,
        regions,
      );
      setManifest(saved);
      setSaveState("saved");
    } catch {
      setSaveState("failed");
    }
  }

  async function handleExport() {
    if (!selectedJob || !acknowledged) return;
    await api.confirmExport(selectedJob.id);
    setExportOpen(false);
    setAcknowledged(false);
    await refreshJobs();
  }

  return (
    <main className="app-shell">
      <header className="topbar">
        <div className="brand">
          <FileText size={28} />
          <span>Redact All The Things</span>
        </div>
        <div className="topbar-actions">
          <span className="system-ok">All Systems Operational</span>
          <span>{userLabel}</span>
          <button className="icon-button" onClick={onSignOut} aria-label="Sign out">
            <LogOut size={18} />
          </button>
          <HelpCircle size={20} />
        </div>
      </header>
      <nav className="sidebar">
        <a className="active">Jobs</a>
        <a>Upload</a>
      </nav>
      <section className="jobs-pane">
        <div className="pane-header">
          <h2>Recent Jobs</h2>
          <button className="icon-button" onClick={() => void refreshJobs()}>
            <RotateCw size={18} />
          </button>
        </div>
        {apiError && <p className="api-error">{apiError}</p>}
        <JobTable jobs={jobs} selected={selectedJob?.id} onSelect={setSelectedJobId} />
        <UploadPanel onUpload={(file) => void handleUpload(file)} progress={uploadProgress} />
      </section>
      {selectedJob && manifest ? (
        <Editor
          job={selectedJob}
          pages={pages}
          manifest={manifest}
          saveState={saveState}
          onChange={setManifest}
          onSave={(regions) => void handleSave(regions)}
          onExport={() => setExportOpen(true)}
        />
      ) : (
        <section className="empty-workspace">
          <FileText size={40} />
          <h2>No reviewable document selected</h2>
          <p>Upload a PDF, JPEG, or PNG file. Ready jobs open here for review.</p>
        </section>
      )}
      {exportOpen && (
        <ExportDialog
          acknowledged={acknowledged}
          onAcknowledge={setAcknowledged}
          onCancel={() => setExportOpen(false)}
          onConfirm={() => void handleExport()}
        />
      )}
    </main>
  );
}

function JobTable({
  jobs,
  selected,
  onSelect,
}: {
  jobs: Job[];
  selected?: string;
  onSelect: (jobId: string) => void;
}) {
  return (
    <table className="jobs-table">
      <thead>
        <tr>
          <th>Job</th>
          <th>Status</th>
          <th>Pages</th>
          <th>Expires</th>
        </tr>
      </thead>
      <tbody>
        {jobs.length === 0 && (
          <tr>
            <td colSpan={4} className="empty-row">
              No jobs yet.
            </td>
          </tr>
        )}
        {jobs.map((job) => (
          <tr
            key={job.id}
            className={job.id === selected ? "selected" : ""}
            onClick={() => onSelect(job.id)}
          >
            <td>{job.id}</td>
            <td>
              <span className={`status ${job.status}`}>{job.status}</span>
            </td>
            <td>{job.page_count || "-"}</td>
            <td>{new Date(job.expires_at).toLocaleString()}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

function UploadPanel({
  onUpload,
  progress,
}: {
  onUpload: (file: File) => void;
  progress: number;
}) {
  const inputRef = useRef<HTMLInputElement | null>(null);
  return (
    <section className="upload-panel">
      <h2>Upload Document (PDF, JPEG, PNG)</h2>
      <p>Max file size 100 MB · PDF max 200 pages</p>
      <button className="dropzone" onClick={() => inputRef.current?.click()}>
        <CloudUpload size={34} />
        <span>Choose File</span>
      </button>
      <input
        ref={inputRef}
        type="file"
        accept=".pdf,.jpg,.jpeg,.png,application/pdf,image/jpeg,image/png"
        hidden
        onChange={(event) => {
          const file = event.target.files?.[0];
          if (file) onUpload(file);
        }}
      />
      {progress > 0 && (
        <div className="progress">
          <span style={{ width: `${progress}%` }} />
        </div>
      )}
    </section>
  );
}

function Editor({
  job,
  pages,
  manifest,
  saveState,
  onChange,
  onSave,
  onExport,
}: {
  job: Job;
  pages: PageSummary[];
  manifest: PageManifest;
  saveState: SaveState;
  onChange: (manifest: PageManifest) => void;
  onSave: (regions: RedactionRegion[]) => void;
  onExport: () => void;
}) {
  const [tool, setTool] = useState<Tool>("select");
  const [selectedId, setSelectedId] = useState(manifest.regions[0]?.id);
  const [zoom, setZoom] = useState(1);
  const saveTimer = useRef<number | null>(null);
  const currentPage = pages[manifest.page_number - 1] ?? pages[0];
  const selected = manifest.regions.find((region) => region.id === selectedId);

  function updateRegions(regions: RedactionRegion[]) {
    const next = { ...manifest, regions };
    onChange(next);
    if (saveTimer.current) window.clearTimeout(saveTimer.current);
    saveTimer.current = window.setTimeout(() => onSave(regions), 700);
  }

  function addRegion() {
    const region = createManualRegion(manifest.page_number, 0.62, 0.1);
    setSelectedId(region.id);
    updateRegions([...manifest.regions, region]);
  }

  function deleteRegion() {
    if (!selectedId) return;
    updateRegions(manifest.regions.filter((region) => region.id !== selectedId));
    setSelectedId(manifest.regions[0]?.id);
  }

  return (
    <section className="editor">
      <header className="editor-header">
        <button className="text-button">
          <ArrowLeft size={18} /> Back to Jobs
        </button>
        <strong>{job.id}</strong>
        <span className="status ready">ready</span>
        <span className="expiry">Expires {new Date(job.expires_at).toLocaleString()}</span>
      </header>
      <div className="toolbar">
        <button className={tool === "select" ? "active" : ""} onClick={() => setTool("select")}>
          <MousePointer2 size={18} /> Select
        </button>
        <button className={tool === "draw" ? "active" : ""} onClick={() => setTool("draw")}>
          <SquareDashedMousePointer size={18} /> Draw Rectangle
        </button>
        <button onClick={deleteRegion}>
          <Trash2 size={18} /> Delete
        </button>
        <button onClick={() => setZoom((value) => Math.max(0.5, value - 0.1))}>
          <ZoomOut size={18} /> Zoom Out
        </button>
        <span>{Math.round(zoom * 100)}%</span>
        <button onClick={() => setZoom((value) => Math.min(2, value + 0.1))}>
          <ZoomIn size={18} /> Zoom In
        </button>
        <button>
          <RotateCcw size={18} /> Undo
        </button>
        <button>
          <RotateCw size={18} /> Redo
        </button>
        <span className={`autosave ${saveState}`}>
          {saveState === "saving" && <Loader2 size={16} />}
          {saveState === "saved" && <CheckCircle2 size={16} />}
          {saveState === "failed" ? "Autosave failed" : "Autosave"}
        </span>
      </div>
      <aside className="pages-strip">
        <h3>Pages</h3>
        {pages.map((page) => (
          <button key={page.page_number} className="thumbnail">
            <img src={page.preview_url} alt={`Page ${page.page_number}`} />
            <span>{page.page_number}</span>
            <strong>{page.suggestion_count}</strong>
          </button>
        ))}
      </aside>
      <section className="canvas-wrap">
        <div className="page-canvas" style={{ transform: `scale(${zoom})` }}>
          <img src={currentPage?.preview_url} alt={`Page ${manifest.page_number}`} />
          <div className="region-layer">
            {manifest.regions.map((region) => (
              <button
                key={region.id}
                className={`region ${region.id === selectedId ? "selected" : ""}`}
                style={regionStyle(region)}
                onClick={() => setSelectedId(region.id)}
                onDoubleClick={() =>
                  updateRegions(
                    manifest.regions.map((item) =>
                      item.id === region.id ? moveRegion(item, 0.02, 0.02) : item,
                    ),
                  )
                }
              />
            ))}
            {tool === "draw" && (
              <button className="draw-target" onClick={addRegion}>
                <Plus size={20} />
              </button>
            )}
          </div>
        </div>
      </section>
      <aside className="inspector">
        <h3>Selected Region</h3>
        {selected ? (
          <>
            <dl>
              <dt>Source</dt>
              <dd>{selected.source}</dd>
              <dt>Category</dt>
              <dd>{selected.category}</dd>
              <dt>Confidence</dt>
              <dd>{selected.confidence ?? "-"}</dd>
            </dl>
            <label className="toggle-row">
              Selected
              <input
                type="checkbox"
                checked={selected.selected}
                onChange={(event) =>
                  updateRegions(
                    manifest.regions.map((region) =>
                      region.id === selected.id
                        ? { ...region, selected: event.target.checked }
                        : region,
                    ),
                  )
                }
              />
            </label>
          </>
        ) : (
          <p className="muted">No region selected.</p>
        )}
        <button className="danger" onClick={deleteRegion}>
          Delete Region
        </button>
        <button className="primary" onClick={onExport}>
          Review & Export
        </button>
      </aside>
    </section>
  );
}

function ExportDialog({
  acknowledged,
  onAcknowledge,
  onCancel,
  onConfirm,
}: {
  acknowledged: boolean;
  onAcknowledge: (value: boolean) => void;
  onCancel: () => void;
  onConfirm: () => void;
}) {
  return (
    <div className="modal-backdrop">
      <section className="export-dialog">
        <h2>Ready to export?</h2>
        <p>Automated detection may miss PII. Review the document thoroughly before exporting.</p>
        <label>
          <input
            type="checkbox"
            checked={acknowledged}
            onChange={(event) => onAcknowledge(event.target.checked)}
          />
          I have reviewed the document and understand that PII may have been missed.
        </label>
        <div className="dialog-actions">
          <button onClick={onCancel}>Cancel</button>
          <button className="primary" disabled={!acknowledged} onClick={onConfirm}>
            Review & Export
          </button>
        </div>
      </section>
    </div>
  );
}
