import {
  ArrowLeft,
  CheckCircle2,
  CloudUpload,
  Download,
  FileText,
  HelpCircle,
  Loader2,
  Lock,
  LogOut,
  MousePointer2,
  RotateCcw,
  RotateCw,
  SquareDashedMousePointer,
  Trash2,
  ZoomIn,
  ZoomOut,
} from "lucide-react";
import {
  type KeyboardEvent,
  type PointerEvent as ReactPointerEvent,
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
} from "react";
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
import {
  type Point,
  type ResizeHandle,
  moveRegion,
  regionFromPoints,
  regionStyle,
  resizeRegion,
} from "./editor/geometry";
import {
  type PageHistory,
  commitHistory,
  createHistory,
  redoHistory,
  undoHistory,
} from "./editor/history";

type SaveState = "idle" | "saving" | "saved" | "failed";
type Tool = "select" | "draw";
type PrimaryView = "jobs" | "upload";
type UploadState = "idle" | "uploading" | "complete" | "failed" | "cancelled";

const ACCEPTED_TYPES = new Set(["application/pdf", "image/jpeg", "image/png"]);
const MAX_FILE_SIZE = 100 * 1024 * 1024;
const UPLOAD_PART_SIZE = 5 * 1024 * 1024;
const ACTIVE_JOB_STATUSES = new Set(["uploading", "queued", "analyzing", "exporting"]);
const RETRYABLE_FAILURES = new Set([
  "analyze_transient",
  "analyze_spot_interrupted",
  "render_transient",
  "render_spot_interrupted",
]);

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

