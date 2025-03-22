# PowerShell script to start both backend and frontend servers
Write-Host "`n=== Fake News Detection System Startup ===" -ForegroundColor Cyan
Write-Host "Starting both backend and frontend servers..." -ForegroundColor Cyan
Write-Host "This script monitors both servers and handles errors automatically.`n" -ForegroundColor Cyan

# Check if PowerShell version supports jobs
$supportsJobs = $PSVersionTable.PSVersion.Major -ge 3
if (-not $supportsJobs) {
    Write-Host "ERROR: This script requires PowerShell 3.0 or higher." -ForegroundColor Red
    Write-Host "You're running PowerShell version $($PSVersionTable.PSVersion)" -ForegroundColor Red
    Write-Host "Please run backend and frontend servers separately using start-backend.ps1 and start-frontend.ps1" -ForegroundColor Yellow
    exit 1
}

# Define color variables for consistent styling
$backendColor = "Green"
$frontendColor = "Yellow"
$errorColor = "Red"
$infoColor = "Cyan"

# Get the current directory
$projectRoot = Get-Location

# Function to start the backend server
function Start-BackendServer {
    Write-Host "`n[BACKEND] Starting server..." -ForegroundColor $backendColor
    
    # Start backend using the script
    $backendScript = Join-Path -Path $projectRoot -ChildPath "start-backend.ps1"
    if (-not (Test-Path $backendScript)) {
        Write-Host "[BACKEND] Creating backend start script..." -ForegroundColor $backendColor
        
        # Create the script content
        $backendScriptContent = @'
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
if (-not (Test-Path "history")) { New-Item -ItemType Directory -Path "history" | Out-Null }
if (-not (Test-Path "reports")) { New-Item -ItemType Directory -Path "reports" | Out-Null }

# Try to install distutils manually if needed
try {
    & $pythonCmd -m pip install setuptools --upgrade
} catch {
    Write-Host "Warning: Could not upgrade setuptools. Some packages may fail to install." -ForegroundColor Yellow
}

# Start the server
Write-Host "`nStarting backend server with Python..." -ForegroundColor Cyan
& $pythonCmd app_new.py
'@
        
        # Write the script to disk
        Set-Content -Path $backendScript -Value $backendScriptContent
    }
    
    # Start the script as a background job
    $backendJob = Start-Job -ScriptBlock {
        param($scriptPath)
        # Execute the script
        powershell -ExecutionPolicy Bypass -File $scriptPath
    } -ArgumentList $backendScript
    
    Write-Host "[BACKEND] Started with job ID: $($backendJob.Id)" -ForegroundColor $backendColor
    return $backendJob
}

# Function to start the frontend server
function Start-FrontendServer {
    Write-Host "`n[FRONTEND] Starting server..." -ForegroundColor $frontendColor
    
    # Start frontend using the script
    $frontendScript = Join-Path -Path $projectRoot -ChildPath "start-frontend.ps1"
    if (-not (Test-Path $frontendScript)) {
        Write-Host "[FRONTEND] Creating frontend start script..." -ForegroundColor $frontendColor
        
        # Create the script content
        $frontendScriptContent = @'
# PowerShell script to start the frontend
Write-Host "=== Starting Frontend Server ===`n" -ForegroundColor Cyan

# Navigate to frontend directory if needed
if (-not ((Test-Path "package.json") -and ((Get-Content "package.json" -Raw) -match "fake-news-detector-frontend"))) {
    if (Test-Path "frontend\package.json") {
        Set-Location "frontend"
    } elseif (Test-Path "..\frontend\package.json") {
        Set-Location "..\frontend"
    } else {
        Write-Host "ERROR: Cannot find frontend directory." -ForegroundColor Red
        exit 1
    }
}

# Ensure the dev script exists in package.json
$packageJson = Get-Content "package.json" -Raw | ConvertFrom-Json
if (-not ($packageJson.scripts.dev)) {
    Write-Host "Adding 'dev' script to package.json..." -ForegroundColor Yellow
    $packageJson.scripts | Add-Member -Name "dev" -Value "react-scripts start" -MemberType NoteProperty -Force
    $packageJson | ConvertTo-Json -Depth 10 | Set-Content "package.json"
}

# Set environment variables
$env:PORT = 3000

# Start the server
Write-Host "`nStarting React development server..." -ForegroundColor Cyan
npm run dev
'@
        
        # Write the script to disk
        Set-Content -Path $frontendScript -Value $frontendScriptContent
    }
    
    # Start the script as a background job
    $frontendJob = Start-Job -ScriptBlock {
        param($scriptPath)
        # Execute the script
        powershell -ExecutionPolicy Bypass -File $scriptPath
    } -ArgumentList $frontendScript
    
    Write-Host "[FRONTEND] Started with job ID: $($frontendJob.Id)" -ForegroundColor $frontendColor
    return $frontendJob
}

