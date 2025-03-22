# PowerShell script to start both backend and frontend servers
Write-Host "`n=== Fake News Detection System Startup ===" -ForegroundColor Cyan
Write-Host "Starting both backend and frontend servers..." -ForegroundColor Cyan
Write-Host "This script will monitor and handle errors automatically.`n" -ForegroundColor Cyan

# Define colors for visual distinction
$backendColor = "Green"
$frontendColor = "Yellow" 
$errorColor = "Red"
$infoColor = "Cyan"

# Check if we're running as administrator
function Test-Admin {
    $currentUser = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
    return $currentUser.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# Create job to run the backend server
function Start-BackendServer {
    Write-Host "`n[BACKEND] Starting server..." -ForegroundColor $backendColor
    
    # Start backend using the script
    $backendJob = Start-Job -ScriptBlock {
        Set-Location $using:PWD
        if (Test-Path ".\backend\start-backend.ps1") {
            powershell -ExecutionPolicy Bypass -File ".\backend\start-backend.ps1"
        } elseif (Test-Path ".\backend\app_new.py") {
            cd backend
            if (Test-Path ".\requirements.txt") {
                python -m pip install -r requirements.txt
            }
            python app_new.py
        } else {
            Write-Error "Backend server files not found"
            exit 1
        }
    }
    
    Write-Host "[BACKEND] Started with job ID: $($backendJob.Id)" -ForegroundColor $backendColor
    return $backendJob
}

# Create job to run the frontend server
function Start-FrontendServer {
    Write-Host "`n[FRONTEND] Starting server..." -ForegroundColor $frontendColor
    
    # Start frontend
    $frontendJob = Start-Job -ScriptBlock {
        Set-Location $using:PWD
        if (Test-Path ".\npm-dev.cmd") {
            # Use the batch file
            cmd /c npm-dev.cmd
        } elseif (Test-Path ".\frontend\package.json") {
            # Direct approach
            cd frontend
            npm run dev
        } else {
            Write-Error "Frontend files not found"
            exit 1
        }
    }
    
    Write-Host "[FRONTEND] Started with job ID: $($frontendJob.Id)" -ForegroundColor $frontendColor
    return $frontendJob
}

# Monitor job status
function Monitor-Jobs {
    param (
        [Parameter(Mandatory=$true)]
        [System.Management.Automation.Job]$BackendJob,
        
        [Parameter(Mandatory=$true)]
        [System.Management.Automation.Job]$FrontendJob
    )
    
    $backendStarted = $false
    $frontendStarted = $false
    
    # Monitor for 120 seconds (2 minutes)
    $timeout = 120
    $startTime = Get-Date
    
    while ((Get-Date) -lt $startTime.AddSeconds($timeout)) {
        # Get backend status
        if ($BackendJob.State -eq "Running" -and -not $backendStarted) {
            Write-Host "[BACKEND] Server running" -ForegroundColor $backendColor
            $backendStarted = $true
        } elseif ($BackendJob.State -eq "Failed" -or $BackendJob.State -eq "Completed") {
            Write-Host "[BACKEND] Server stopped: $($BackendJob.State)" -ForegroundColor $errorColor
            Receive-Job -Job $BackendJob | ForEach-Object { Write-Host "[BACKEND] $_" -ForegroundColor $backendColor }
            return $false
        }
        
        # Get frontend status
        if ($FrontendJob.State -eq "Running" -and -not $frontendStarted) {
            Write-Host "[FRONTEND] Server running" -ForegroundColor $frontendColor
            $frontendStarted = $true
        } elseif ($FrontendJob.State -eq "Failed" -or $FrontendJob.State -eq "Completed") {
            Write-Host "[FRONTEND] Server stopped: $($FrontendJob.State)" -ForegroundColor $errorColor
            Receive-Job -Job $FrontendJob | ForEach-Object { Write-Host "[FRONTEND] $_" -ForegroundColor $frontendColor }
            return $false
        }
        
        # If both are running, we're good
        if ($backendStarted -and $frontendStarted) {
            Write-Host "`n[SUCCESS] Both servers are running!" -ForegroundColor $infoColor
            return $true
        }
        
        # Wait a bit before checking again
        Start-Sleep -Seconds 1
    }
    
    # If we reach here, we've timed out
    Write-Host "`n[ERROR] Timeout waiting for servers to start" -ForegroundColor $errorColor
    return $false
}

# Open browser when servers are ready
function Open-ApplicationInBrowser {
    $url = "http://localhost:3000"
    Write-Host "`n[OPEN] Opening application in browser: $url" -ForegroundColor $infoColor
    Start-Process $url
}

# Cleanup on exit
function Stop-AllJobs {
    param (
        [Parameter(Mandatory=$true)]
        [System.Management.Automation.Job]$BackendJob,
        
        [Parameter(Mandatory=$true)]
        [System.Management.Automation.Job]$FrontendJob
    )
    
    Write-Host "`n[CLEANUP] Stopping all servers..." -ForegroundColor $infoColor
    
    # Stop all jobs
    Stop-Job -Job $BackendJob -ErrorAction SilentlyContinue
    Stop-Job -Job $FrontendJob -ErrorAction SilentlyContinue
    
    # Remove all jobs
    Remove-Job -Job $BackendJob -Force -ErrorAction SilentlyContinue
    Remove-Job -Job $FrontendJob -Force -ErrorAction SilentlyContinue
    
    Write-Host "[CLEANUP] All servers stopped" -ForegroundColor $infoColor
}

# Main execution
try {
    # Start the backend server
    $backendJob = Start-BackendServer
    
    # Wait a moment to let backend initialize
    Write-Host "`n[WAIT] Waiting for backend to initialize..." -ForegroundColor $infoColor
    Start-Sleep -Seconds 5
    
    # Start the frontend server
    $frontendJob = Start-FrontendServer
    
    # Monitor jobs
    $success = Monitor-Jobs -BackendJob $backendJob -FrontendJob $frontendJob
    
    if ($success) {
        # Open the application in browser
        Open-ApplicationInBrowser
        
        # Print success message with how to stop
        Write-Host "`n=== Servers Running Successfully ===" -ForegroundColor $infoColor
        Write-Host "To stop the servers, press CTRL+C or close this window" -ForegroundColor $infoColor
        Write-Host "Backend: http://localhost:8000" -ForegroundColor $backendColor
        Write-Host "Frontend: http://localhost:3000" -ForegroundColor $frontendColor
        Write-Host "================================================`n" -ForegroundColor $infoColor
        
        # Keep the script running
        Write-Host "Press CTRL+C to stop all servers..." -ForegroundColor $infoColor
        try {
            while ($true) {
                Start-Sleep -Seconds 1
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