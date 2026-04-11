#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY_SCRIPT="$SCRIPT_DIR/search_dorks.py"

# Prefer nearby venvs, then fall back to python3/python.
if [[ -x "$SCRIPT_DIR/../.venv/bin/python" ]]; then
  PYTHON_BIN="$SCRIPT_DIR/../.venv/bin/python"
elif [[ -x "$SCRIPT_DIR/../../../.venv/bin/python" ]]; then
  PYTHON_BIN="$SCRIPT_DIR/../../../.venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="$(command -v python3)"
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN="$(command -v python)"
else
  echo "Error: no Python interpreter found (python3/python)." >&2
  exit 127
fi

exec "$PYTHON_BIN" "$PY_SCRIPT" "$@"
