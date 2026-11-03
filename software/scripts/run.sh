#!/usr/bin/env bash
# Interactive drive prompt. Ctrl+C or "quit" stops the motors.
set -euo pipefail
cd "$(dirname "$0")/.."
export PYTHONUNBUFFERED=1
exec python3 scripts/drive.py "$@"
