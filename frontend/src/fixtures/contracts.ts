import type { Job, PageManifest, PageSummary } from "../contracts/types";

export const fixtureJobs: Job[] = [
  {
    id: "employee-file",
    owner_id: "fixture-user",
    source_type: "pdf",
    source_key: "users/fixture-user/jobs/employee-file/source",
    output_key: "users/fixture-user/jobs/employee-file/output",
    status: "ready",
    page_count: 18,
    completed_pages: 18,
    created_at: "2026-07-04T10:00:00Z",
    expires_at: "2026-07-05T10:00:00Z",
    model_versions: { ocr: "fixture", pii: "fixture" },
    failure_code: null,
    version: 4,
  },
];

export const fixturePages: PageSummary[] = [
  {
    page_number: 1,
    width: 850,
    height: 1100,
    suggestion_count: 7,
    selected_count: 7,
    manifest_version: 1,
    preview_url:
      "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='850' height='1100'%3E%3Crect width='850' height='1100' fill='white'/%3E%3Ctext x='160' y='150' font-size='42'%3EEMPLOYEE INFORMATION FORM%3C/text%3E%3Ctext x='160' y='250' font-size='28'%3EFull Name:%3C/text%3E%3Ctext x='160' y='330' font-size='28'%3EDate of Birth:%3C/text%3E%3Ctext x='160' y='410' font-size='28'%3ESocial Security Number:%3C/text%3E%3Ctext x='160' y='490' font-size='28'%3EEmail Address:%3C/text%3E%3C/svg%3E",
  },
];

export const fixtureManifest: PageManifest = {
  job_id: "employee-file",
  page_number: 1,
  suggestions: [],
  regions: [
    {
      id: "pii-1",
      page_number: 1,
      x: 0.45,
      y: 0.2,
      width: 0.18,
      height: 0.035,
      source: "automatic",
      category: "full_name",
      confidence: 0.96,
      selected: true,
    },
    {
      id: "pii-2",
      page_number: 1,
      x: 0.45,
      y: 0.28,
      width: 0.22,
      height: 0.035,
      source: "automatic",
      category: "date_of_birth",
      confidence: 0.92,
      selected: true,
    },
  ],
  version: 1,
  last_saved_at: "2026-07-04T10:05:00Z",
};
