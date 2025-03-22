# PowerShell script to fix connection issues and start both servers properly
Write-Host "=== Fixing Frontend/Backend Connection Issues ===" -ForegroundColor Cyan

# 1. Install Python dependencies first
Write-Host "`n[1/4] Setting up backend..." -ForegroundColor Green
Push-Location backend

# Install setuptools first (for distutils problem)
Write-Host "Installing setuptools (needed for distutils in Python 3.13+)..." -ForegroundColor Yellow
py -m pip install setuptools wheel --upgrade

# Install required packages
Write-Host "Installing key backend dependencies..." -ForegroundColor Yellow
py -m pip install fastapi uvicorn pydantic python-multipart httpx numpy pandas scikit-learn

# Create required directories
if (-not (Test-Path "history")) { New-Item -ItemType Directory -Path "history" | Out-Null }
if (-not (Test-Path "reports")) { New-Item -ItemType Directory -Path "reports" | Out-Null }

Pop-Location

# 2. Fix frontend package.json proxy setting
Write-Host "`n[2/4] Fixing frontend configuration..." -ForegroundColor Yellow
Push-Location frontend

# Update package.json to ensure proxy is set correctly
if (Test-Path "package.json") {
    $packageJson = Get-Content "package.json" -Raw | ConvertFrom-Json
    
    # Set proxy to backend URL
    if (-not ($packageJson.PSObject.Properties.Name -contains "proxy") -or 
        $packageJson.proxy -ne "http://localhost:8000") {
        
        Write-Host "Setting proxy to http://localhost:8000..." -ForegroundColor Yellow
        $packageJson | Add-Member -Name "proxy" -Value "http://localhost:8000" -MemberType NoteProperty -Force
        $packageJson | ConvertTo-Json -Depth 10 | Set-Content "package.json"
    }
}

Pop-Location

# 3. Start backend server in a new window
Write-Host "`n[3/4] Starting backend server..." -ForegroundColor Green
$backendCmd = "cd '$((Get-Location).Path)\backend'; py app_new.py"
Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendCmd

# 4. Wait a moment for backend to start, then start frontend
Write-Host "Waiting for backend to initialize (5 seconds)..." -ForegroundColor Cyan
Start-Sleep -Seconds 5

Write-Host "`n[4/4] Starting frontend server..." -ForegroundColor Yellow
$frontendCmd = "cd '$((Get-Location).Path)\frontend'; npm run dev"
Start-Process powershell -ArgumentList "-NoExit", "-Command", $frontendCmd

# Final message
Write-Host "`n=== Servers Started ===`n" -ForegroundColor Cyan
Write-Host "Both servers are now running in separate windows:" -ForegroundColor White
Write-Host " • Frontend: http://localhost:3000" -ForegroundColor Yellow
Write-Host " • Backend: http://localhost:8000" -ForegroundColor Green
Write-Host "`nIf you still experience connection issues:" -ForegroundColor White
Write-Host "1. Check that both server windows are running" -ForegroundColor Cyan
Write-Host "2. Verify the backend shows no errors" -ForegroundColor Cyan
Write-Host "3. Refresh the frontend page" -ForegroundColor Cyan

Write-Host "`nPress any key to exit this launcher..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 