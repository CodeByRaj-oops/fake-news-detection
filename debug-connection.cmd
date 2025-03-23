@echo off
echo ===================================================
echo Connection Debugger for Fake News Detection System
echo ===================================================
echo.

:: Setup error handling
setlocal enabledelayedexpansion

echo Performing connection diagnostics...
echo.

:: Check if backend is running
echo [1/6] Checking if backend server is running...
curl -s http://localhost:8000/health >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Backend server is not running or not responding.
    echo.
    echo Possible solutions:
    echo - Start the backend server with: cd backend ^& python app_new.py
    echo - Check for error messages in the backend terminal
    echo - Ensure port 8000 is not being used by another application
    echo.
) else (
    echo SUCCESS: Backend server is running on port 8000.
)

:: Check if frontend is running
echo [2/6] Checking if frontend development server is running...
curl -s http://localhost:3000 >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Frontend server is not running or not responding.
    echo.
    echo Possible solutions:
    echo - Start the frontend server with: cd frontend ^& npm run dev
    echo - Check for error messages in the frontend terminal
    echo - Ensure port 3000 is not being used by another application
    echo.
) else (
    echo SUCCESS: Frontend server is running on port 3000.
)

:: Check proxy configuration
echo [3/6] Checking proxy configuration in package.json...
cd frontend
findstr /C:"\"proxy\":" package.json >nul
if %errorlevel% neq 0 (
    echo ERROR: Proxy configuration not found in package.json.
    echo.
    echo Adding proxy configuration...
    node -e "const fs = require('fs'); const path = './package.json'; const pkg = JSON.parse(fs.readFileSync(path, 'utf8')); pkg.proxy = 'http://localhost:8000'; fs.writeFileSync(path, JSON.stringify(pkg, null, 2));"
    echo SUCCESS: Added proxy configuration to package.json.
    echo NOTE: You need to restart the frontend server for changes to take effect.
    echo.
) else (
    findstr /C:"\"proxy\": \"http://localhost:8000\"" package.json >nul
    if %errorlevel% neq 0 (
        echo ERROR: Incorrect proxy configuration in package.json.
        echo.
        echo Fixing proxy configuration...
        node -e "const fs = require('fs'); const path = './package.json'; const pkg = JSON.parse(fs.readFileSync(path, 'utf8')); pkg.proxy = 'http://localhost:8000'; fs.writeFileSync(path, JSON.stringify(pkg, null, 2));"
        echo SUCCESS: Updated proxy configuration in package.json.
        echo NOTE: You need to restart the frontend server for changes to take effect.
        echo.
    ) else (
        echo SUCCESS: Proxy configuration in package.json is correct.
    )
)
cd ..

:: Check CORS configuration
echo [4/6] Checking CORS configuration in backend...
cd backend
findstr /C:"allow_origins" app_new.py >nul
if %errorlevel% neq 0 (
    echo ERROR: CORS configuration not found in app_new.py.
    echo.
    echo This is a critical issue. Please check the backend code.
    echo.
) else (
    echo SUCCESS: CORS configuration exists in app_new.py.
    echo.
    echo Ensuring CORS is properly configured...
    python -c "
import re
import os

file_path = 'app_new.py'
with open(file_path, 'r') as file:
    content = file.read()

# Update CORS configuration
cors_pattern = r'app\.add_middleware\(\s*CORSMiddleware,[\s\S]*?\)'
cors_replacement = '''app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  # Allow all origins in development
    allow_credentials=True,
    allow_methods=['*'],  # Allow all methods
    allow_headers=['*'],  # Allow all headers
)'''

# Replace CORS configuration
if re.search(cors_pattern, content):
    updated_content = re.sub(cors_pattern, cors_replacement, content)
    with open(file_path, 'w') as file:
        file.write(updated_content)
    print('CORS configuration updated successfully.')
else:
    print('Could not locate CORS configuration section. Manual inspection required.')
"
    echo NOTE: Backend server needs to be restarted for CORS changes to take effect.
    echo.
)
cd ..

:: Check API connection in frontend code
echo [5/6] Checking API connection in frontend code...
cd frontend
findstr /s /C:"fetch" /C:"axios" /C:"API_URL" src\*.js >nul
if %errorlevel% neq 0 (
    echo WARNING: Could not find API calls in frontend code.
    echo This might be normal if the project uses a different method for API calls.
    echo.
) else (
    echo SUCCESS: Found API calls in frontend code.
    echo.
    echo Creating/updating API configuration file...
    echo // API Configuration > src\config.js
    echo export const API_URL = 'http://localhost:8000'; > src\config.js
    echo export const API_TIMEOUT = 30000; // 30 seconds >> src\config.js
    echo.
    echo Please use this configuration in your API calls:
    echo "import { API_URL } from '../config';"
    echo "fetch(`${API_URL}/your-endpoint`)"
    echo.
)
cd ..

:: Test the API connection
echo [6/6] Testing API connection...
echo.
echo Sending test request to backend health endpoint...
curl -s http://localhost:8000/health
echo.
echo.

echo ===================================================
echo Diagnosis complete!
echo ===================================================
echo.
echo If issues persist, try the following:
echo.
echo 1. Stop both frontend and backend servers
echo 2. Run dev-environment.cmd to start fresh
echo 3. Clear browser cache or try incognito/private mode
echo 4. Check browser console for specific error messages
echo 5. Ensure firewalls aren't blocking localhost connections
echo.
echo For a permanent fix, consider running production-setup.cmd
echo to prepare your project for production deployment.
echo.
pause 