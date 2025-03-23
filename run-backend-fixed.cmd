@echo off
echo ===================================================
echo Fake News Detection Backend - Fixed Version
echo ===================================================
echo.

:: Setup error handling
setlocal enabledelayedexpansion

:: Create logs directory
if not exist logs mkdir logs

:: Create necessary backend directories
if not exist backend\reports mkdir backend\reports
if not exist backend\history mkdir backend\history
if not exist backend\models mkdir backend\models

:: Check for Node.js
echo [1/5] Checking Node.js installation...
where node >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

:: Check for PM2
echo [2/5] Checking PM2 installation...
node -e "try { require('pm2'); console.log('PM2 is installed'); } catch(e) { console.log('Installing PM2...'); require('child_process').execSync('npm install -g pm2', {stdio: 'inherit'}); }"

:: Check for Python
echo [3/5] Checking Python installation...
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: Python is not found in PATH. Will attempt to find it...
    
    :: Try to find Python in common locations
    if exist "C:\Python37\python.exe" (
        set PYTHON_CMD=C:\Python37\python.exe
    ) else if exist "C:\Python38\python.exe" (
        set PYTHON_CMD=C:\Python38\python.exe
    ) else if exist "C:\Python39\python.exe" (
        set PYTHON_CMD=C:\Python39\python.exe
    ) else if exist "C:\Python310\python.exe" (
        set PYTHON_CMD=C:\Python310\python.exe
    ) else if exist "C:\Program Files\Python37\python.exe" (
        set PYTHON_CMD="C:\Program Files\Python37\python.exe"
    ) else if exist "C:\Program Files\Python38\python.exe" (
        set PYTHON_CMD="C:\Program Files\Python38\python.exe"
    ) else if exist "C:\Program Files\Python39\python.exe" (
        set PYTHON_CMD="C:\Program Files\Python39\python.exe"
    ) else if exist "C:\Program Files\Python310\python.exe" (
        set PYTHON_CMD="C:\Program Files\Python310\python.exe"
    ) else (
        echo ERROR: Python not found. Please install Python 3.7+
        pause
        exit /b 1
    )
    
    echo Found Python at: !PYTHON_CMD!
) else (
    set PYTHON_CMD=python
)

:: Install Python dependencies
echo [4/5] Installing Python dependencies...
cd backend
!PYTHON_CMD! -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo WARNING: Failed to install dependencies with pip. Trying an alternative approach...
    !PYTHON_CMD! -m pip install --upgrade pip
    !PYTHON_CMD! -m pip install fastapi uvicorn
)
cd ..

:: Start the backend with PM2
echo [5/5] Starting backend with PM2...
cd backend

:: Configure PM2 ecosystem file
echo module.exports = { > ecosystem.config.js
echo   apps: [{ >> ecosystem.config.js
echo     name: "fake-news-backend", >> ecosystem.config.js
echo     script: "app_new.py", >> ecosystem.config.js
echo     interpreter: "python", >> ecosystem.config.js
echo     env: { >> ecosystem.config.js
echo       PORT: 5000 >> ecosystem.config.js
echo     }, >> ecosystem.config.js
echo     watch: true, >> ecosystem.config.js
echo     ignore_watch: ["__pycache__", "*.pyc", "reports", "history"], >> ecosystem.config.js
echo     max_memory_restart: "500M", >> ecosystem.config.js
echo     autorestart: true, >> ecosystem.config.js
echo     restart_delay: 3000, >> ecosystem.config.js
echo     max_restarts: 10, >> ecosystem.config.js
echo     error_file: "../logs/backend-error.log", >> ecosystem.config.js
echo     out_file: "../logs/backend-output.log", >> ecosystem.config.js
echo   }] >> ecosystem.config.js
echo } >> ecosystem.config.js

:: Kill any existing instances
call pm2 delete fake-news-backend >nul 2>&1

:: Start with PM2
call pm2 start ecosystem.config.js
cd ..

