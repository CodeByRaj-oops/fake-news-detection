# PowerShell script to fix the "Missing script: 'dev'" error
Write-Host "Checking and fixing package.json files..." -ForegroundColor Cyan

# Check if frontend package.json exists
if (-not (Test-Path .\frontend\package.json)) {
    Write-Host "Error: frontend/package.json not found!" -ForegroundColor Red
    exit 1
}

# Function to ensure the dev script exists in package.json
function Ensure-DevScript {
    param (
        [string]$PackageJsonPath,
        [string]$DevCommand
    )
    
    Write-Host "Checking $PackageJsonPath..." -ForegroundColor Yellow
    
    try {
        # Read the package.json file
        $packageJson = Get-Content -Path $PackageJsonPath -Raw | ConvertFrom-Json
        
        # Check if the scripts object exists
        if (-not (Get-Member -InputObject $packageJson -Name "scripts" -MemberType Properties)) {
            Write-Host "Adding scripts object to $PackageJsonPath" -ForegroundColor Yellow
            $packageJson | Add-Member -Name "scripts" -Value (@{}) -MemberType NoteProperty
        }
        
        # Check if the dev script exists
        $scriptsModified = $false
        if (-not (Get-Member -InputObject $packageJson.scripts -Name "dev" -MemberType Properties)) {
            Write-Host "Adding dev script to $PackageJsonPath" -ForegroundColor Yellow
            $packageJson.scripts | Add-Member -Name "dev" -Value $DevCommand -MemberType NoteProperty
            $scriptsModified = $true
        }
        
        # If scripts were modified, write the changes back to the file
        if ($scriptsModified) {
            $packageJson | ConvertTo-Json -Depth 10 | Set-Content -Path $PackageJsonPath
            Write-Host "Fixed $PackageJsonPath successfully!" -ForegroundColor Green
        } else {
            Write-Host "$PackageJsonPath already has a dev script." -ForegroundColor Green
        }
        
        return $true
    } catch {
        Write-Host "Error processing $PackageJsonPath: $_" -ForegroundColor Red
        return $false
    }
}

# Check and fix the frontend package.json
$frontendFixed = Ensure-DevScript -PackageJsonPath ".\frontend\package.json" -DevCommand "react-scripts start"

# Check and fix the root package.json
$rootFixed = Ensure-DevScript -PackageJsonPath ".\package.json" -DevCommand "pwsh -File .\run-dev.ps1"

# Create npm-dev.cmd file for Windows CMD compatibility
$npmDevCmdContent = @"
@echo off
powershell -ExecutionPolicy Bypass -File .\run-dev.ps1
"@
Set-Content -Path ".\npm-dev.cmd" -Value $npmDevCmdContent
Write-Host "Created npm-dev.cmd for Windows CMD compatibility" -ForegroundColor Green

if ($frontendFixed -and $rootFixed) {
    Write-Host "`nAll package.json files have been checked and fixed." -ForegroundColor Green
    Write-Host "You can now run the dev server using any of these methods:" -ForegroundColor Cyan
    Write-Host "  1. .\run-dev.ps1                   (PowerShell)" -ForegroundColor White
    Write-Host "  2. npm-dev.cmd                     (Windows CMD)" -ForegroundColor White
    Write-Host "  3. cd frontend; npm run dev        (PowerShell)" -ForegroundColor White
} else {
    Write-Host "`nThere were some issues fixing the package.json files." -ForegroundColor Red
    Write-Host "Please check the error messages above." -ForegroundColor Red
}

Write-Host "`nPress any key to continue..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 