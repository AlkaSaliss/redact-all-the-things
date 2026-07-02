#!/usr/bin/env bash
set -euo pipefail

if [[ -z "${FLOCI_ENDPOINT_URL:-}" ]]; then
  echo "FLOCI_ENDPOINT_URL is required, for example http://127.0.0.1:4566" >&2
  exit 2
fi

if ! command -v curl >/dev/null 2>&1; then
  echo "curl is required to check the Floci endpoint" >&2
  exit 2
fi

status="$(
  curl --connect-timeout 2 --max-time 5 --silent --show-error \
    --output /dev/null --write-out "%{http_code}" \
    "${FLOCI_ENDPOINT_URL}" || true
)"

if [[ "${status}" == "000" ]]; then
  echo "Floci endpoint is not reachable at ${FLOCI_ENDPOINT_URL}" >&2
  exit 1
fi

echo "Floci endpoint responded with HTTP ${status}: ${FLOCI_ENDPOINT_URL}"
