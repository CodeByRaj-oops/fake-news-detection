@echo off
echo Starting Fake News Detection Application...
echo.

:: Create necessary directories
if not exist backend\reports mkdir backend\reports
if not exist backend\history mkdir backend\history

:: Start backend in a new window
start cmd /k "cd backend && echo Installing backend dependencies... && python -m pip install -r requirements.txt && echo Starting backend server... && python app_new.py"

:: Wait for backend to start
echo Waiting for backend to initialize...
timeout /t 5 /nobreak > nul

:: Start frontend in another window
start cmd /k "cd frontend && echo Installing frontend dependencies... && npm install && echo Starting frontend server... && npm run dev"

echo.
echo Servers are starting in separate windows.
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Press any key to exit this window...
pause > nul 