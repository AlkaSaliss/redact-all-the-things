import { describe, expect, it, vi } from "vitest";
import { RedactionApiClient } from "./client";

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
});
