import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";
import type { RedactionApiClient } from "./api/client";
import { Workspace } from "./App";
import type { Job, PageManifest, PageSummary } from "./contracts/types";

const expiresAt = "2026-07-16T12:00:00Z";

function job(id: string, status: Job["status"], failureCode: string | null = null): Job {
  return {
    id,
    owner_id: "user-1",
    source_type: "pdf",
    source_key: `${id}/source.pdf`,
    output_key: `${id}/output.pdf`,
    status,
    page_count: status === "ready" ? 2 : 1,
    completed_pages: status === "ready" ? 2 : 1,
    created_at: "2026-07-15T12:00:00Z",
    expires_at: expiresAt,
    model_versions: {},
    failure_code: failureCode,
    version: 1,
  };
}

const jobs = [
  job("ready-job", "ready"),
  job("complete-job", "complete"),
  job("failed-job", "failed", "analyze_transient"),
];
const pages: PageSummary[] = [1, 2].map((pageNumber) => ({
  page_number: pageNumber,
  width: 1000,
  height: 1400,
  suggestion_count: 1,
  selected_count: 1,
  manifest_version: 1,
  preview_url: `https://preview.example/page-${pageNumber}.png`,
}));

function manifest(pageNumber: number): PageManifest {
  return {
    job_id: "ready-job",
    page_number: pageNumber,
    suggestions: [],
    regions: Array.from({ length: pageNumber }, (_, index) =>
      ({
        id: `region-${pageNumber}-${index}`,
        page_number: pageNumber,
        x: 0.1,
        y: 0.1 + index * 0.2,
        width: 0.2,
        height: 0.1,
        source: "automatic",
        category: index === 0 ? "person" : "email",
        confidence: 0.9,
        selected: true,
      }),
    ),
    version: 1,
    last_saved_at: "2026-07-15T12:00:00Z",
  };
}

function mockApi() {
  return {
    listJobs: vi.fn().mockResolvedValue(jobs),
    listPages: vi.fn().mockResolvedValue(pages),
    getManifest: vi.fn((_jobId: string, pageNumber: number) =>
      Promise.resolve(manifest(pageNumber)),
    ),
    saveManifest: vi.fn(
      (_jobId: string, pageNumber: number, version: number, regions: PageManifest["regions"]) =>
        Promise.resolve({ ...manifest(pageNumber), version: version + 1, regions }),
    ),
    authorizeDownload: vi.fn().mockResolvedValue("https://download.example/output.pdf"),
    confirmExport: vi.fn().mockResolvedValue(job("ready-job", "exporting")),
    retryJob: vi.fn(),
    createJob: vi.fn(),
    completeUpload: vi.fn(),
  } as unknown as RedactionApiClient;
}

afterEach(() => {
  vi.restoreAllMocks();
  vi.unstubAllGlobals();
});

