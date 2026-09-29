@echo off
TITLE PhishGuard AI - One-Command Startup
echo ======================================================================
echo                 STARTING PHISHGUARD AI SYSTEM
echo ======================================================================
echo.

echo [1/2] Launching FastAPI Backend Server (http://127.0.0.1:8000)...
start "PhishGuard AI Backend" cmd /k "cd /d %~dp0backend && .\venv\Scripts\activate.bat && uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"

echo [2/2] Launching React Frontend Dev Server (http://localhost:5173)...
start "PhishGuard AI Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo ======================================================================
echo  PhishGuard AI is now initializing!
echo  - Backend API: http://127.0.0.1:8000/docs
echo  - Frontend Web App: http://localhost:5173
echo ======================================================================
echo.
pause
