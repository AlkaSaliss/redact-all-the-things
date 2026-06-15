import json
from pathlib import Path

from redact_api.domain import Job, PageManifest, WorkerSubmission


FIXTURES = Path(__file__).parents[1] / "fixtures"


def load(name: str) -> object:
    return json.loads((FIXTURES / name).read_text())


def test_shared_job_fixtures_match_the_contract() -> None:
    assert Job.model_validate(load("job.json")).status.value == "ready"
    assert Job.model_validate(load("failed-job.json")).status.value == "failed"


def test_shared_manifest_and_worker_fixtures_match_the_contract() -> None:
    assert PageManifest.model_validate(load("page-manifest.json")).version == 1
    assert (
        WorkerSubmission.model_validate(load("worker-request.json")).mode.value
        == "analyze"
    )
