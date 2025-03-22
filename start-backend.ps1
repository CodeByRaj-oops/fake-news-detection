# PowerShell script to find Python and start the backend
Write-Host "=== Starting Backend Server ===`n" -ForegroundColor Cyan

# Find Python executable - try multiple possible paths/commands
$possiblePythonCommands = @("python", "python3", "py")
$pythonCmd = $null

foreach ($cmd in $possiblePythonCommands) {
    try {
        $output = & $cmd --version 2>&1
        if ($output -match "Python 3") {
            Write-Host "Found Python: $output" -ForegroundColor Green
            $pythonCmd = $cmd
            break
        }
    } catch {
        # Command not found, try next
        continue
    }
}

if ($null -eq $pythonCmd) {
    Write-Host "ERROR: Could not find Python. Please install Python 3.x and add it to your PATH." -ForegroundColor Red
    exit 1
}

# Navigate to backend directory if needed
$currentDir = Get-Location
$appPath = Join-Path -Path $currentDir -ChildPath "app_new.py"
$backendAppPath = Join-Path -Path $currentDir -ChildPath "backend\app_new.py"
$parentBackendAppPath = Join-Path -Path $currentDir -ChildPath "..\backend\app_new.py"

if (Test-Path $appPath) {
    # Already in the correct directory
    Write-Host "Found app_new.py in current directory" -ForegroundColor Green
} elseif (Test-Path $backendAppPath) {
    Write-Host "Found app_new.py in backend subdirectory" -ForegroundColor Green
    Set-Location "backend"
} elseif (Test-Path $parentBackendAppPath) {
    Write-Host "Found app_new.py in parent backend directory" -ForegroundColor Green
    Set-Location "..\backend"
} else {
    Write-Host "ERROR: Cannot find app_new.py in current, backend, or parent backend directory." -ForegroundColor Red
    Write-Host "Current directory: $currentDir" -ForegroundColor Yellow
    exit 1
}

# Create required directories
if (-not (Test-Path "history")) { 
    Write-Host "Creating history directory..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Path "history" | Out-Null 
}

if (-not (Test-Path "reports")) { 
    Write-Host "Creating reports directory..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Path "reports" | Out-Null 
}

# Try to install required packages for newer Python versions
try {
    Write-Host "Attempting to install setuptools (needed for distutils)..." -ForegroundColor Yellow
    & $pythonCmd -m pip install setuptools --upgrade
    Write-Host "Installing required packages..." -ForegroundColor Cyan
    & $pythonCmd -m pip install fastapi uvicorn scikit-learn pandas numpy
} catch {
    Write-Host "Warning: Could not install some packages. The server might not work correctly." -ForegroundColor Yellow
    Write-Host "Error details: $_" -ForegroundColor Yellow
}

# Start the server
Write-Host "`nStarting backend server with Python..." -ForegroundColor Cyan
try {
    & $pythonCmd app_new.py
} catch {
    Write-Host "ERROR: Failed to start backend server: $_" -ForegroundColor Red
    exit 1
} 