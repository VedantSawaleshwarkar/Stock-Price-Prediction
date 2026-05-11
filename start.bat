@echo off
title Stock Price Prediction Launcher
echo ======================================
echo   Stock Price Prediction - Launcher
echo ======================================

SET ROOT=D:\Programming\Yukti Tech Solution\Stock Price Prediction System using ML

echo [STEP 1] Starting Backend...
start "BACKEND - FastAPI" cmd /k "cd /d "%ROOT%\backend" && python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload"

echo [STEP 2] Waiting for backend...
timeout /t 5 /nobreak

echo [STEP 3] Starting Frontend...
start "FRONTEND - Vite" cmd /k "cd /d "%ROOT%\frontend" && npm install && npm run dev"

echo [STEP 4] Opening browser...
timeout /t 5 /nobreak
start http://localhost:5173

echo.
echo Both servers launched in separate windows!
echo Backend:  http://127.0.0.1:8000
echo Frontend: http://localhost:5173
pause
