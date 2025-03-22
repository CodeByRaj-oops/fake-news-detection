# Simplified PowerShell script to run both backend and frontend with proper error handling
Write-Host "`n=== Fake News Detection System ===`n" -ForegroundColor Cyan
Write-Host "This script will start both the backend and frontend servers" -ForegroundColor Cyan

# Step 1: Install backend dependencies first
Write-Host "`n[1/4] Installing backend dependencies..." -ForegroundColor Green
$pythonCommands = @("python", "python3", "py")
$pythonFound = $false

foreach ($cmd in $pythonCommands) {
    try {
        $null = & $cmd --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Using Python command: $cmd" -ForegroundColor Green
            $pythonFound = $true
            
            # Navigate to backend directory and install dependencies
            if (Test-Path "backend") {
                Push-Location "backend"
                if (Test-Path "requirements.txt") {
                    Write-Host "Installing Python packages from requirements.txt..." -ForegroundColor Cyan
                    & $cmd -m pip install -r requirements.txt
                } else {
                    Write-Host "Installing required packages individually..." -ForegroundColor Cyan
                    & $cmd -m pip install fastapi uvicorn scikit-learn pandas numpy
                }
                
                # Create required directories
                if (-not (Test-Path "history")) { New-Item -ItemType Directory -Path "history" | Out-Null }
                if (-not (Test-Path "reports")) { New-Item -ItemType Directory -Path "reports" | Out-Null }
                
                Pop-Location
            }
            break
        }
    } catch {
        # Command not found, try next
        continue
    }
}

if (-not $pythonFound) {
    Write-Host "ERROR: Python not found. Please install Python 3.x and add it to your PATH" -ForegroundColor Red
    Write-Host "Press any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

# Step 2: Start the backend server
Write-Host "`n[2/4] Starting backend server..." -ForegroundColor Green
$backendStarted = $false

# Start backend in a new window
$backendPath = Join-Path -Path (Get-Location) -ChildPath "backend"
$backendCommand = "cd '$backendPath'; $cmd app_new.py"

try {
    $backendProcess = Start-Process -FilePath "powershell.exe" -ArgumentList "-NoExit", "-Command", $backendCommand -PassThru
    Start-Sleep -Seconds 5  # Give backend time to start
    
    # Check if process is still running (basic check)
    if (-not $backendProcess.HasExited) {
        Write-Host "Backend server appears to be running (PID: $($backendProcess.Id))" -ForegroundColor Green
        $backendStarted = $true
    } else {
        Write-Host "Backend server failed to start or crashed immediately" -ForegroundColor Red
    }
} catch {
    Write-Host "Failed to start backend server: $_" -ForegroundColor Red
}

# Step 3: Install frontend dependencies
Write-Host "`n[3/4] Installing frontend dependencies..." -ForegroundColor Yellow
if (Test-Path "frontend") {
    Push-Location "frontend"
    
    # Check and ensure package.json has dev script
    if (Test-Path "package.json") {
        $packageJson = Get-Content "package.json" -Raw | ConvertFrom-Json
        
        # Fix proxy setting in package.json if needed
        $needsSave = $false
        if (-not (Get-Member -InputObject $packageJson -Name "proxy" -MemberType Properties) -or 
            $packageJson.proxy -ne "http://localhost:8000") {
            Write-Host "Updating proxy setting in package.json..." -ForegroundColor Yellow
            $packageJson | Add-Member -Name "proxy" -Value "http://localhost:8000" -MemberType NoteProperty -Force
            $needsSave = $true
        }
        
        # Check if dev script exists
        if (-not (Get-Member -InputObject $packageJson.scripts -Name "dev" -MemberType Properties)) {
            Write-Host "Adding dev script to package.json..." -ForegroundColor Yellow
            $packageJson.scripts | Add-Member -Name "dev" -Value "react-scripts start" -MemberType NoteProperty -Force
            $needsSave = $true
        }
        
        if ($needsSave) {
            $packageJson | ConvertTo-Json -Depth 10 | Set-Content "package.json"
            Write-Host "Updated package.json" -ForegroundColor Green
        }
    }
    
    # Install dependencies if node_modules doesn't exist
    if (-not (Test-Path "node_modules")) {
        Write-Host "Installing npm dependencies..." -ForegroundColor Yellow
        npm install
    }
    
    # Check for required files
    if (-not (Test-Path "public\index.html")) {
        if (-not (Test-Path "public")) {
            New-Item -ItemType Directory -Path "public" | Out-Null
        }
        
        Write-Host "Creating minimal index.html..." -ForegroundColor Yellow
        $htmlContent = @"
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <link rel="icon" href="%PUBLIC_URL%/favicon.ico" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta name="description" content="Fake News Detection System" />
    <link rel="manifest" href="%PUBLIC_URL%/manifest.json" />
    <title>Fake News Detector</title>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
  </body>
</html>
"@
        Set-Content -Path "public\index.html" -Value $htmlContent
    }
    
    Pop-Location
}

# Step 4: Start the frontend server
Write-Host "`n[4/4] Starting frontend server..." -ForegroundColor Yellow
$frontendStarted = $false

# Start frontend in a new window
$frontendPath = Join-Path -Path (Get-Location) -ChildPath "frontend"
$frontendCommand = "cd '$frontendPath'; npm run dev"

try {
    $frontendProcess = Start-Process -FilePath "powershell.exe" -ArgumentList "-NoExit", "-Command", $frontendCommand -PassThru
    Write-Host "Frontend server starting (PID: $($frontendProcess.Id))" -ForegroundColor Yellow
    $frontendStarted = $true
} catch {
    Write-Host "Failed to start frontend server: $_" -ForegroundColor Red
}

# Final status message
Write-Host "`n=== System Status ===`n" -ForegroundColor Cyan
if ($backendStarted) {
    Write-Host "Backend: RUNNING (http://localhost:8000)" -ForegroundColor Green
} else {
    Write-Host "Backend: FAILED" -ForegroundColor Red
}

if ($frontendStarted) {
    Write-Host "Frontend: RUNNING (http://localhost:3000)" -ForegroundColor Yellow
} else {
    Write-Host "Frontend: FAILED" -ForegroundColor Red
}

Write-Host "`nThe system is now running. Open your browser to http://localhost:3000" -ForegroundColor Cyan
Write-Host "To stop the servers, close the terminal windows that opened" -ForegroundColor Cyan
Write-Host "`nPress any key to exit this launcher..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 