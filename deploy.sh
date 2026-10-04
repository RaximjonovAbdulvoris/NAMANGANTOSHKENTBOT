#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
# Export credentials in your hosting environment before invoking this script.
# It does not stop an existing bot service or start a second background process.
exec "${PYTHON_BIN:-python}" -m bot.main
