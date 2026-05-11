#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR/backend"

HOST="${HOST:-127.0.0.1}"
PORT="${PORT:-8000}"
RELOAD="${RELOAD:-true}"

if [ "$RELOAD" = "true" ]; then
  exec uvicorn main:app --host "$HOST" --port "$PORT" --reload
else
  exec uvicorn main:app --host "$HOST" --port "$PORT"
fi
