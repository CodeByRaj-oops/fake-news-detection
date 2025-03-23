@echo off
TITLE Fake News Detection Development Environment

echo Starting Backend Server (FastAPI) on port 8001...
start "Backend Server" cmd /k "cd backend && python -m uvicorn fallback_app:app --reload --host 0.0.0.0 --port 8001"

echo Starting Frontend Server (React) on port 3000...
start "Frontend Server" cmd /k "cd frontend && npm start"

echo.
echo ======== Development Environment Started ========
echo.
echo Backend: http://localhost:8001
echo Frontend: http://localhost:3000
echo API Documentation: http://localhost:8001/docs
echo.
echo Close this window to stop monitoring, or press Ctrl+C
echo in each server window to stop the individual servers.
echo.

:: Keep the window open
pause 