export function Workspace({
  api,
  userLabel,
  onSignOut,
}: {
  api: RedactionApiClient;
  userLabel: string;
  onSignOut: () => void;
}) {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [jobsLoading, setJobsLoading] = useState(true);
  const [primaryView, setPrimaryView] = useState<PrimaryView>("jobs");
  const [selectedJobId, setSelectedJobId] = useState("");
  const [pages, setPages] = useState<PageSummary[]>([]);
  const [manifests, setManifests] = useState<Record<number, PageManifest>>({});
  const manifestsRef = useRef(manifests);
  const [activePage, setActivePage] = useState(1);
  const [pageLoading, setPageLoading] = useState(false);
  const [apiError, setApiError] = useState<string | null>(null);
  const [saveStates, setSaveStates] = useState<Record<number, SaveState>>({});
  const saveTimers = useRef(new Map<number, number>());
  const saveQueues = useRef(new Map<number, Promise<void>>());
  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploadState, setUploadState] = useState<UploadState>("idle");
  const [uploadError, setUploadError] = useState<string | null>(null);
  const uploadController = useRef<AbortController | null>(null);
  const [exportOpen, setExportOpen] = useState(false);
  const [acknowledged, setAcknowledged] = useState(false);

  const selectedJob = jobs.find((job) => job.id === selectedJobId);
  const manifest = manifests[activePage];

  useEffect(() => {
    manifestsRef.current = manifests;
  }, [manifests]);

  useEffect(
    () => () => {
      saveTimers.current.forEach((timer) => window.clearTimeout(timer));
      uploadController.current?.abort();
    },
    [],
  );

  const refreshJobs = useCallback(async () => {
    try {
      const nextJobs = await api.listJobs();
      setJobs(nextJobs);
      setSelectedJobId((current) =>
        nextJobs.some((job) => job.id === current) ? current : "",
      );
      setApiError(null);
    } catch (error) {
      setJobs([]);
      setSelectedJobId("");
      setApiError(error instanceof Error ? error.message : "Unable to load jobs");
    } finally {
      setJobsLoading(false);
    }
  }, [api]);

  useEffect(() => {
    void refreshJobs();
  }, [refreshJobs]);

  useEffect(() => {
    if (!jobs.some((job) => ACTIVE_JOB_STATUSES.has(job.status))) return;
    const timer = window.setInterval(() => void refreshJobs(), 3_000);
    return () => window.clearInterval(timer);
  }, [jobs, refreshJobs]);

  async function openJob(job: Job) {
    setPrimaryView("jobs");
    setSelectedJobId(job.id);
    setApiError(null);
    setPages([]);
    setManifests({});
    setSaveStates({});
    setActivePage(1);
    const hasReviewPages =
      job.status === "ready" || (job.status === "failed" && job.completed_pages > 0);
    if (!hasReviewPages) return;
    setPageLoading(true);
    try {
      const [nextPages, nextManifest] = await Promise.all([
        api.listPages(job.id),
        api.getManifest(job.id, 1),
      ]);
      setPages(nextPages);
      manifestsRef.current = { 1: nextManifest };
      setManifests(manifestsRef.current);
    } catch (error) {
      setApiError(error instanceof Error ? error.message : "Unable to load review");
    } finally {
      setPageLoading(false);
    }
  }

  async function selectPage(pageNumber: number) {
    if (!selectedJob || !["ready", "failed"].includes(selectedJob.status)) return;
    if (manifestsRef.current[pageNumber]) {
      setActivePage(pageNumber);
      return;
    }
    setPageLoading(true);
    try {
      const nextManifest = await api.getManifest(selectedJob.id, pageNumber);
      manifestsRef.current = { ...manifestsRef.current, [pageNumber]: nextManifest };
      setManifests(manifestsRef.current);
      setActivePage(pageNumber);
      setApiError(null);
    } catch (error) {
      setApiError(error instanceof Error ? error.message : "Unable to load page manifest");
    } finally {
      setPageLoading(false);
    }
  }

  async function persistPage(
    jobId: string,
    pageNumber: number,
    regions: RedactionRegion[],
  ) {
    const current = manifestsRef.current[pageNumber];
    if (!current) return;
    setSaveStates((states) => ({ ...states, [pageNumber]: "saving" }));
    try {
      const saved = await api.saveManifest(jobId, pageNumber, current.version, regions);
      const latest = manifestsRef.current[pageNumber];
      manifestsRef.current = {
        ...manifestsRef.current,
        [pageNumber]: latest?.regions === regions
          ? saved
          : { ...saved, regions: latest?.regions ?? saved.regions },
      };
      setManifests(manifestsRef.current);
      setSaveStates((states) => ({ ...states, [pageNumber]: "saved" }));
    } catch {
      setSaveStates((states) => ({ ...states, [pageNumber]: "failed" }));
    }
  }

  function savePage(
    jobId: string,
    pageNumber: number,
    regions: RedactionRegion[],
  ): Promise<void> {
    const previous = saveQueues.current.get(pageNumber) ?? Promise.resolve();
    const next = previous
      .catch(() => undefined)
      .then(() => persistPage(jobId, pageNumber, regions));
    saveQueues.current.set(pageNumber, next);
    return next;
  }

  function handleRegionsChange(pageNumber: number, regions: RedactionRegion[]) {
    if (!selectedJob) return;
    manifestsRef.current = {
      ...manifestsRef.current,
      [pageNumber]: { ...manifestsRef.current[pageNumber], regions },
    };
    setManifests(manifestsRef.current);
    const pending = saveTimers.current.get(pageNumber);
    if (pending) window.clearTimeout(pending);
    setSaveStates((states) => ({ ...states, [pageNumber]: "idle" }));
    const jobId = selectedJob.id;
    saveTimers.current.set(
      pageNumber,
      window.setTimeout(() => void savePage(jobId, pageNumber, regions), 700),
    );
  }

  async function handleUpload(file: File) {
    if (!ACCEPTED_TYPES.has(file.type) || file.size > MAX_FILE_SIZE) {
      setUploadError(
        file.size > MAX_FILE_SIZE
          ? "File exceeds the 100 MB limit."
          : "Choose a PDF, JPEG, or PNG file.",
      );
      setUploadState("failed");
      return;
    }
    const sourceType: SourceType =
      file.type === "application/pdf"
        ? "pdf"
        : file.type === "image/jpeg"
          ? "jpeg"
          : "png";
    const controller = new AbortController();
    uploadController.current = controller;
    setUploadState("uploading");
    setUploadError(null);
    setUploadProgress(0);
    try {
      const created = await api.createJob(sourceType, file.size);
      const completedParts = [];
      for (const part of created.upload_parts) {
        const start = (part.part_number - 1) * UPLOAD_PART_SIZE;
        const body = file.slice(start, Math.min(start + UPLOAD_PART_SIZE, file.size));
        const etag = await uploadMultipartPart(
          part.upload_url,
          body,
          (partProgress) =>
            setUploadProgress(
              Math.round(
                ((part.part_number - 1 + partProgress / 100) /
                  created.upload_parts.length) *
                  100,
              ),
            ),
          controller.signal,
        );
        completedParts.push({ part_number: part.part_number, etag });
      }
      await api.completeUpload(created.job.id, created.upload_id, completedParts);
      setUploadState("complete");
      await refreshJobs();
      setPrimaryView("jobs");
    } catch (error) {
      if (controller.signal.aborted) {
        setUploadState("cancelled");
        setUploadError("Upload cancelled.");
      } else {
        setUploadState("failed");
        setUploadError(error instanceof Error ? error.message : "Upload failed");
      }
    } finally {
      uploadController.current = null;
    }
  }

  async function handleExport() {
    if (!selectedJob || !acknowledged) return;
    try {
      const exporting = await api.confirmExport(selectedJob.id);
      setJobs((current) =>
        current.map((job) => (job.id === exporting.id ? exporting : job)),
      );
      setExportOpen(false);
      setAcknowledged(false);
    } catch (error) {
      setApiError(error instanceof Error ? error.message : "Unable to start export");
    }
  }

  async function retryJob(job: Job) {
    try {
      const retried = await api.retryJob(job.id);
      setJobs((current) => current.map((item) => (item.id === job.id ? retried : item)));
      setApiError(null);
    } catch (error) {
      setApiError(error instanceof Error ? error.message : "Unable to retry job");
    }
  }

  async function downloadJob(job: Job) {
    try {
      const url = await api.authorizeDownload(job.id);
      window.open(url, "_blank", "noopener,noreferrer");
      setApiError(null);
    } catch (error) {
      setApiError(error instanceof Error ? error.message : "Unable to authorize download");
    }
  }

  function showJobs() {
    setPrimaryView("jobs");
    setSelectedJobId("");
  }

  function showUpload() {
    setPrimaryView("upload");
    setSelectedJobId("");
  }

  return (
    <main className="app-shell">
      <header className="topbar">
        <div className="brand">
          <FileText size={28} />
          <span>Redact All The Things</span>
        </div>
        <div className="topbar-actions">
          <span className="system-ok">Secure workspace</span>
          <span>{userLabel}</span>
          <button className="icon-button" onClick={onSignOut} aria-label="Sign out">
            <LogOut size={18} />
          </button>
          <HelpCircle size={20} aria-hidden="true" />
        </div>
      </header>
      <nav className="sidebar">
        <button className={primaryView === "jobs" ? "active" : ""} onClick={showJobs}>
          Jobs
        </button>
        <button className={primaryView === "upload" ? "active" : ""} onClick={showUpload}>
          Upload
        </button>
      </nav>
      <section className="jobs-pane">
        {primaryView === "jobs" ? (
          <>
            <div className="pane-header">
              <h2>Recent Jobs</h2>
              <button
                className="icon-button"
                onClick={() => void refreshJobs()}
                aria-label="Refresh jobs"
              >
                <RotateCw size={18} />
              </button>
            </div>
            <JobTable
              jobs={jobs}
              loading={jobsLoading}
              selected={selectedJob?.id}
              onSelect={(job) => void openJob(job)}
            />
          </>
        ) : (
          <UploadPanel
            onUpload={(file) => void handleUpload(file)}
            onCancel={() => uploadController.current?.abort()}
            progress={uploadProgress}
            state={uploadState}
            error={uploadError}
          />
        )}
        {apiError && <p className="api-error">{apiError}</p>}
      </section>
      {selectedJob && ["ready", "failed"].includes(selectedJob.status) && manifest ? (
        <Editor
          job={selectedJob}
          pages={pages}
          manifest={manifest}
          saveState={saveStates[activePage] ?? "idle"}
          loading={pageLoading}
          onChange={handleRegionsChange}
          onRetrySave={() => void savePage(selectedJob.id, activePage, manifest.regions)}
          onSelectPage={(pageNumber) => void selectPage(pageNumber)}
          onBack={showJobs}
          retryable={Boolean(
            selectedJob.failure_code && RETRYABLE_FAILURES.has(selectedJob.failure_code),
          )}
          onRetryJob={() => void retryJob(selectedJob)}
          onExport={() => setExportOpen(true)}
        />
      ) : selectedJob ? (
        <JobDetail
          job={selectedJob}
          loading={pageLoading}
          retryable={Boolean(
            selectedJob.failure_code && RETRYABLE_FAILURES.has(selectedJob.failure_code),
          )}
          onRetry={() => void retryJob(selectedJob)}
          onDownload={() => void downloadJob(selectedJob)}
          onBack={showJobs}
        />
      ) : (
        <section className="empty-workspace">
          <FileText size={40} />
          <h2>{primaryView === "upload" ? "Choose a document to begin" : "Select a job"}</h2>
          <p>
            {primaryView === "upload"
              ? "PDF, JPEG, and PNG files are supported."
              : "Ready jobs resume in the editor; completed jobs can be downloaded."}
          </p>
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
  loading,
  selected,
  onSelect,
}: {
  jobs: Job[];
  loading: boolean;
  selected?: string;
  onSelect: (job: Job) => void;
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
        {loading && (
          <tr>
            <td colSpan={4} className="empty-row">Loading jobs…</td>
          </tr>
        )}
        {!loading && jobs.length === 0 && (
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
          >
            <td>
              <button className="job-link" onClick={() => onSelect(job)} aria-label={`Open job ${job.id}`}>
                {job.id}
              </button>
            </td>
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
  onCancel,
  progress,
  state,
  error,
}: {
  onUpload: (file: File) => void;
  onCancel: () => void;
  progress: number;
  state: UploadState;
  error: string | null;
}) {
  const inputRef = useRef<HTMLInputElement | null>(null);
  const uploading = state === "uploading";
  return (
    <section className="upload-panel">
      <h2>Upload Document (PDF, JPEG, PNG)</h2>
      <p>Max file size 100 MB · PDF max 200 pages</p>
      <button
        className="dropzone"
        disabled={uploading}
        onClick={() => inputRef.current?.click()}
        onDragOver={(event) => event.preventDefault()}
        onDrop={(event) => {
          event.preventDefault();
          const file = event.dataTransfer.files[0];
          if (file && !uploading) onUpload(file);
        }}
      >
        <CloudUpload size={34} />
        <span>{uploading ? "Uploading…" : "Choose File or drop it here"}</span>
      </button>
      <input
        ref={inputRef}
        type="file"
        accept=".pdf,.jpg,.jpeg,.png,application/pdf,image/jpeg,image/png"
        hidden
        disabled={uploading}
        onChange={(event) => {
          const file = event.target.files?.[0];
          if (file) onUpload(file);
          event.target.value = "";
        }}
      />
      {progress > 0 && (
        <div className="progress" role="progressbar" aria-valuenow={progress}>
          <span style={{ width: `${progress}%` }} />
        </div>
      )}
      {uploading && (
        <button className="danger" onClick={onCancel}>Cancel upload</button>
      )}
      {state === "complete" && <p className="success-text">Upload complete.</p>}
      {error && <p className="error-text" role="alert">{error}</p>}
    </section>
  );
}

function JobDetail({
  job,
  loading,
  retryable,
  onRetry,
  onDownload,
  onBack,
}: {
  job: Job;
  loading: boolean;
  retryable: boolean;
  onRetry: () => void;
  onDownload: () => void;
  onBack: () => void;
}) {
  return (
    <section className="job-detail">
      <button className="text-button" onClick={onBack}>
        <ArrowLeft size={18} /> Back to Jobs
      </button>
      <FileText size={42} />
      <h2>{job.id}</h2>
      <span className={`status ${job.status}`}>{job.status}</span>
      <p>Expires {new Date(job.expires_at).toLocaleString()}</p>
      {loading && <p>Loading review…</p>}
      {job.status === "failed" && (
        <p>{job.failure_code ? `Processing failed: ${job.failure_code}` : "Processing failed."}</p>
      )}
      {job.status === "failed" && retryable && (
        <button className="primary" onClick={onRetry}>Retry job</button>
      )}
      {job.status === "failed" && !retryable && <p>This failure cannot be retried.</p>}
      {job.status === "complete" && (
        <button className="primary" onClick={onDownload}>
          <Download size={18} /> Download redacted file
        </button>
      )}
      {ACTIVE_JOB_STATUSES.has(job.status) && (
        <p>Work continues in the background. This status refreshes automatically.</p>
      )}
      {job.status === "expired" && <p>This job has expired and is no longer accessible.</p>}
    </section>
  );
}

function Editor({
  job,
  pages,
  manifest,
  saveState,
  loading,
  onChange,
  onRetrySave,
  onSelectPage,
  onBack,
  retryable,
  onRetryJob,
  onExport,
}: {
  job: Job;
  pages: PageSummary[];
  manifest: PageManifest;
  saveState: SaveState;
  loading: boolean;
  onChange: (pageNumber: number, regions: RedactionRegion[]) => void;
  onRetrySave: () => void;
  onSelectPage: (pageNumber: number) => void;
  onBack: () => void;
  retryable: boolean;
  onRetryJob: () => void;
  onExport: () => void;
}) {
  const [tool, setTool] = useState<Tool>("select");
  const [histories, setHistories] = useState<Record<number, PageHistory>>({});
  const [selectedId, setSelectedId] = useState(manifest.regions[0]?.id);
  const [zoom, setZoom] = useState(1);
  const [gesture, setGesture] = useState<
    | { kind: "draw"; start: Point; base: RedactionRegion[] }
    | { kind: "move"; start: Point; regionId: string; base: RedactionRegion[] }
    | { kind: "resize"; start: Point; regionId: string; handle: ResizeHandle; base: RedactionRegion[] }
    | null
  >(null);
  const [draftRegions, setDraftRegions] = useState<RedactionRegion[] | null>(null);
  const layerRef = useRef<HTMLDivElement | null>(null);
  const currentPage = pages.find((page) => page.page_number === manifest.page_number);
  const history = histories[manifest.page_number] ?? createHistory(manifest.regions);
  const regions = draftRegions ?? history.present;
  const selected = regions.find((region) => region.id === selectedId);
  const suggestions = regions.filter((region) => region.source === "automatic");

  useEffect(() => {
    setHistories((current) =>
      current[manifest.page_number]
        ? current
        : { ...current, [manifest.page_number]: createHistory(manifest.regions) },
    );
    setSelectedId(manifest.regions[0]?.id);
    setDraftRegions(null);
    setGesture(null);
  }, [manifest.job_id, manifest.page_number]);

  function setHistory(next: PageHistory) {
    setHistories((current) => ({ ...current, [manifest.page_number]: next }));
    onChange(manifest.page_number, next.present);
  }

  function commitRegions(nextRegions: RedactionRegion[]) {
    setHistory(commitHistory(history, nextRegions));
  }

  function deleteRegion() {
    if (!selectedId) return;
    const next = regions.filter((region) => region.id !== selectedId);
    commitRegions(next);
    setSelectedId(next[0]?.id);
  }

  function undo() {
    const next = undoHistory(history);
    if (next !== history) setHistory(next);
  }

  function redo() {
    const next = redoHistory(history);
    if (next !== history) setHistory(next);
  }

  function navigateSuggestion(direction: -1 | 1) {
    if (suggestions.length === 0) return;
    const currentIndex = suggestions.findIndex((region) => region.id === selectedId);
    const nextIndex = (currentIndex + direction + suggestions.length) % suggestions.length;
    setSelectedId(suggestions[nextIndex].id);
  }

  function pointFromEvent(event: ReactPointerEvent): Point {
    const bounds = layerRef.current?.getBoundingClientRect();
    if (!bounds || bounds.width === 0 || bounds.height === 0) return { x: 0, y: 0 };
    return {
      x: Math.min(Math.max((event.clientX - bounds.left) / bounds.width, 0), 1),
      y: Math.min(Math.max((event.clientY - bounds.top) / bounds.height, 0), 1),
    };
  }

  function regionsForGesture(nextPoint: Point): RedactionRegion[] {
    if (!gesture) return regions;
    if (gesture.kind === "draw") {
      return [...gesture.base, regionFromPoints(manifest.page_number, gesture.start, nextPoint)];
    }
    const dx = nextPoint.x - gesture.start.x;
    const dy = nextPoint.y - gesture.start.y;
    return gesture.base.map((region) => {
      if (region.id !== gesture.regionId) return region;
      return gesture.kind === "move"
        ? moveRegion(region, dx, dy)
        : resizeRegion(region, gesture.handle, dx, dy);
    });
  }

  function startDraw(event: ReactPointerEvent<HTMLDivElement>) {
    if (tool !== "draw" || event.target !== event.currentTarget) return;
    const start = pointFromEvent(event);
    setGesture({ kind: "draw", start, base: history.present });
    layerRef.current?.setPointerCapture?.(event.pointerId);
  }

  function startRegionGesture(
    event: ReactPointerEvent,
    regionId: string,
    handle?: ResizeHandle,
  ) {
    event.stopPropagation();
    if (tool !== "select") return;
    setSelectedId(regionId);
    const start = pointFromEvent(event);
    setGesture(
      handle
        ? { kind: "resize", start, regionId, handle, base: history.present }
        : { kind: "move", start, regionId, base: history.present },
    );
    layerRef.current?.setPointerCapture?.(event.pointerId);
  }

  function finishGesture(event: ReactPointerEvent) {
    if (!gesture) return;
    const next = regionsForGesture(pointFromEvent(event));
    const created = gesture.kind === "draw" ? next.at(-1) : undefined;
    setGesture(null);
    setDraftRegions(null);
    commitRegions(next);
    if (created) {
      setSelectedId(created.id);
      setTool("select");
    }
  }

  function handleKeyDown(event: KeyboardEvent<HTMLElement>) {
    const modifier = event.metaKey || event.ctrlKey;
    if (modifier && event.key.toLowerCase() === "z") {
      event.preventDefault();
      event.shiftKey ? redo() : undo();
    } else if (modifier && event.key.toLowerCase() === "y") {
      event.preventDefault();
      redo();
    } else if ((event.key === "Delete" || event.key === "Backspace") && selectedId) {
      event.preventDefault();
      deleteRegion();
    }
  }

  return (
    <section className="editor" onKeyDown={handleKeyDown} tabIndex={-1}>
      <header className="editor-header">
        <button className="text-button" onClick={onBack}>
          <ArrowLeft size={18} /> Back to Jobs
        </button>
        <strong>{job.id}</strong>
        <span className={`status ${job.status}`}>{job.status}</span>
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
        <button onClick={undo} disabled={history.past.length === 0} aria-label="Undo">
          <RotateCcw size={18} /> Undo
        </button>
        <button onClick={redo} disabled={history.future.length === 0} aria-label="Redo">
          <RotateCw size={18} /> Redo
        </button>
        <button onClick={() => navigateSuggestion(-1)} disabled={suggestions.length === 0}>
          Previous suggestion
        </button>
        <button onClick={() => navigateSuggestion(1)} disabled={suggestions.length === 0}>
          Next suggestion
        </button>
        <button
          aria-label="Select all"
          onClick={() => commitRegions(regions.map((region) => ({ ...region, selected: true })))}
        >
          Select all
        </button>
        <button
          aria-label="Deselect all"
          onClick={() => commitRegions(regions.map((region) => ({ ...region, selected: false })))}
        >
          Deselect all
        </button>
        <span className={`autosave ${saveState}`}>
          {saveState === "saving" && <Loader2 size={16} />}
          {saveState === "saved" && <CheckCircle2 size={16} />}
          {saveState === "saving" ? "Saving…" : saveState === "saved" ? "Saved" : "Autosave"}
          {saveState === "failed" && <button onClick={onRetrySave}>Retry save</button>}
        </span>
      </div>
      <aside className="pages-strip">
        <h3>Pages</h3>
        {pages.map((page) => (
          <button
            key={page.page_number}
            className={`thumbnail ${page.page_number === manifest.page_number ? "active" : ""}`}
            onClick={() => onSelectPage(page.page_number)}
            aria-label={`Open page ${page.page_number}`}
          >
            <img src={page.preview_url} alt={`Page ${page.page_number} thumbnail`} />
            <span>{page.page_number}</span>
            <strong>{page.suggestion_count}</strong>
          </button>
        ))}
      </aside>
      <section className="canvas-wrap">
        {loading && <p className="canvas-loading">Loading page…</p>}
        <div className="page-canvas" style={{ transform: `scale(${zoom})` }}>
          {currentPage && <img src={currentPage.preview_url} alt={`Page ${manifest.page_number}`} />}
          <div
            ref={layerRef}
            className={`region-layer ${tool === "draw" ? "drawing" : ""}`}
            role="application"
            aria-label="Redaction canvas"
            onPointerDown={startDraw}
            onPointerMove={(event) => gesture && setDraftRegions(regionsForGesture(pointFromEvent(event)))}
            onPointerUp={finishGesture}
            onPointerCancel={() => {
              setGesture(null);
              setDraftRegions(null);
            }}
          >
            {regions.map((region) => (
              <div
                key={region.id}
                className={`region ${region.id === selectedId ? "selected" : ""}`}
                style={regionStyle(region)}
                role="button"
                tabIndex={0}
                aria-label={`Redaction region ${region.id}`}
                onClick={(event) => {
                  event.stopPropagation();
                  setSelectedId(region.id);
                }}
                onPointerDown={(event) => startRegionGesture(event, region.id)}
              >
                {region.id === selectedId && (["nw", "ne", "sw", "se"] as ResizeHandle[]).map((handle) => (
                  <span
                    key={handle}
                    className={`resize-handle ${handle}`}
                    onPointerDown={(event) => startRegionGesture(event, region.id, handle)}
                  />
                ))}
              </div>
            ))}
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
                  commitRegions(
                    regions.map((region) =>
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
        {job.status === "failed" && (
          <p className="error-text">
            Processing stopped{job.failure_code ? `: ${job.failure_code}` : "."}
          </p>
        )}
        {job.status === "failed" && retryable && (
          <button className="primary" onClick={onRetryJob}>Retry job</button>
        )}
        <button className="primary" onClick={onExport} disabled={job.status !== "ready"}>
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
