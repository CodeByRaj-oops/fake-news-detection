@echo off
echo ===================================================
echo Fake News Detection Backend Starter
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

:: Go to the backend directory
cd backend

:: Run the backend runner script
echo Starting backend with Node.js runner...
node run-backend.js

:: This point will only be reached if the runner exits
echo.
echo Backend has stopped. Press any key to exit...
pause 