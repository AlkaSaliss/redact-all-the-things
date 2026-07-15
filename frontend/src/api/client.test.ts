import { describe, expect, it, vi } from "vitest";
import { RedactionApiClient, uploadMultipartPart } from "./client";

describe("RedactionApiClient", () => {
  it("maps manifest saves to the backend contract", async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ version: 2, regions: [] }),
    });
    vi.stubGlobal("fetch", fetchMock);
    const client = new RedactionApiClient("https://api.example", async () => "token");

    await client.saveManifest("job-1", 1, 1, []);

    expect(fetchMock).toHaveBeenCalledWith(
      "https://api.example/jobs/job-1/pages/1/manifest",
      expect.objectContaining({
        method: "PUT",
        body: JSON.stringify({ version: 1, regions: [] }),
        headers: expect.objectContaining({ authorization: "Bearer token" }),
      }),
    );
  });

  it("maps retry and download authorization to existing routes", async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce({ ok: true, json: async () => ({ status: "queued" }) })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ download_url: "https://download.example/output" }),
      });
    vi.stubGlobal("fetch", fetchMock);
    const client = new RedactionApiClient("https://api.example", async () => "token");

    await client.retryJob("job-1");
    await expect(client.authorizeDownload("job-1")).resolves.toBe(
      "https://download.example/output",
    );

    expect(fetchMock).toHaveBeenNthCalledWith(
      1,
      "https://api.example/jobs/job-1/retry",
      expect.objectContaining({ method: "POST" }),
    );
  });

  it("passes an abort signal to the direct upload", async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      headers: new Headers({ etag: "part-etag" }),
    });
    vi.stubGlobal("fetch", fetchMock);
    const controller = new AbortController();

    await uploadMultipartPart(
      "https://upload.example/part",
      new File(["pdf"], "file.pdf", { type: "application/pdf" }),
      vi.fn(),
      controller.signal,
    );

    expect(fetchMock).toHaveBeenCalledWith(
      "https://upload.example/part",
      expect.objectContaining({ signal: controller.signal }),
    );
  });
});
