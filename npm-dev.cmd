@echo off
echo === Starting Frontend Development Server ===
echo.
echo This will run the npm run dev command in the frontend directory.
echo.

REM Check if frontend directory exists
if not exist frontend\ (
  echo Error: frontend directory not found!
  goto :error
)

REM Check if package.json exists in frontend
if not exist frontend\package.json (
  echo Error: frontend/package.json not found!
  goto :error
)

REM Change to frontend directory
cd frontend

REM Run the dev script
echo Starting the dev server...
echo.
call npm run dev

goto :end

:error
echo.
echo Please make sure you're running this from the project root directory.
echo.
pause

:end
