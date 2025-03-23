# Improved PowerShell script to start the backend server with robust error handling
Write-Host "`n=== Starting Fake News Detection Backend ===`n" -ForegroundColor Cyan

# Function to find Python executable
function Find-PythonExecutable {
    Write-Host "Searching for Python installation..." -ForegroundColor Yellow
    
    # Try multiple commands to find Python
    $pythonCommands = @("python", "python3", "py", "py -3")
    
    foreach ($cmd in $pythonCommands) {
        try {
            $output = & $cmd --version 2>&1
            if ($output -match "Python 3") {
                Write-Host "Found Python: $output using command: $cmd" -ForegroundColor Green
                return $cmd
            }
        } catch {
            # Continue to next command
        }
    }
    
    # Check common installation directories
    $commonPaths = @(
        "C:\Python37\python.exe",
        "C:\Python38\python.exe", 
        "C:\Python39\python.exe",
        "C:\Python310\python.exe",
        "C:\Python311\python.exe",
        "C:\Program Files\Python37\python.exe",
        "C:\Program Files\Python38\python.exe",
        "C:\Program Files\Python39\python.exe",
        "C:\Program Files\Python310\python.exe",
        "C:\Program Files\Python311\python.exe",
        "C:\Program Files (x86)\Python37\python.exe",
        "C:\Program Files (x86)\Python38\python.exe",
        "C:\Program Files (x86)\Python39\python.exe",
        "C:\Program Files (x86)\Python310\python.exe",
        "C:\Program Files (x86)\Python311\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python37\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python38\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python39\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python310\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe"
    )
    
    foreach ($path in $commonPaths) {
        if (Test-Path $path) {
            Write-Host "Found Python at: $path" -ForegroundColor Green
            return $path
        }
    }
    
    # Python not found
    Write-Host "Python 3.x not found. Please install Python 3.7 or later." -ForegroundColor Red
    return $null
}

# Function to ensure we're in the correct directory
function Set-BackendDirectory {
    # Check if we're in the correct directory
    if (-not (Test-Path ".\backend\app_new.py") -and -not (Test-Path ".\app_new.py")) {
        Write-Host "Could not find backend directory with app_new.py" -ForegroundColor Red
        
        # Try to find the backend directory
        if (Test-Path ".\backend") {
            Set-Location ".\backend"
            if (Test-Path ".\app_new.py") {
                Write-Host "Found backend directory, navigating to it." -ForegroundColor Green
                return $true
            }
        } elseif (Test-Path "..\backend") {
            Set-Location "..\backend"
            if (Test-Path ".\app_new.py") {
                Write-Host "Found backend directory, navigating to it." -ForegroundColor Green
                return $true
            }
        }
        
        Write-Host "Could not locate backend directory with app_new.py. Please run this script from the project root." -ForegroundColor Red
        return $false
    } elseif (Test-Path ".\backend\app_new.py") {
        Set-Location ".\backend"
        Write-Host "Found backend directory, navigating to it." -ForegroundColor Green
        return $true
    } elseif (Test-Path ".\app_new.py") {
        # Already in the backend directory
        Write-Host "Already in backend directory." -ForegroundColor Green
        return $true
    }
    
    return $false
}

# Function to install requirements
function Install-Requirements {
    param (
        [string]$PythonCmd
    )
    
    if (-not (Test-Path ".\requirements.txt")) {
        Write-Host "Warning: requirements.txt not found" -ForegroundColor Yellow
        return $true
    }
    
    Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
    try {
        & $PythonCmd -m pip install -r requirements.txt
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Warning: Some dependencies failed to install. Will attempt to install core dependencies." -ForegroundColor Yellow
            & $PythonCmd -m pip install fastapi uvicorn
            return $true
        }
        Write-Host "Dependencies installed successfully." -ForegroundColor Green
        return $true
    } catch {
        Write-Host "Error installing dependencies: $_" -ForegroundColor Red
        Write-Host "Will attempt to install core dependencies." -ForegroundColor Yellow
        try {
            & $PythonCmd -m pip install fastapi uvicorn
            return $true
        } catch {
            Write-Host "Failed to install core dependencies. The application may not run correctly." -ForegroundColor Red
            return $false
        }
    }
}

