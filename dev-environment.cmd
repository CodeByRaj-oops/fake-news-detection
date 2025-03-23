@echo off
echo ===================================================
echo Fake News Detection System - Development Environment
echo ===================================================
echo.

:: Setup error handling
setlocal enabledelayedexpansion

:: Check for Python
echo [1/6] Checking Python installation...
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Check for Node.js
echo [2/6] Checking Node.js installation...
where node >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js 14+ from https://nodejs.org/
    pause
    exit /b 1
)

:: Create necessary directories
echo [3/6] Creating necessary directories...
if not exist backend\reports mkdir backend\reports
if not exist backend\history mkdir backend\history
if not exist backend\models mkdir backend\models
if not exist logs mkdir logs

:: Update frontend API URL configuration
echo [4/6] Ensuring frontend can connect to backend...
if not exist frontend\src\config.js (
    echo Creating config.js with API URL configuration...
    echo // API Configuration > frontend\src\config.js
    echo export const API_URL = 'http://localhost:8000'; >> frontend\src\config.js
    echo export const API_TIMEOUT = 30000; // 30 seconds >> frontend\src\config.js
) else (
    echo Updating API URL in config.js...
    echo // API Configuration > frontend\src\config.js
    echo export const API_URL = 'http://localhost:8000'; >> frontend\src\config.js
    echo export const API_TIMEOUT = 30000; // 30 seconds >> frontend\src\config.js
)

:: Update backend CORS settings directly in app_new.py
echo [5/6] Updating backend CORS settings...
cd backend
python -c "
import re
import os

file_path = 'app_new.py'
with open(file_path, 'r') as file:
    content = file.read()

# Look for CORS middleware section and update it
cors_pattern = r'app\.add_middleware\(\s*CORSMiddleware,[\s\S]*?\)'
cors_replacement = '''app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  # Allow all origins in development
    allow_credentials=True,
    allow_methods=['*'],  # Allow all methods
    allow_headers=['*'],  # Allow all headers
)'''

# Replace CORS configuration
updated_content = re.sub(cors_pattern, cors_replacement, content)

# Write updated content back to file
with open(file_path, 'w') as file:
    file.write(updated_content)

print('Backend CORS settings updated successfully.')
"
cd ..

:: Start servers
echo [6/6] Starting development servers...
echo.
echo Starting backend server in a new window...
start cmd /k "cd backend && python -m pip install -r requirements.txt && python app_new.py"

:: Wait for backend to initialize
echo Waiting for backend to initialize...
timeout /t 5 /nobreak > nul

:: Check if backend is running
echo Checking if backend is running...
curl -s http://localhost:8000/health >nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: Backend may not be running correctly. Starting frontend anyway...
) else (
    echo Backend is running successfully!
)

:: Start frontend
echo Starting frontend in a new window...
start cmd /k "cd frontend && npm install && npm run dev"

echo.
echo ===================================================
echo Development environment started!
echo ===================================================
echo.
echo Frontend: http://localhost:3000
echo Backend: http://localhost:8000
echo API Health Check: http://localhost:8000/health
echo.
echo If you encounter connection issues:
echo 1. Ensure both terminal windows show servers running
echo 2. Check logs for any errors
echo 3. Try restarting with this script
echo.
pause 