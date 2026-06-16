from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from redact_api.domain import (
    PageManifest,
    RedactionRegion,
    RegionSource,
    save_manifest,
)


NOW = datetime(2026, 6, 15, 12, 0, tzinfo=UTC)


def region(**overrides: object) -> RedactionRegion:
    values: dict[str, object] = {
        "id": "region-1",
        "page_number": 1,
        "x": 0.1,
        "y": 0.2,
        "width": 0.3,
        "height": 0.2,
        "source": RegionSource.AUTOMATIC,
        "category": "EMAIL",
        "confidence": 0.95,
        "selected": True,
    }
    values.update(overrides)
    return RedactionRegion.model_validate(values)


def manifest(**overrides: object) -> PageManifest:
    suggestion = region()
    values: dict[str, object] = {
        "job_id": "job-123",
        "page_number": 1,
        "suggestions": (suggestion,),
        "regions": (suggestion,),
        "version": 1,
        "last_saved_at": NOW,
    }
    values.update(overrides)
    return PageManifest.model_validate(values)


def test_region_serializes_normalized_geometry() -> None:
    payload = region().model_dump(mode="json")

    assert payload["source"] == "automatic"
    assert payload["x"] == 0.1
    assert payload["selected"] is True


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("x", -0.1),
        ("y", float("inf")),
        ("width", 0),
        ("height", -0.1),
        ("confidence", 1.1),
        ("page_number", 0),
    ],
)
def test_region_rejects_invalid_values(field: str, value: object) -> None:
    with pytest.raises(ValidationError):
        region(**{field: value})


def test_region_rejects_geometry_outside_page_bounds() -> None:
    with pytest.raises(ValidationError):
        region(x=0.8, width=0.3)


def test_manifest_requires_automatic_suggestions_on_the_same_page() -> None:
    with pytest.raises(ValidationError):
        manifest(suggestions=(region(source=RegionSource.MANUAL, confidence=None),))

    with pytest.raises(ValidationError):
        manifest(regions=(region(page_number=2),))


def test_manifest_requires_aware_last_save_timestamp() -> None:
    with pytest.raises(ValidationError):
        manifest(last_saved_at=datetime(2026, 6, 15, 12, 0))


def test_save_manifest_preserves_suggestions_and_increments_version() -> None:
    original = manifest()
    manual = region(
        id="manual-1",
        source=RegionSource.MANUAL,
        category="MANUAL",
        confidence=None,
    )

    saved = save_manifest(original, regions=(manual,), now=NOW)

    assert saved.suggestions == original.suggestions
    assert saved.regions == (manual,)
    assert saved.version == 2
    assert saved.last_saved_at == NOW
