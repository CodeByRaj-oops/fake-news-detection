# PowerShell script to start the backend server with error handling
Write-Host "Starting backend server..." -ForegroundColor Green

# Function to check if Python is installed
function Test-PythonInstallation {
    try {
        $pythonVersion = python --version 2>&1
        if ($pythonVersion -match "Python") {
            Write-Host "Found Python: $pythonVersion" -ForegroundColor Green
            return $true
        }
        return $false
    } catch {
        return $false
    }
}

# Function to check if required packages are installed
function Test-RequiredPackages {
    if (-not (Test-Path ".\requirements.txt")) {
        Write-Host "Warning: requirements.txt not found" -ForegroundColor Yellow
        return $true
    }

    try {
        $output = python -c "import fastapi, uvicorn, lime, shap" 2>&1
        return $true
    } catch {
        Write-Host "Some required packages are missing. Installing them now..." -ForegroundColor Yellow
        python -m pip install -r requirements.txt
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Failed to install requirements. Please run 'python -m pip install -r requirements.txt' manually." -ForegroundColor Red
            return $false
        }
        return $true
    }
}

# Check if we're in the backend directory
if (-not (Test-Path ".\app_new.py")) {
    # Try to navigate to backend directory
    if (Test-Path "..\backend\app_new.py") {
        Set-Location ..\backend
    } elseif (Test-Path ".\backend\app_new.py") {
        Set-Location .\backend
    } else {
        Write-Host "Error: Could not find backend directory. Please run this script from the project root or backend directory." -ForegroundColor Red
        exit 1
    }
}

# Verify Python installation
if (-not (Test-PythonInstallation)) {
    Write-Host "Error: Python is not installed or not in PATH. Please install Python and try again." -ForegroundColor Red
    exit 1
}

# Verify required packages
if (-not (Test-RequiredPackages)) {
    exit 1
}

# Create directories if they don't exist
if (-not (Test-Path ".\history")) {
    Write-Host "Creating history directory..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Path ".\history" | Out-Null
}

if (-not (Test-Path ".\reports")) {
    Write-Host "Creating reports directory..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Path ".\reports" | Out-Null
}

# Configure auto-restart
$maxRetries = 5
$retryCount = 0
$exitCode = 0

# Main server loop with auto-restart
do {
    try {
        $retryCount++
        Write-Host "Starting backend server (Attempt $retryCount of $maxRetries)..." -ForegroundColor Green
        
        # Start the server and capture output
        python app_new.py
        $exitCode = $LASTEXITCODE
        
        if ($exitCode -eq 0) {
            Write-Host "Server stopped gracefully." -ForegroundColor Yellow
            break
        } else {
            Write-Host "Server crashed with exit code $exitCode." -ForegroundColor Red
            
            if ($retryCount -lt $maxRetries) {
                Write-Host "Restarting in 5 seconds..." -ForegroundColor Yellow
                Start-Sleep -Seconds 5
            } else {
                Write-Host "Maximum retry attempts reached. Please check the logs." -ForegroundColor Red
            }
        }
    } catch {
        Write-Host "Error starting server: $_" -ForegroundColor Red
        
        if ($retryCount -lt $maxRetries) {
            Write-Host "Retrying in 5 seconds..." -ForegroundColor Yellow
            Start-Sleep -Seconds 5
        } else {
            Write-Host "Maximum retry attempts reached. Please check the server logs." -ForegroundColor Red
            break
        }
    }
} while ($retryCount -lt $maxRetries)

Write-Host "Press any key to exit..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 