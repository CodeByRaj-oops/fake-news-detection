@echo off
echo ===================================================
echo Fake News Detection System - Production Setup
echo ===================================================
echo.

:: Setup error handling
setlocal enabledelayedexpansion

:: Check for Python installation
echo [1/10] Checking Python installation...
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Check for Node.js installation
echo [2/10] Checking Node.js installation...
where node >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js 14+ from https://nodejs.org/
    pause
    exit /b 1
)

:: Create necessary directories
echo [3/10] Creating necessary directories...
if not exist backend\reports mkdir backend\reports
if not exist backend\history mkdir backend\history
if not exist backend\models mkdir backend\models
if not exist logs mkdir logs

:: Install backend dependencies
echo [4/10] Installing backend dependencies...
cd backend
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install backend dependencies
    cd ..
    pause
    exit /b 1
)
cd ..

:: Install frontend dependencies
echo [5/10] Installing frontend dependencies...
cd frontend
call npm install
if %errorlevel% neq 0 (
    echo ERROR: Failed to install frontend dependencies
    cd ..
    pause
    exit /b 1
)

:: Build frontend for production
echo [6/10] Building frontend for production...
call npm run build
if %errorlevel% neq 0 (
    echo ERROR: Failed to build frontend
    cd ..
    pause
    exit /b 1
)
cd ..

:: Create production server script
echo [7/10] Creating production server configuration...
echo import os > backend\production_server.py
echo import uvicorn >> backend\production_server.py
echo from app_new import app >> backend\production_server.py
echo. >> backend\production_server.py
echo if __name__ == "__main__": >> backend\production_server.py
echo     port = int(os.environ.get("PORT", 8000)) >> backend\production_server.py
echo     uvicorn.run(app, host="0.0.0.0", port=port) >> backend\production_server.py

:: Create start script for production
echo [8/10] Creating startup scripts...
echo @echo off > start-production.cmd
echo cd backend >> start-production.cmd
echo start /B python production_server.py ^> ..\logs\backend.log 2^>^&1 >> start-production.cmd
echo cd .. >> start-production.cmd
echo echo Server running at http://localhost:8000 >> start-production.cmd
echo echo Logs available in logs\backend.log >> start-production.cmd
echo echo. >> start-production.cmd
echo echo To deploy the frontend, serve the files in frontend\build with a web server >> start-production.cmd
echo echo For testing, you can use: >> start-production.cmd
echo echo cd frontend\build ^& python -m http.server 3000 >> start-production.cmd
echo pause >> start-production.cmd

:: Create monitoring script
echo [9/10] Creating health monitoring script...
echo @echo off > monitor-servers.cmd
echo echo Checking server health... >> monitor-servers.cmd
echo echo. >> monitor-servers.cmd
echo curl -s http://localhost:8000/health >> monitor-servers.cmd
echo echo. >> monitor-servers.cmd
echo echo If you see a JSON response above, the server is running correctly. >> monitor-servers.cmd
echo pause >> monitor-servers.cmd

:: Create documentation
echo [10/10] Creating documentation...
echo # Fake News Detection System - Production Deployment > PRODUCTION.md
echo. >> PRODUCTION.md
echo ## System Requirements >> PRODUCTION.md
echo. >> PRODUCTION.md
echo - Python 3.7+ >> PRODUCTION.md
echo - Node.js 14+ >> PRODUCTION.md
echo - 4GB RAM minimum >> PRODUCTION.md
echo - 2GB free disk space >> PRODUCTION.md
echo. >> PRODUCTION.md
echo ## Deployment Instructions >> PRODUCTION.md
echo. >> PRODUCTION.md
echo 1. Run `production-setup.cmd` to prepare the environment >> PRODUCTION.md
echo 2. Run `start-production.cmd` to start the backend server >> PRODUCTION.md
echo 3. Deploy the frontend files in `frontend/build` to your web server >> PRODUCTION.md
echo 4. Configure your web server to proxy API requests to the backend server >> PRODUCTION.md
echo. >> PRODUCTION.md
echo ## Monitoring >> PRODUCTION.md
echo. >> PRODUCTION.md
echo - Backend logs are stored in `logs/backend.log` >> PRODUCTION.md
echo - Use `monitor-servers.cmd` to check if the server is running correctly >> PRODUCTION.md
echo - Health endpoint: `http://localhost:8000/health` >> PRODUCTION.md
echo. >> PRODUCTION.md
echo ## Troubleshooting >> PRODUCTION.md
echo. >> PRODUCTION.md
echo - If the backend fails to start, check the logs in `logs/backend.log` >> PRODUCTION.md
echo - Ensure all directories have proper write permissions >> PRODUCTION.md
echo - Verify that ports 8000 and 3000 are not in use by other applications >> PRODUCTION.md
echo - For connection issues, verify that CORS is properly configured in the backend >> PRODUCTION.md

echo.
echo ===================================================
echo Setup complete! Your system is ready for production.
echo ===================================================
echo.
echo Documentation available in PRODUCTION.md
echo.
echo To start the production server, run: start-production.cmd
echo.
pause 