# Function to monitor job status and output
function Monitor-Jobs {
    param (
        [Parameter(Mandatory=$true)]
        [System.Management.Automation.Job]$BackendJob,
        
        [Parameter(Mandatory=$true)]
        [System.Management.Automation.Job]$FrontendJob
    )
    
    $backendStarted = $false
    $frontendStarted = $false
    $backendHealth = $false
    
    # Number of seconds to wait for services to start
    $timeout = 120
    $startTime = Get-Date
    
    while ((Get-Date) -lt $startTime.AddSeconds($timeout)) {
        # Check backend job state
        $currentBackendState = $BackendJob.State
        if (-not $backendStarted -and $currentBackendState -eq "Running") {
            $backendStarted = $true
            Write-Host "[BACKEND] Job running - checking service health..." -ForegroundColor $backendColor
        }
        
        # If backend job is running, check if the service is responding
        if ($backendStarted -and -not $backendHealth) {
            try {
                $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -TimeoutSec 2 -ErrorAction SilentlyContinue
                if ($response.StatusCode -eq 200) {
                    $backendHealth = $true
                    Write-Host "[BACKEND] Service is healthy and responding!" -ForegroundColor $backendColor
                }
            } catch {
                # Health endpoint not responding yet, continue waiting
            }
        }
        
        # Check frontend job state
        $currentFrontendState = $FrontendJob.State
        if (-not $frontendStarted -and $currentFrontendState -eq "Running") {
            # Get any output from the job
            $output = Receive-Job -Job $FrontendJob -Keep
            if ($output -match "Compiled successfully" -or $output -match "You can now view" -or $output -match "Local:") {
                $frontendStarted = $true
                Write-Host "[FRONTEND] Server running successfully!" -ForegroundColor $frontendColor
            }
        }
        
        # Check if either job has failed
        if ($currentBackendState -eq "Failed" -or $currentBackendState -eq "Completed") {
            Write-Host "[BACKEND] Server stopped unexpectedly: $currentBackendState" -ForegroundColor $errorColor
            $output = Receive-Job -Job $BackendJob
            Write-Host $output -ForegroundColor $backendColor
            return $false
        }
        
        if ($currentFrontendState -eq "Failed" -or $currentFrontendState -eq "Completed") {
            Write-Host "[FRONTEND] Server stopped unexpectedly: $currentFrontendState" -ForegroundColor $errorColor
            $output = Receive-Job -Job $FrontendJob
            Write-Host $output -ForegroundColor $frontendColor
            return $false
        }
        
        # If both services are up, we're good to go
        if ($backendHealth -and $frontendStarted) {
            Write-Host "`n[SUCCESS] Both servers are running successfully!" -ForegroundColor $infoColor
            return $true
        }
        
        # Wait a bit before checking again
        Start-Sleep -Seconds 2
    }
    
    # If we reach here, we've timed out
    Write-Host "`n[ERROR] Timeout waiting for servers to start" -ForegroundColor $errorColor
    
    if (-not $backendStarted) {
        Write-Host "[BACKEND] Server failed to start. Check logs for details." -ForegroundColor $errorColor
    } elseif (-not $backendHealth) {
        Write-Host "[BACKEND] Server started but health endpoint is not responding." -ForegroundColor $errorColor
    }
    
    if (-not $frontendStarted) {
        Write-Host "[FRONTEND] Server failed to start. Check logs for details." -ForegroundColor $errorColor
    }
    
    return $false
}

# Function to open browser
function Open-ApplicationInBrowser {
    $url = "http://localhost:3000"
    Write-Host "`n[OPEN] Opening application in browser: $url" -ForegroundColor $infoColor
    
    try {
        Start-Process $url
    } catch {
        Write-Host "[OPEN] Failed to open browser automatically. Please open $url manually." -ForegroundColor $errorColor
    }
}

