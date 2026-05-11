#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "======================================"
echo "  Stock Price Prediction - Launcher"
echo "======================================"

# --- Check Node ---
if ! command -v npm >/dev/null 2>&1; then
  echo "[ERROR] npm not found. Install Node.js from https://nodejs.org"
  exit 1
fi

# --- Check Python ---
if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN="python"
else
  echo "[ERROR] Python not found. Install Python from https://python.org"
  exit 1
fi

echo "[INFO] Using Python: $($PYTHON_BIN --version)"
echo "[INFO] Using Node: $(node --version)"

# --- Install Python deps from ROOT (requirements.txt is at root) ---
echo ""
echo "[STEP 1] Installing Python dependencies from root requirements.txt..."
cd "$ROOT_DIR"
"$PYTHON_BIN" -m pip install -r requirements.txt --quiet

# --- Install Frontend deps ---
echo ""
echo "[STEP 2] Installing frontend dependencies..."
cd "$ROOT_DIR/frontend"
if [ ! -d node_modules ]; then
  npm install
else
  echo "  node_modules already present, skipping npm install"
fi

# --- Create .env for frontend if missing ---
if [ ! -f "$ROOT_DIR/frontend/.env" ]; then
  echo "VITE_API_BASE_URL=http://127.0.0.1:8000/api" > "$ROOT_DIR/frontend/.env"
  echo "[INFO] Created frontend/.env with default API URL"
fi

# --- Create backend cache dir if missing ---
mkdir -p "$ROOT_DIR/backend/cache"
mkdir -p "$ROOT_DIR/backend/saved_models"

# --- Start Backend ---
echo ""
echo "[STEP 3] Starting backend on http://127.0.0.1:8000 ..."
cd "$ROOT_DIR/backend"
"$PYTHON_BIN" -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload &
BACKEND_PID=$!

# --- Wait for backend to be ready ---
echo "[INFO] Waiting for backend to start..."
for i in {1..15}; do
  if curl -s http://127.0.0.1:8000/ >/dev/null 2>&1; then
    echo "[OK] Backend is up!"
    break
  fi
  sleep 1
done

# --- Start Frontend ---
echo ""
echo "[STEP 4] Starting frontend on http://localhost:5173 ..."
cd "$ROOT_DIR/frontend"
npm run dev &
FRONTEND_PID=$!

echo ""
echo "======================================"
echo "  Both servers are running!"
echo "  Backend:  http://127.0.0.1:8000"
echo "  Frontend: http://localhost:5173"
echo "  Press Ctrl+C to stop both"
echo "======================================"

# --- Cleanup on exit ---
cleanup() {
  echo ""
  echo "[INFO] Shutting down..."
  kill "$BACKEND_PID" 2>/dev/null || true
  kill "$FRONTEND_PID" 2>/dev/null || true
  echo "[INFO] Done."
}
trap cleanup EXIT INT TERM

# Keep script alive
wait $FRONTEND_PID
