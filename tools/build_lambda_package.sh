#!/usr/bin/env bash
set -euo pipefail

package_path="${1:-.build/control-plane-lambda.zip}"
build_root=".build/lambda-control-plane"
package_dir="${build_root}/package"

rm -rf "$build_root"
mkdir -p "$package_dir" "$(dirname "$package_path")"

uv pip install \
  --target "$package_dir" \
  --python-platform x86_64-manylinux2014 \
  --python-version 3.12 \
  --only-binary=:all: \
  boto3==1.43.29 \
  fastapi==0.137.1 \
  mangum==0.21.0 \
  pydantic==2.13.4

cp -R src/redact_api "$package_dir/redact_api"

python - "$package_dir" "$package_path" <<'PY'
import os
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile
import sys

package_dir = Path(sys.argv[1])
package_path = Path(sys.argv[2])
fixed_timestamp = 315532800

for path in package_dir.rglob("*"):
    if path.is_file():
        path.chmod(0o644)
        os.utime(path, (fixed_timestamp, fixed_timestamp))

with ZipFile(package_path, "w", ZIP_DEFLATED) as archive:
    for path in sorted(package_dir.rglob("*")):
        if path.is_file():
            if "__pycache__" in path.parts or path.suffix == ".pyc":
                continue

            archive.write(path, path.relative_to(package_dir))
PY

echo "Built Lambda package at ${package_path}"
