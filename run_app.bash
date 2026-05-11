#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if ! command -v npm >/dev/null 2>&1; then
  echo "npm not found. Install Node.js first."
  exit 1
fi

if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN="python"
else
  echo "Python not found. Install Python first."
  exit 1
fi

echo "Starting backend on http://127.0.0.1:8000 ..."
(
  cd "$ROOT_DIR/backend"
  "$PYTHON_BIN" -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
) &
BACKEND_PID=$!

cleanup() {
  echo "Stopping backend (PID: $BACKEND_PID)"
  kill "$BACKEND_PID" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

echo "Starting frontend on http://localhost:5173 ..."
cd "$ROOT_DIR/frontend"

if [ ! -d node_modules ]; then
  npm install
fi

npm run dev
