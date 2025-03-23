@echo off
echo ===================================================
echo Fake News Detection System - Simple Starter
echo ===================================================
echo.

:: Create necessary directories
if not exist backend\reports mkdir backend\reports
if not exist backend\history mkdir backend\history
if not exist backend\models mkdir backend\models

:: Edit the frontend/src/config.js file
echo // API Configuration > frontend\src\config.js
echo export const API_URL = 'http://localhost:8000'; > frontend\src\config.js
echo export const API_TIMEOUT = 30000; // 30 seconds >> frontend\src\config.js

:: Start backend
echo Starting backend server...
start cmd /k "cd backend && python -m pip install fastapi uvicorn && python app_new.py"

:: Wait for backend to initialize
echo Waiting for backend to initialize...
timeout /t 5 /nobreak > nul

:: Start frontend
echo Starting frontend server...
start cmd /k "cd frontend && npm install && npm run dev"

echo.
echo ===================================================
echo Both servers have been started!
echo ===================================================
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo.
echo If the text analysis is not working:
echo 1. Make sure both server windows show no errors
echo 2. Try refreshing the browser
echo 3. Check if the text meets the minimum length requirement (50 characters)
echo.
pause 