# Function to stop and clean up jobs
function Stop-AllJobs {
    param (
        [Parameter(Mandatory=$true)]
        [System.Management.Automation.Job]$BackendJob,
        
        [Parameter(Mandatory=$true)]
        [System.Management.Automation.Job]$FrontendJob
    )
    
    Write-Host "`n[CLEANUP] Stopping all servers..." -ForegroundColor $infoColor
    
    # Stop jobs
    Stop-Job -Job $BackendJob -ErrorAction SilentlyContinue
    Stop-Job -Job $FrontendJob -ErrorAction SilentlyContinue
    
    # Get final output
    Write-Host "`n[BACKEND] Final output:" -ForegroundColor $backendColor
    Receive-Job -Job $BackendJob | ForEach-Object { Write-Host $_ -ForegroundColor $backendColor }
    
    Write-Host "`n[FRONTEND] Final output:" -ForegroundColor $frontendColor
    Receive-Job -Job $FrontendJob | ForEach-Object { Write-Host $_ -ForegroundColor $frontendColor }
    
    # Remove jobs
    Remove-Job -Job $BackendJob -Force -ErrorAction SilentlyContinue
    Remove-Job -Job $FrontendJob -Force -ErrorAction SilentlyContinue
    
    Write-Host "[CLEANUP] All servers stopped" -ForegroundColor $infoColor
}

# Main execution flow
try {
    # Start backend first
    $backendJob = Start-BackendServer
    
    # Give backend a moment to start
    Write-Host "`n[WAIT] Waiting for backend to initialize..." -ForegroundColor $infoColor
    Start-Sleep -Seconds 5
    
    # Start frontend
    $frontendJob = Start-FrontendServer
    
    # Monitor both services
    $success = Monitor-Jobs -BackendJob $backendJob -FrontendJob $frontendJob
    
    if ($success) {
        # Open browser
        Open-ApplicationInBrowser
        
        # Display success message
        Write-Host "`n=== Servers Running Successfully ===" -ForegroundColor $infoColor
        Write-Host "To stop the servers, press CTRL+C or close this window" -ForegroundColor $infoColor
        Write-Host "Backend: http://localhost:8000" -ForegroundColor $backendColor
        Write-Host "Frontend: http://localhost:3000" -ForegroundColor $frontendColor
        Write-Host "================================================`n" -ForegroundColor $infoColor
        
        # Keep the script running
        Write-Host "Press CTRL+C to stop both servers..." -ForegroundColor $infoColor
        try {
            while ($true) {
                # Check if services are still healthy
                $backendHealthy = $false
                try {
                    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -TimeoutSec 2 -ErrorAction SilentlyContinue
                    $backendHealthy = $response.StatusCode -eq 200
                } catch {
                    # Health check failed
                }
                
                if (-not $backendHealthy) {
                    Write-Host "[WARNING] Backend server is not responding. The application may not function correctly." -ForegroundColor $errorColor
                }
                
                # Check job states
                if ($backendJob.State -ne "Running") {
                    Write-Host "[ERROR] Backend server has stopped running. Trying to restart..." -ForegroundColor $errorColor
                    Stop-Job -Job $backendJob -ErrorAction SilentlyContinue
                    Remove-Job -Job $backendJob -Force -ErrorAction SilentlyContinue
                    $backendJob = Start-BackendServer
                }
                
                if ($frontendJob.State -ne "Running") {
                    Write-Host "[ERROR] Frontend server has stopped running. Trying to restart..." -ForegroundColor $errorColor
                    Stop-Job -Job $frontendJob -ErrorAction SilentlyContinue
                    Remove-Job -Job $frontendJob -Force -ErrorAction SilentlyContinue
                    $frontendJob = Start-FrontendServer
                }
                
                # Wait before checking again
                Start-Sleep -Seconds 10
            }
        } catch {
            # User pressed CTRL+C
            Write-Host "`n[STOP] User-initiated shutdown" -ForegroundColor $infoColor
        }
    }
} finally {
    # Clean up
    if ($backendJob -or $frontendJob) {
        Stop-AllJobs -BackendJob $backendJob -FrontendJob $frontendJob
    }
    
    Write-Host "`nAll servers have been stopped. Press any key to exit..." -ForegroundColor $infoColor
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
} 