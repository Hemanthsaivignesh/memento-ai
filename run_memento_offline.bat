@echo off
title Memento AI - Offline Launcher
echo ========================================================
echo   Starting Memento AI (Fully Offline Mode)
echo ========================================================

:: Change directory to the script folder
cd /d "%~dp0"

echo 1. Launching Backend FastAPI Server...
start /b cmd /c "cd backend && .\venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000"

echo 2. Launching Frontend React Server...
start /b cmd /c "cd frontend && npm run dev"

echo 3. Waiting for servers to initialize...
timeout /t 3 /nobreak >nul

echo 4. Opening Memento AI in your default browser...
start http://localhost:5174

echo ========================================================
echo   Memento AI is now running.
echo   To stop the application, simply close this window!
echo ========================================================
pause
