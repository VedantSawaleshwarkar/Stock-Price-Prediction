#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

PYTHON_BIN="${PYTHON_BIN:-python3}"
if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  if command -v python >/dev/null 2>&1; then
    PYTHON_BIN="python"
  else
    echo "Python is not installed or not on PATH."
    exit 1
  fi
fi

echo "Using Python: $PYTHON_BIN"
"$PYTHON_BIN" -m venv .venv

if [ -f ".venv/bin/activate" ]; then
  # Linux/macOS
  # shellcheck disable=SC1091
  source .venv/bin/activate
else
  echo "Virtual env created. On Windows, activate manually with:"
  echo "  .venv\\Scripts\\activate"
fi

"$PYTHON_BIN" -m pip install --upgrade pip
"$PYTHON_BIN" -m pip install -r requirements.txt

echo "Backend setup completed."
