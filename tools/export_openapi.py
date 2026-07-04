"""Export the FastAPI OpenAPI contract for frontend type checks."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from redact_api.http import create_app


def main() -> None:
    app = create_app(object())  # type: ignore[arg-type]
    print(json.dumps(app.openapi(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
