## Context

The analysis worker already writes raster page artifacts, OCR artifacts, and
page manifests. The control-plane API already manages jobs, upload completion,
manifest saves, export submission, retry, and download authorization. The
missing product slice is the browser review workflow and render-mode export
that consume those artifacts.

## Decisions

### Default frontend runtime targets the dev AWS stack

The frontend uses fixtures for tests and empty-state resilience, but local
`npm run dev` expects `VITE_*` values from the real AWS dev stack. This keeps
runtime behavior aligned with Cognito Hosted UI and API Gateway JWT
authorization instead of making fixture mode the default.

### Preview images use presigned page artifact URLs

The API returns owner-checked, short-lived URLs for existing raster page
artifacts. This avoids Lambda image proxy bandwidth while preserving private S3
object ownership boundaries.

### Editor geometry stays normalized

The frontend renders page images with an SVG/CSS overlay and stores only the
existing normalized region contract. No PDF viewer or canvas editing library is
introduced because all review/export behavior is rectangle-based.

### Render mode consumes saved manifests

The render worker reads raster page artifacts and current page manifests,
burns selected regions into pixels, and serializes raster-only PDF/image
outputs. PDF text layers, annotations, and metadata are not copied because the
output is rebuilt from pixels.

## Risks

- Combined scope is large and crosses backend, frontend, infrastructure, and
  docs. Verification must be broad.
- Hosted UI callback/logout URLs depend on deployed CloudFront and localhost
  origins; incorrect stack outputs will block browser sign-in.
- Re-OCR export checks can be slow, so heavy OCR smoke coverage is kept marked
  separately from fast CI tests.
