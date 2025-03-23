@echo off
echo ===================================================
echo Fake News Detection System - Docker Deployment
echo ===================================================
echo.

:: Check for Docker
echo [1/5] Checking for Docker...
where docker >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker is not installed or not in PATH
    echo Please install Docker from https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

:: Create server.py for Docker
echo [2/5] Creating server script for Docker...
if not exist deployment mkdir deployment

echo import os > deployment\server.py
echo import sys >> deployment\server.py
echo import uvicorn >> deployment\server.py
echo import threading >> deployment\server.py
echo import time >> deployment\server.py
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
echo     host = os.environ.get("HOST", "0.0.0.0") >> deployment\server.py
echo     print(f"Starting server at http://{host}:{port}") >> deployment\server.py
echo     uvicorn.run(app, host=host, port=port) >> deployment\server.py

:: Create data directory
echo [3/5] Creating data directory...
if not exist data mkdir data

:: Build Docker image
echo [4/5] Building Docker image...
docker build -t fake-news-detector .
if %errorlevel% neq 0 (
    echo ERROR: Failed to build Docker image
    pause
    exit /b 1
)

:: Start Docker container
echo [5/5] Starting Docker container...
docker-compose up -d
if %errorlevel% neq 0 (
    echo ERROR: Failed to start Docker container
    pause
    exit /b 1
)

echo.
echo ===================================================
echo Docker deployment completed successfully!
echo ===================================================
echo.
echo Your application is now running at:
echo http://localhost:8000
echo.
echo To stop the application, run:
echo docker-compose down
echo.
echo To view logs, run:
echo docker-compose logs -f
echo.
pause 