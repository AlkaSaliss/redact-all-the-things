import type {
  CreateJobResponse,
  Job,
  PageManifest,
  PageSummary,
  RedactionRegion,
  SourceType,
} from "../contracts/types";

export class ApiError extends Error {
  constructor(
    message: string,
    public readonly status: number,
  ) {
    super(message);
  }
}

export class RedactionApiClient {
  constructor(
    private readonly baseUrl: string,
    private readonly accessToken: () => Promise<string>,
  ) {}

  async listJobs(): Promise<Job[]> {
    return this.request<Job[]>("/jobs");
  }

  async createJob(
    sourceType: SourceType,
    sizeBytes: number,
  ): Promise<CreateJobResponse> {
    return this.request<CreateJobResponse>("/jobs", {
      method: "POST",
      body: JSON.stringify({ source_type: sourceType, size_bytes: sizeBytes }),
    });
  }

  async completeUpload(
    jobId: string,
    uploadId: string,
    parts: Array<{ part_number: number; etag: string }>,
  ): Promise<Job> {
    return this.request<Job>(`/jobs/${jobId}/upload-complete`, {
      method: "POST",
      body: JSON.stringify({ upload_id: uploadId, parts }),
    });
  }

  async listPages(jobId: string): Promise<PageSummary[]> {
    return this.request<PageSummary[]>(`/jobs/${jobId}/pages`);
  }

  async getManifest(
    jobId: string,
    pageNumber: number,
  ): Promise<PageManifest> {
    return this.request<PageManifest>(
      `/jobs/${jobId}/pages/${pageNumber}/manifest`,
    );
  }

  async saveManifest(
    jobId: string,
    pageNumber: number,
    version: number,
    regions: RedactionRegion[],
  ): Promise<PageManifest> {
    return this.request<PageManifest>(
      `/jobs/${jobId}/pages/${pageNumber}/manifest`,
      {
        method: "PUT",
        body: JSON.stringify({ version, regions }),
      },
    );
  }

  async confirmExport(jobId: string): Promise<Job> {
    return this.request<Job>(`/jobs/${jobId}/export`, {
      method: "POST",
      body: JSON.stringify({ acknowledged: true }),
    });
  }

  async authorizeDownload(jobId: string): Promise<string> {
    const response = await this.request<{ download_url: string }>(
      `/jobs/${jobId}/download`,
    );
    return response.download_url;
  }

  private async request<T>(
    path: string,
    init: RequestInit = {},
  ): Promise<T> {
    const token = await this.accessToken();
    const response = await fetch(`${this.baseUrl}${path}`, {
      ...init,
      headers: {
        "content-type": "application/json",
        authorization: `Bearer ${token}`,
        ...init.headers,
      },
    });
    if (!response.ok) {
      throw new ApiError(await response.text(), response.status);
    }
    return response.json() as Promise<T>;
  }
}

export async function uploadMultipartPart(
  url: string,
  file: File,
  onProgress: (progress: number) => void,
): Promise<string> {
  onProgress(0);
  const response = await fetch(url, {
    method: "PUT",
    body: file,
  });
  if (!response.ok) {
    throw new ApiError("upload failed", response.status);
  }
  onProgress(100);
  return response.headers.get("etag") ?? "";
}
