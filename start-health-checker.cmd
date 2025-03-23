@echo off
echo ===================================================
echo Fake News Detection Backend Health Checker
echo ===================================================
echo.

:: Check for Node.js
where node >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

:: Create logs directory
if not exist logs mkdir logs

:: Start the health checker in the background
echo Starting health checker in the background...
start /B node backend\health-check.js > logs\health-checker-output.log 2>&1

echo Health checker started successfully in the background.
echo It will automatically monitor and restart the backend if needed.
echo.
echo You can close this window now.
timeout /t 5 