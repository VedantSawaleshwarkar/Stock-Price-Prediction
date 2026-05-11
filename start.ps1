Write-Host "======================================" -ForegroundColor Cyan
Write-Host "  Stock Price Prediction - Launcher" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan

$ROOT = Split-Path -Parent $MyInvocation.MyCommand.Path

# Check Python
try { python --version | Out-Null } catch {
    Write-Host "[ERROR] Python not found." -ForegroundColor Red; exit 1
}

# Check npm
try { npm --version | Out-Null } catch {
    Write-Host "[ERROR] npm not found." -ForegroundColor Red; exit 1
}

# Install deps
Write-Host "`n[STEP 1] Installing Python dependencies..." -ForegroundColor Yellow
Set-Location $ROOT
python -m pip install -r requirements.txt --quiet

# Create dirs
New-Item -ItemType Directory -Force -Path "$ROOT\backend\cache" | Out-Null
New-Item -ItemType Directory -Force -Path "$ROOT\backend\saved_models" | Out-Null

# Frontend .env
if (-not (Test-Path "$ROOT\frontend\.env")) {
    "VITE_API_BASE_URL=http://127.0.0.1:8000/api" | Out-File "$ROOT\frontend\.env" -Encoding utf8
    Write-Host "[INFO] Created frontend/.env" -ForegroundColor Green
}

# npm install
Write-Host "`n[STEP 2] Installing frontend dependencies..." -ForegroundColor Yellow
Set-Location "$ROOT\frontend"
if (-not (Test-Path "node_modules")) { npm install }

# Start backend
Write-Host "`n[STEP 3] Starting backend..." -ForegroundColor Yellow
Set-Location "$ROOT\backend"
Start-Process "cmd" -ArgumentList "/k python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload" -WindowStyle Normal

Start-Sleep -Seconds 4

# Start frontend
Write-Host "`n[STEP 4] Starting frontend..." -ForegroundColor Yellow
Set-Location "$ROOT\frontend"
Start-Process "cmd" -ArgumentList "/k npm run dev" -WindowStyle Normal

Write-Host "`n======================================" -ForegroundColor Cyan
Write-Host "  Backend:  http://127.0.0.1:8000" -ForegroundColor Green
Write-Host "  Frontend: http://localhost:5173" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Cyan
