# Integrated script to run both backend and frontend servers
# Provides clean logging and automatically opens the application in the browser

# Configuration
$backendPort = 8000
$frontendPort = 3000
$backendUrl = "http://localhost:$backendPort"
$frontendUrl = "http://localhost:$frontendPort"
$healthCheckEndpoint = "$backendUrl/health"
$maxAttempts = 15  # Increased attempts
$waitTime = 2 # seconds

# Script directory for relative paths
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path

# Create function to write colored output
function Write-ColorOutput($message, $color) {
    Write-Host $message -ForegroundColor $color
}

# Function to check if a port is in use
function Test-PortInUse($port) {
    try {
        $connections = Get-NetTCPConnection -State Listen -LocalPort $port -ErrorAction SilentlyContinue
        return $null -ne $connections
    }
    catch {
        Write-ColorOutput "Warning: Unable to check port $port. Assuming it's free." "Yellow"
        return $false
    }
}

# Kill processes using specific ports if necessary
function Stop-ProcessOnPort($port) {
    try {
        Write-ColorOutput "Checking if port $port is in use..." "Yellow"
        if (Test-PortInUse $port) {
            Write-ColorOutput "Port $port is in use. Attempting to free it..." "Yellow"
            $process = Get-Process -Id (Get-NetTCPConnection -LocalPort $port -State Listen).OwningProcess -ErrorAction SilentlyContinue
            if ($process) {
                Write-ColorOutput "Stopping process: $($process.ProcessName) (PID: $($process.Id))..." "Yellow"
                Stop-Process -Id $process.Id -Force
                Start-Sleep -Seconds 2
            }
        }
    }
    catch {
        Write-ColorOutput "Error checking port $port. Please check manually." "Red"
    }
}

# Function to test backend health
function Test-BackendHealth {
    try {
        $response = Invoke-WebRequest -Uri $healthCheckEndpoint -TimeoutSec 5 -UseBasicParsing
        return $response.StatusCode -eq 200
    }
    catch {
        return $false
    }
}

# Ensure Python is available
function Test-PythonAvailability {
    try {
        $pythonVersion = & python --version 2>&1
        if ($pythonVersion -match "Python \d+\.\d+\.\d+") {
            Write-ColorOutput "Found Python: $pythonVersion" "Green"
            return $true
        }
        else {
            Write-ColorOutput "Python not found or returned unexpected output" "Red"
            return $false
        }
    }
    catch {
        Write-ColorOutput "Python is not available in PATH. Please install Python and add it to your PATH." "Red"
        return $false
    }
}

# Ensure Node.js is available
function Test-NodeAvailability {
    try {
        $nodeVersion = & node --version 2>&1
        if ($nodeVersion -match "v\d+\.\d+\.\d+") {
            Write-ColorOutput "Found Node.js: $nodeVersion" "Green"
            return $true
        }
        else {
            Write-ColorOutput "Node.js not found or returned unexpected output" "Red"
            return $false
        }
    }
    catch {
        Write-ColorOutput "Node.js is not available in PATH. Please install Node.js and add it to your PATH." "Red"
        return $false
    }
}

# Main execution starts here
Write-ColorOutput "====== Starting Fake News Detection Application ======" "Cyan"

# Check requirements
if (-not (Test-PythonAvailability)) {
    Write-ColorOutput "Python is required to run the backend server. Please install Python and try again." "Red"
    exit 1
}

if (-not (Test-NodeAvailability)) {
    Write-ColorOutput "Node.js is required to run the frontend server. Please install Node.js and try again." "Red"
    exit 1
}

# Stop any processes on our ports
Stop-ProcessOnPort $backendPort
Stop-ProcessOnPort $frontendPort

Write-ColorOutput "`n[1/3] Starting Backend Server on port $backendPort..." "Green"

# Start the backend in a new PowerShell window
$backendPath = Join-Path -Path $scriptPath -ChildPath "backend"
$backendCmd = "cd '$backendPath'; python -m uvicorn fallback_app:app --reload --host 0.0.0.0 --port $backendPort"
Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendCmd

Write-ColorOutput "`nWaiting for backend to initialize..." "Yellow"

# Check if backend is up
$healthy = $false
$attempt = 1

while (-not $healthy -and $attempt -le $maxAttempts) {
    Write-ColorOutput "Checking backend health (Attempt $attempt of $maxAttempts)..." "Yellow"
    
    if (Test-BackendHealth) {
        $healthy = $true
        Write-ColorOutput "Backend is running on $backendUrl" "Green"
    }
    else {
        Write-ColorOutput "Backend not responsive yet. Waiting $waitTime seconds..." "Yellow"
        Start-Sleep -Seconds $waitTime
        $attempt++
    }
}

if (-not $healthy) {
    Write-ColorOutput "Backend failed to start properly. Please check for errors in the backend window." "Red"
    Write-ColorOutput "You may need to ensure all requirements are installed: pip install -r backend/requirements.txt" "Yellow"
    Write-ColorOutput "`nAttempting to continue with frontend startup anyway..." "Yellow"
}

Write-ColorOutput "`n[2/3] Starting Frontend Server on port $frontendPort..." "Green"

# Start the frontend in a new PowerShell window
$frontendPath = Join-Path -Path $scriptPath -ChildPath "frontend"
$frontendCmd = "cd '$frontendPath'; npm start"
Start-Process powershell -ArgumentList "-NoExit", "-Command", $frontendCmd

Write-ColorOutput "`nWaiting for frontend to initialize..." "Yellow"
Start-Sleep -Seconds 10  # Increased wait time

Write-ColorOutput "`n[3/3] Opening application in browser..." "Green"

# Open the application in the default browser
Start-Process $frontendUrl

Write-ColorOutput "`n====== Application Started ======" "Cyan"
Write-ColorOutput "Frontend: $frontendUrl" "Green"
Write-ColorOutput "Backend API: $backendUrl" "Green"
Write-ColorOutput "API Documentation: $backendUrl/docs" "Green"
Write-ColorOutput "`nTo stop the application, close the server windows or press Ctrl+C in each window." "Yellow" 