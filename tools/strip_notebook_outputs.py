"""Strip execution output from Jupyter notebooks before commit."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def strip_notebook(path: Path) -> bool:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    original = json.dumps(notebook, sort_keys=True, separators=(",", ":"))

    for cell in notebook.get("cells", []):
        if cell.get("cell_type") == "code":
            cell["execution_count"] = None
            cell["outputs"] = []

    metadata = notebook.get("metadata")
    if isinstance(metadata, dict):
        metadata.pop("widgets", None)

    stripped = json.dumps(notebook, sort_keys=True, separators=(",", ":"))
    if stripped == original:
        return False

    path.write_text(json.dumps(notebook, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return True


def main(argv: list[str]) -> int:
    changed: list[Path] = []
    invalid: list[tuple[Path, Exception]] = []

    for raw_path in argv:
        path = Path(raw_path)
        try:
            if strip_notebook(path):
                changed.append(path)
        except (OSError, json.JSONDecodeError, TypeError) as exc:
            invalid.append((path, exc))

    for path, exc in invalid:
        print(f"{path}: {exc}", file=sys.stderr)
    for path in changed:
        print(f"stripped notebook outputs: {path}", file=sys.stderr)

    return 1 if changed or invalid else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
