#!/usr/bin/env bash
set -euo pipefail

"$(dirname "$0")/check_floci.sh"

cat <<'EOF'
Floci endpoint smoke check passed.

App edge/auth/API resources are modeled in Terraform. Floci smoke coverage is
limited to services supported by the local emulator; CloudFront, Cognito, API
Gateway, and Lambda compatibility must be treated as static validation unless
the configured Floci endpoint supports those services.
EOF
