# Simple PowerShell script to navigate to frontend directory and run the server
Write-Host "Starting frontend server..." -ForegroundColor Cyan

# Navigate to frontend directory if needed
if (Test-Path "frontend\package.json") {
    Set-Location "frontend"
    Write-Host "Found package.json in frontend directory" -ForegroundColor Green
} elseif (Test-Path "..\frontend\package.json") {
    Set-Location "..\frontend"
    Write-Host "Found package.json in parent frontend directory" -ForegroundColor Green
} elseif (-not (Test-Path "package.json")) {
    Write-Host "ERROR: Cannot find package.json in current, frontend, or parent frontend directory" -ForegroundColor Red
    exit 1
}

# Check if package.json has a dev script
$packageJson = Get-Content "package.json" -Raw | ConvertFrom-Json
if (-not (Get-Member -InputObject $packageJson.scripts -Name "dev" -MemberType Properties)) {
    Write-Host "Adding dev script to package.json..." -ForegroundColor Yellow
    $packageJson.scripts | Add-Member -Name "dev" -Value "react-scripts start" -MemberType NoteProperty -Force
    $packageJson | ConvertTo-Json -Depth 10 | Set-Content "package.json"
}

# Run the dev server
Write-Host "Running frontend development server..." -ForegroundColor Green
npm run dev

# Keep the console open when done
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 