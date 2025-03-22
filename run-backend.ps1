# Simple PowerShell script to navigate to backend directory and run the server
Write-Host "Starting backend server..." -ForegroundColor Cyan

# Navigate to backend directory if needed
if (Test-Path "backend\app_new.py") {
    Set-Location "backend"
    Write-Host "Found app_new.py in backend directory" -ForegroundColor Green
} elseif (Test-Path "..\backend\app_new.py") {
    Set-Location "..\backend"
    Write-Host "Found app_new.py in parent backend directory" -ForegroundColor Green
} elseif (-not (Test-Path "app_new.py")) {
    Write-Host "ERROR: Cannot find app_new.py in current, backend, or parent backend directory" -ForegroundColor Red
    exit 1
}

# Find Python
$pythonCommands = @("python", "python3", "py")
$pythonFound = $false

foreach ($cmd in $pythonCommands) {
    try {
        $null = & $cmd --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Using Python command: $cmd" -ForegroundColor Green
            & $cmd app_new.py
            $pythonFound = $true
            break
        }
    } catch {
        # Command not found, try next
    }
}

if (-not $pythonFound) {
    Write-Host "ERROR: Python not found. Please install Python 3.x and add it to your PATH" -ForegroundColor Red
    exit 1
}

# Keep the console open when done
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 