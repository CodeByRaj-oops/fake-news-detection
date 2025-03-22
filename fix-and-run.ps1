# PowerShell script to fix all issues and run the frontend
Write-Host "=== Comprehensive Fix for Frontend Project ===" -ForegroundColor Cyan
Write-Host "This script will fix the 'Missing script: dev' error and run the development server." -ForegroundColor Cyan
Write-Host "----------------------------------------------" -ForegroundColor Cyan

# Step 1: Fix package.json files
Write-Host "`nStep 1: Checking and fixing package.json files..." -ForegroundColor Yellow

# Check if the files exist
if (-not (Test-Path ".\frontend\package.json")) {
    Write-Host "  Error: frontend/package.json not found!" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path ".\package.json")) {
    Write-Host "  Error: root package.json not found!" -ForegroundColor Red
    exit 1
}

# Fix frontend package.json
Write-Host "  Checking frontend package.json..." -ForegroundColor Yellow
$frontendPackageJson = Get-Content -Path ".\frontend\package.json" -Raw | ConvertFrom-Json
$frontendModified = $false

# Check if dev script exists in frontend
if (-not ($frontendPackageJson.scripts -and $frontendPackageJson.scripts.dev)) {
    Write-Host "  Adding dev script to frontend package.json" -ForegroundColor Yellow
    if (-not $frontendPackageJson.scripts) {
        $frontendPackageJson | Add-Member -Name "scripts" -Value @{} -MemberType NoteProperty
    }
    $frontendPackageJson.scripts | Add-Member -Name "dev" -Value "react-scripts start" -MemberType NoteProperty
    $frontendModified = $true
}

# Save frontend changes if needed
if ($frontendModified) {
    $frontendPackageJson | ConvertTo-Json -Depth 10 | Set-Content -Path ".\frontend\package.json"
    Write-Host "  Fixed frontend package.json successfully!" -ForegroundColor Green
} else {
    Write-Host "  Frontend package.json already has a dev script." -ForegroundColor Green
}

# Fix root package.json
Write-Host "  Checking root package.json..." -ForegroundColor Yellow
$rootPackageJson = Get-Content -Path ".\package.json" -Raw | ConvertFrom-Json
$rootModified = $false

# Check if dev script exists in root
if (-not ($rootPackageJson.scripts -and $rootPackageJson.scripts.dev)) {
    Write-Host "  Adding dev script to root package.json" -ForegroundColor Yellow
    if (-not $rootPackageJson.scripts) {
        $rootPackageJson | Add-Member -Name "scripts" -Value @{} -MemberType NoteProperty
    }
    $rootPackageJson.scripts | Add-Member -Name "dev" -Value "powershell -File .\run-dev.ps1" -MemberType NoteProperty
    $rootModified = $true
}

# Save root changes if needed
if ($rootModified) {
    $rootPackageJson | ConvertTo-Json -Depth 10 | Set-Content -Path ".\package.json"
    Write-Host "  Fixed root package.json successfully!" -ForegroundColor Green
} else {
    Write-Host "  Root package.json already has a dev script." -ForegroundColor Green
}

# Step 2: Create run-dev.ps1 script
Write-Host "`nStep 2: Creating helper scripts..." -ForegroundColor Yellow

# Create run-dev.ps1
$runDevContent = @'
# PowerShell script to run the frontend dev server
Write-Host "Starting frontend development server..." -ForegroundColor Green

# Change directory to frontend
Set-Location -Path .\frontend

# Run the development server
npm run dev

# Keep the console open
Write-Host "`nPress any key to exit..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
'@
Set-Content -Path ".\run-dev.ps1" -Value $runDevContent
Write-Host "  Created run-dev.ps1 script" -ForegroundColor Green

# Create npm-dev.cmd for Windows CMD
$npmDevCmdContent = @'
@echo off
echo Starting frontend development server...
powershell -ExecutionPolicy Bypass -File .\run-dev.ps1
'@
Set-Content -Path ".\npm-dev.cmd" -Value $npmDevCmdContent
Write-Host "  Created npm-dev.cmd for Windows CMD" -ForegroundColor Green

# Step 3: Run development server
Write-Host "`nStep 3: Ready to run the development server" -ForegroundColor Green
Write-Host "You can now run the development server using any of these methods:" -ForegroundColor White
Write-Host "  1. .\run-dev.ps1                (PowerShell)" -ForegroundColor White
Write-Host "  2. npm-dev.cmd                  (CMD)" -ForegroundColor White
Write-Host "  3. npm run dev                  (NPM)" -ForegroundColor White
Write-Host "  4. cd frontend; npm run dev     (Direct)" -ForegroundColor White

Write-Host "`nDo you want to start the development server now? (Y/N)" -ForegroundColor Yellow
$response = $Host.UI.ReadLine()

if ($response -eq "Y" -or $response -eq "y") {
    Write-Host "`nStarting the development server..." -ForegroundColor Green
    & .\run-dev.ps1
} else {
    Write-Host "`nYou can start the server later using one of the methods above." -ForegroundColor White
    Write-Host "Press any key to exit..." -ForegroundColor Yellow
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
} 