:: Create health check service
echo import http.server > backend\health_checker.py
echo import socketserver >> backend\health_checker.py
echo import threading >> backend\health_checker.py
echo import time >> backend\health_checker.py
echo import requests >> backend\health_checker.py
echo import sys >> backend\health_checker.py
echo import os >> backend\health_checker.py
echo import subprocess >> backend\health_checker.py
echo. >> backend\health_checker.py
echo # Configuration >> backend\health_checker.py
echo PORT = int(os.environ.get('PORT', 5000)) >> backend\health_checker.py
echo CHECK_INTERVAL = 60  # seconds >> backend\health_checker.py
echo MAX_RETRIES = 3 >> backend\health_checker.py
echo. >> backend\health_checker.py
echo def check_backend_health(): >> backend\health_checker.py
echo     """Check if the backend is healthy""" >> backend\health_checker.py
echo     try: >> backend\health_checker.py
echo         response = requests.get(f'http://localhost:{PORT}/health', timeout=5) >> backend\health_checker.py
echo         return response.status_code == 200 >> backend\health_checker.py
echo     except Exception as e: >> backend\health_checker.py
echo         print(f"Health check failed: {e}") >> backend\health_checker.py
echo         return False >> backend\health_checker.py
echo. >> backend\health_checker.py
echo def restart_backend(): >> backend\health_checker.py
echo     """Restart the backend server""" >> backend\health_checker.py
echo     try: >> backend\health_checker.py
echo         # First try using PM2 >> backend\health_checker.py
echo         subprocess.run(['pm2', 'restart', 'fake-news-backend'], check=True) >> backend\health_checker.py
echo         print("Backend restarted with PM2") >> backend\health_checker.py
echo         return True >> backend\health_checker.py
echo     except Exception as e: >> backend\health_checker.py
echo         print(f"Failed to restart with PM2: {e}") >> backend\health_checker.py
echo         # Fall back to direct start >> backend\health_checker.py
echo         try: >> backend\health_checker.py
echo             subprocess.Popen(['python', 'app_new.py'], cwd=os.path.dirname(os.path.abspath(__file__))) >> backend\health_checker.py
echo             print("Backend restarted directly") >> backend\health_checker.py
echo             return True >> backend\health_checker.py
echo         except Exception as e2: >> backend\health_checker.py
echo             print(f"Failed to restart directly: {e2}") >> backend\health_checker.py
echo             return False >> backend\health_checker.py
echo. >> backend\health_checker.py
echo def health_checker_thread(): >> backend\health_checker.py
echo     """Thread to periodically check backend health""" >> backend\health_checker.py
echo     failed_checks = 0 >> backend\health_checker.py
echo     while True: >> backend\health_checker.py
echo         if check_backend_health(): >> backend\health_checker.py
echo             failed_checks = 0 >> backend\health_checker.py
echo             print("Backend health check passed") >> backend\health_checker.py
echo         else: >> backend\health_checker.py
echo             failed_checks += 1 >> backend\health_checker.py
echo             print(f"Failed health checks: {failed_checks}/{MAX_RETRIES}") >> backend\health_checker.py
echo             if failed_checks >= MAX_RETRIES: >> backend\health_checker.py
echo                 print("Too many failed health checks. Restarting backend...") >> backend\health_checker.py
echo                 restart_backend() >> backend\health_checker.py
echo                 failed_checks = 0 >> backend\health_checker.py
echo         time.sleep(CHECK_INTERVAL) >> backend\health_checker.py
echo. >> backend\health_checker.py
echo # Start health checker thread >> backend\health_checker.py
echo health_thread = threading.Thread(target=health_checker_thread, daemon=True) >> backend\health_checker.py
echo health_thread.start() >> backend\health_checker.py
echo. >> backend\health_checker.py
echo # Status server to show that the health checker is running >> backend\health_checker.py
echo class HealthHandler(http.server.SimpleHTTPRequestHandler): >> backend\health_checker.py
echo     def do_GET(self): >> backend\health_checker.py
echo         self.send_response(200) >> backend\health_checker.py
echo         self.send_header('Content-type', 'text/html') >> backend\health_checker.py
echo         self.end_headers() >> backend\health_checker.py
echo         self.wfile.write(bytes("<html><body><h1>Health Checker Running</h1>" >> backend\health_checker.py
echo                              "<p>Backend status: " + ("OK" if check_backend_health() else "Not responding") + "</p>" >> backend\health_checker.py
echo                              "</body></html>", "utf-8")) >> backend\health_checker.py
echo. >> backend\health_checker.py
echo PORT = 8080 >> backend\health_checker.py
echo Handler = HealthHandler >> backend\health_checker.py
echo. >> backend\health_checker.py
echo with socketserver.TCPServer(("", PORT), Handler) as httpd: >> backend\health_checker.py
echo     print(f"Health checker monitoring backend on port {PORT}") >> backend\health_checker.py
echo     print(f"View status at http://localhost:{PORT}") >> backend\health_checker.py
echo     try: >> backend\health_checker.py
echo         httpd.serve_forever() >> backend\health_checker.py
echo     except KeyboardInterrupt: >> backend\health_checker.py
echo         pass >> backend\health_checker.py
echo     httpd.server_close() >> backend\health_checker.py

:: Start the health checker in the background
echo Starting health checker in the background...
start "Health Checker" /B python backend\health_checker.py > logs\health_checker.log 2>&1

echo.
echo ===================================================
echo Backend successfully started and health checker is running!
echo ===================================================
echo.
echo Backend API: http://localhost:5000
echo API Documentation: http://localhost:5000/docs
echo Health Status: http://localhost:8080
echo.
echo The backend is now running with automatic crash recovery.
echo The health checker will restart the backend if it stops responding.
echo.
echo Press any key to stop all services...
pause

:: Stop services
echo Stopping services...
call pm2 delete fake-news-backend
taskkill /F /FI "WINDOWTITLE eq Health Checker" /T
echo Done! 