# Run frontend and backend concurrently using PowerShell jobs

# Function to handle job output
function Show-JobOutput {
    param (
        [Parameter(Mandatory = $true)]
        [string] $JobName
    )
    
    $job = Get-Job -Name $JobName -ErrorAction SilentlyContinue
    if ($job) {
        Receive-Job -Name $JobName -Keep | ForEach-Object {
            Write-Host "[$JobName] $_"
        }
    }
}

# Kill any existing jobs
Get-Job | Stop-Job
Get-Job | Remove-Job

# Start frontend job
$frontendJob = Start-Job -Name "Frontend" -ScriptBlock {
    Set-Location -Path "$using:PWD\frontend"
    npm run dev
}

# Start backend job (only if Python is installed)
try {
    $backendJob = Start-Job -Name "Backend" -ScriptBlock {
        Set-Location -Path "$using:PWD\backend"
        # Try different Python commands
        if (Get-Command "python" -ErrorAction SilentlyContinue) {
            python app_new.py
        } elseif (Get-Command "python3" -ErrorAction SilentlyContinue) {
            python3 app_new.py
        } elseif (Get-Command "py" -ErrorAction SilentlyContinue) {
            py app_new.py
        } else {
            Write-Host "Python is not installed or not in PATH. Please install Python to run the backend."
            exit 1
        }
    }
} catch {
    Write-Host "Failed to start backend job: $_"
}

# Monitor jobs
try {
    Write-Host "Running Frontend and Backend services. Press Ctrl+C to stop."
    while ($true) {
        Show-JobOutput -JobName "Frontend"
        Show-JobOutput -JobName "Backend"
        Start-Sleep -Seconds 1
    }
} finally {
    # Clean up jobs on exit
    Get-Job | Stop-Job
    Get-Job | Remove-Job
    Write-Host "Services stopped."
} 