#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if ! command -v uvicorn >/dev/null 2>&1; then
  echo "uvicorn not found. Run scripts/setup_backend.sh first."
  exit 1
fi

if ! command -v npm >/dev/null 2>&1; then
  echo "npm not found. Install Node.js first."
  exit 1
fi

echo "Starting backend and frontend..."
"$ROOT_DIR/scripts/run_backend.sh" &
BACKEND_PID=$!

cleanup() {
  echo "Stopping services..."
  kill "$BACKEND_PID" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

"$ROOT_DIR/scripts/run_frontend.sh"