# Function to ensure necessary directories exist
function Ensure-Directories {
    $directories = @(".\reports", ".\history", ".\models")
    
    foreach ($dir in $directories) {
        if (-not (Test-Path $dir)) {
            Write-Host "Creating directory: $dir" -ForegroundColor Yellow
            New-Item -ItemType Directory -Path $dir | Out-Null
        }
    }
}

# Function to start the backend server with monitoring
function Start-BackendWithMonitoring {
    param (
        [string]$PythonCmd
    )
    
    # Configure error handling and retry logic
    $maxRetries = 5
    $retryCount = 0
    $healthCheckPort = 8000  # Default FastAPI port
    
    while ($retryCount -lt $maxRetries) {
        $retryCount++
        Write-Host "`nStarting backend server (Attempt $retryCount of $maxRetries)..." -ForegroundColor Green
        
        try {
            # Start the server
            $process = Start-Process -FilePath $PythonCmd -ArgumentList "app_new.py" -NoNewWindow -PassThru
            
            # Wait for server to start
            Write-Host "Waiting for server to start (checking http://localhost:$healthCheckPort)..." -ForegroundColor Yellow
            $serverStarted = $false
            $startTime = Get-Date
            $timeoutSeconds = 30
            
            while (-not $serverStarted -and ((Get-Date) - $startTime).TotalSeconds -lt $timeoutSeconds) {
                try {
                    # Try to connect to the server
                    $request = [System.Net.WebRequest]::Create("http://localhost:$healthCheckPort")
                    $request.Timeout = 1000
                    $response = $request.GetResponse()
                    $response.Close()
                    $serverStarted = $true
                    Write-Host "Backend server started successfully!" -ForegroundColor Green
                } catch {
                    # Server not ready yet, wait a bit
                    Start-Sleep -Seconds 1
                }
            }
            
            if (-not $serverStarted) {
                Write-Host "Timed out waiting for server to start." -ForegroundColor Red
                if ($retryCount -lt $maxRetries) {
                    Write-Host "Retrying in 5 seconds..." -ForegroundColor Yellow
                    Start-Sleep -Seconds 5
                    continue
                }
            }
            
            # Server started, provide information
            Write-Host "`n=== Backend Server Information ===`n" -ForegroundColor Cyan
            Write-Host "API URL: http://localhost:$healthCheckPort" -ForegroundColor Green
            Write-Host "API Documentation: http://localhost:$healthCheckPort/docs" -ForegroundColor Green
            Write-Host "`nPress Ctrl+C to stop the server.`n" -ForegroundColor Yellow
            
            # Wait for the process to exit
            $process.WaitForExit()
            
            # Check exit code
            if ($process.ExitCode -eq 0) {
                Write-Host "Server stopped gracefully." -ForegroundColor Yellow
                break
            } else {
                Write-Host "Server crashed with exit code $($process.ExitCode)" -ForegroundColor Red
                if ($retryCount -lt $maxRetries) {
                    Write-Host "Restarting in 5 seconds..." -ForegroundColor Yellow
                    Start-Sleep -Seconds 5
                }
            }
        } catch {
            Write-Host "Error starting server: $_" -ForegroundColor Red
            if ($retryCount -lt $maxRetries) {
                Write-Host "Retrying in 5 seconds..." -ForegroundColor Yellow
                Start-Sleep -Seconds 5
            }
        }
    }
    
    if ($retryCount -ge $maxRetries) {
        Write-Host "Maximum retry attempts reached. Please check server logs for errors." -ForegroundColor Red
    }
}

# MAIN EXECUTION

# Find Python
$pythonCmd = Find-PythonExecutable
if (-not $pythonCmd) {
    exit 1
}

# Go to the backend directory
if (-not (Set-BackendDirectory)) {
    exit 1
}

# Install requirements
if (-not (Install-Requirements -PythonCmd $pythonCmd)) {
    exit 1
}

# Ensure directories exist
Ensure-Directories

# Start server with monitoring
Start-BackendWithMonitoring -PythonCmd $pythonCmd

# Exit
Write-Host "`nBackend server has stopped. Press any key to exit..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 