describe("Workspace", () => {
  it("navigates primary views and loads page-specific manifests", async () => {
    const api = mockApi();
    const user = userEvent.setup();
    render(<Workspace api={api} userLabel="Ada" onSignOut={vi.fn()} />);

    await screen.findByText("ready-job");
    await user.click(screen.getByRole("button", { name: "Upload" }));
    expect(screen.getByRole("heading", { name: /Upload Document/ })).toBeInTheDocument();
    await user.click(screen.getByRole("button", { name: "Jobs" }));
    await user.click(screen.getByRole("button", { name: "Open job ready-job" }));
    await screen.findByRole("img", { name: "Page 1" });
    await user.click(screen.getByRole("button", { name: "Open page 2" }));

    expect(await screen.findByRole("img", { name: "Page 2" })).toBeInTheDocument();
    expect(api.getManifest).toHaveBeenCalledWith("ready-job", 2);
    await user.click(screen.getByRole("button", { name: "Next suggestion" }));
    expect(screen.getByText("email")).toBeInTheDocument();
    await user.click(screen.getByRole("button", { name: "Back to Jobs" }));
    expect(screen.getByRole("heading", { name: "Recent Jobs" })).toBeInTheDocument();
  });

  it("supports selection history and autosaves current page edits", async () => {
    const api = mockApi();
    const user = userEvent.setup();
    render(<Workspace api={api} userLabel="Ada" onSignOut={vi.fn()} />);

    await user.click(await screen.findByRole("button", { name: "Open job ready-job" }));
    await screen.findByRole("img", { name: "Page 1" });
    await user.click(screen.getByRole("button", { name: "Deselect all" }));
    expect(screen.getByRole("checkbox", { name: "Selected" })).not.toBeChecked();
    await user.click(screen.getByRole("button", { name: "Undo" }));
    expect(screen.getByRole("checkbox", { name: "Selected" })).toBeChecked();
    await user.click(screen.getByRole("button", { name: "Redo" }));

    await waitFor(() => expect(api.saveManifest).toHaveBeenCalled());
    expect(api.saveManifest).toHaveBeenLastCalledWith(
      "ready-job",
      1,
      expect.any(Number),
      expect.arrayContaining([expect.objectContaining({ selected: false })]),
    );
  });

  it("draws a pointer-defined region and can undo it", async () => {
    const api = mockApi();
    const user = userEvent.setup();
    render(<Workspace api={api} userLabel="Ada" onSignOut={vi.fn()} />);

    await user.click(await screen.findByRole("button", { name: "Open job ready-job" }));
    const canvas = await screen.findByRole("application", { name: "Redaction canvas" });
    vi.spyOn(canvas, "getBoundingClientRect").mockReturnValue({
      x: 0,
      y: 0,
      left: 0,
      top: 0,
      right: 1000,
      bottom: 1000,
      width: 1000,
      height: 1000,
      toJSON: () => ({}),
    });
    await user.click(screen.getByRole("button", { name: "Draw Rectangle" }));
    fireEvent.pointerDown(canvas, { pointerId: 1, clientX: 200, clientY: 300 });
    fireEvent.pointerMove(canvas, { pointerId: 1, clientX: 600, clientY: 500 });
    fireEvent.pointerUp(canvas, { pointerId: 1, clientX: 600, clientY: 500 });

    expect(screen.getAllByRole("button", { name: /Redaction region/ })).toHaveLength(2);
    fireEvent.keyDown(canvas, { key: "z", ctrlKey: true });
    expect(screen.getAllByRole("button", { name: /Redaction region/ })).toHaveLength(1);
    fireEvent.keyDown(canvas, { key: "y", ctrlKey: true });
    expect(screen.getAllByRole("button", { name: /Redaction region/ })).toHaveLength(2);
  });

  it("authorizes and opens completed downloads", async () => {
    const api = mockApi();
    const open = vi.spyOn(window, "open").mockImplementation(() => null);
    const user = userEvent.setup();
    render(<Workspace api={api} userLabel="Ada" onSignOut={vi.fn()} />);

    await user.click(await screen.findByRole("button", { name: "Open job complete-job" }));
    await user.click(screen.getByRole("button", { name: "Download redacted file" }));

    expect(api.authorizeDownload).toHaveBeenCalledWith("complete-job");
    expect(open).toHaveBeenCalledWith(
      "https://download.example/output.pdf",
      "_blank",
      "noopener,noreferrer",
    );
  });

  it("retains failed autosave edits and retries them", async () => {
    const api = mockApi();
    vi.mocked(api.saveManifest)
      .mockRejectedValueOnce(new Error("version conflict"))
      .mockImplementationOnce(
        async (_jobId, pageNumber, version, regions) => ({
          ...manifest(pageNumber),
          version: version + 1,
          regions,
        }),
      );
    const user = userEvent.setup();
    render(<Workspace api={api} userLabel="Ada" onSignOut={vi.fn()} />);

    await user.click(await screen.findByRole("button", { name: "Open job ready-job" }));
    await user.click(await screen.findByRole("button", { name: "Deselect all" }));
    await user.click(await screen.findByRole("button", { name: "Retry save" }));

    await waitFor(() => expect(api.saveManifest).toHaveBeenCalledTimes(2));
    expect(api.saveManifest).toHaveBeenLastCalledWith(
      "ready-job",
      1,
      1,
      expect.arrayContaining([expect.objectContaining({ selected: false })]),
    );
  });

  it("cancels an active upload and reports invalid files", async () => {
    const api = mockApi();
    vi.mocked(api.createJob).mockResolvedValue({
      job: job("upload-job", "uploading"),
      upload_id: "upload-1",
      upload_parts: [{ part_number: 1, upload_url: "https://upload.example/part" }],
    });
    vi.stubGlobal(
      "fetch",
      vi.fn((_url: string, init?: RequestInit) =>
        new Promise((_resolve, reject) => {
          init?.signal?.addEventListener("abort", () =>
            reject(new DOMException("aborted", "AbortError")),
          );
        }),
      ),
    );
    const user = userEvent.setup();
    const { container } = render(
      <Workspace api={api} userLabel="Ada" onSignOut={vi.fn()} />,
    );

    await user.click(screen.getByRole("button", { name: "Upload" }));
    const input = container.querySelector('input[type="file"]') as HTMLInputElement;
    fireEvent.change(input, {
      target: { files: [new File(["pdf"], "document.pdf", { type: "application/pdf" })] },
    });
    await user.click(await screen.findByRole("button", { name: "Cancel upload" }));
    expect(await screen.findByRole("alert")).toHaveTextContent("Upload cancelled");

    const invalid = new File(["text"], "notes.txt", { type: "text/plain" });
    fireEvent.change(input, { target: { files: [invalid] } });
    expect(await screen.findByRole("alert")).toHaveTextContent("PDF, JPEG, or PNG");
  });

  it("uploads every API-provided part and completes with ordered etags", async () => {
    const api = mockApi();
    vi.mocked(api.createJob).mockResolvedValue({
      job: job("upload-job", "uploading"),
      upload_id: "upload-1",
      upload_parts: [
        { part_number: 1, upload_url: "https://upload.example/part-1" },
        { part_number: 2, upload_url: "https://upload.example/part-2" },
      ],
    });
    vi.mocked(api.completeUpload).mockResolvedValue(job("upload-job", "queued"));
    vi.stubGlobal(
      "fetch",
      vi
        .fn()
        .mockResolvedValueOnce({ ok: true, headers: new Headers({ etag: "etag-1" }) })
        .mockResolvedValueOnce({ ok: true, headers: new Headers({ etag: "etag-2" }) }),
    );
    const user = userEvent.setup();
    const { container } = render(
      <Workspace api={api} userLabel="Ada" onSignOut={vi.fn()} />,
    );

    await user.click(screen.getByRole("button", { name: "Upload" }));
    const input = container.querySelector('input[type="file"]') as HTMLInputElement;
    fireEvent.change(input, {
      target: {
        files: [
          new File([new Uint8Array(5 * 1024 * 1024 + 1)], "document.pdf", {
            type: "application/pdf",
          }),
        ],
      },
    });

    await waitFor(() =>
      expect(api.completeUpload).toHaveBeenCalledWith("upload-job", "upload-1", [
        { part_number: 1, etag: "etag-1" },
        { part_number: 2, etag: "etag-2" },
      ]),
    );
    expect(screen.getByRole("heading", { name: "Recent Jobs" })).toBeInTheDocument();
  });

  it("requires acknowledgement before starting export", async () => {
    const api = mockApi();
    const user = userEvent.setup();
    render(<Workspace api={api} userLabel="Ada" onSignOut={vi.fn()} />);

    await user.click(await screen.findByRole("button", { name: "Open job ready-job" }));
    await user.click(await screen.findByRole("button", { name: "Review & Export" }));
    const confirm = screen.getAllByRole("button", { name: "Review & Export" }).at(-1)!;
    expect(confirm).toBeDisabled();
    await user.click(
      screen.getByRole("checkbox", { name: /I have reviewed the document/ }),
    );
    await user.click(confirm);

    expect(api.confirmExport).toHaveBeenCalledWith("ready-job");
  });

  it("retries an eligible failed job", async () => {
    const api = mockApi();
    vi.mocked(api.retryJob).mockResolvedValue(job("failed-job", "queued"));
    const user = userEvent.setup();
    render(<Workspace api={api} userLabel="Ada" onSignOut={vi.fn()} />);

    await user.click(await screen.findByRole("button", { name: "Open job failed-job" }));
    await user.click(screen.getByRole("button", { name: "Retry job" }));

    expect(api.retryJob).toHaveBeenCalledWith("failed-job");
    expect((await screen.findAllByText("queued")).length).toBeGreaterThan(0);
  });
});
