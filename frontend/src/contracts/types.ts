export type SourceType = "pdf" | "jpeg" | "png";
export type JobStatus =
  | "uploading"
  | "queued"
  | "analyzing"
  | "ready"
  | "exporting"
  | "complete"
  | "failed"
  | "expired";

export type RegionSource = "automatic" | "manual";

export interface Job {
  id: string;
  owner_id: string;
  source_type: SourceType;
  source_key: string;
  output_key: string;
  status: JobStatus;
  page_count: number;
  completed_pages: number;
  created_at: string;
  expires_at: string;
  model_versions: Record<string, string>;
  failure_code: string | null;
  version: number;
}

export interface RedactionRegion {
  id: string;
  page_number: number;
  x: number;
  y: number;
  width: number;
  height: number;
  source: RegionSource;
  category: string;
  confidence: number | null;
  selected: boolean;
}

export interface PageManifest {
  job_id: string;
  page_number: number;
  suggestions: RedactionRegion[];
  regions: RedactionRegion[];
  version: number;
  last_saved_at: string;
}

export interface PageSummary {
  page_number: number;
  width: number;
  height: number;
  suggestion_count: number;
  selected_count: number;
  manifest_version: number;
  preview_url: string;
}

export interface CreateJobResponse {
  job: Job;
  upload_id: string;
  upload_parts: Array<{ part_number: number; upload_url: string }>;
}
