@echo off
echo ===================================================
echo Fake News Detection System - Single Server Deployment
echo ===================================================
echo.

:: Setup error handling
setlocal enabledelayedexpansion

:: Check for required tools
echo [1/8] Checking for required tools...
where node >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

where python >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Create directories
echo [2/8] Creating deployment directories...
if not exist deployment mkdir deployment
if not exist deployment\backend mkdir deployment\backend
if not exist deployment\frontend mkdir deployment\frontend
if not exist deployment\logs mkdir deployment\logs

:: Install backend dependencies
echo [3/8] Setting up backend...
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

:: Build frontend
echo [4/8] Building frontend for production...
cd frontend
call npm install
if %errorlevel% neq 0 (
    echo ERROR: Failed to install frontend dependencies
    cd ..
    pause
    exit /b 1
)

call npm run build
if %errorlevel% neq 0 (
    echo ERROR: Failed to build frontend
    cd ..
    pause
    exit /b 1
)
cd ..

:: Copy backend files
echo [5/8] Copying backend files to deployment directory...
xcopy /E /Y backend\*.py deployment\backend\
xcopy /E /Y backend\requirements.txt deployment\backend\
mkdir deployment\backend\reports
mkdir deployment\backend\history
mkdir deployment\backend\models
mkdir deployment\backend\utils
xcopy /E /Y backend\utils\*.py deployment\backend\utils\

:: Copy frontend build files
echo [6/8] Copying frontend build files to deployment directory...
xcopy /E /Y frontend\build\* deployment\frontend\

:: Create combined server script
echo [7/8] Creating server script...
echo import os > deployment\server.py
echo import sys >> deployment\server.py
echo import uvicorn >> deployment\server.py
echo import subprocess >> deployment\server.py
echo import threading >> deployment\server.py
echo import webbrowser >> deployment\server.py
echo import time >> deployment\server.py
echo from pathlib import Path >> deployment\server.py
echo. >> deployment\server.py
echo # Import FastAPI app >> deployment\server.py
echo sys_path = os.path.dirname(os.path.abspath(__file__)) >> deployment\server.py
echo backend_dir = os.path.join(sys_path, 'backend') >> deployment\server.py
echo os.chdir(backend_dir) >> deployment\server.py
echo sys.path.append(backend_dir) >> deployment\server.py
echo from app_new import app >> deployment\server.py
echo. >> deployment\server.py
echo # Serve static files from frontend build >> deployment\server.py
echo from fastapi.staticfiles import StaticFiles >> deployment\server.py
echo frontend_dir = os.path.join(sys_path, 'frontend') >> deployment\server.py
echo app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend") >> deployment\server.py
echo. >> deployment\server.py
echo if __name__ == "__main__": >> deployment\server.py
echo     port = int(os.environ.get("PORT", 8000)) >> deployment\server.py
echo     print(f"Starting server at http://localhost:{port}") >> deployment\server.py
echo     print("Press Ctrl+C to stop the server") >> deployment\server.py
echo     # Open browser after a short delay >> deployment\server.py
echo     def open_browser(): >> deployment\server.py
echo         time.sleep(2) >> deployment\server.py
echo         webbrowser.open(f"http://localhost:{port}") >> deployment\server.py
echo     threading.Thread(target=open_browser).start() >> deployment\server.py
echo     # Start server >> deployment\server.py
echo     uvicorn.run(app, host="0.0.0.0", port=port) >> deployment\server.py

:: Create startup script
echo [8/8] Creating startup script...
echo @echo off > deployment\start-server.cmd
echo echo Starting Fake News Detection System... >> deployment\start-server.cmd
echo cd /d %%~dp0 >> deployment\start-server.cmd
echo python server.py >> deployment\start-server.cmd
echo pause >> deployment\start-server.cmd

echo.
echo ===================================================
echo Deployment completed successfully!
echo ===================================================
echo.
echo Your application has been deployed to the 'deployment' directory.
echo.
echo To start the server:
echo 1. Navigate to the deployment directory
echo 2. Run start-server.cmd
echo.
echo The server will run on http://localhost:8000 and will serve:
echo - Frontend: http://localhost:8000/
echo - Backend API: http://localhost:8000/analyze and other endpoints
echo.
echo.
echo For production deployment:
echo - Configure a proper web server like Nginx or Apache
echo - Set up process management with systemd or PM2
echo - Configure HTTPS with Let's Encrypt
echo.
pause 