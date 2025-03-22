# PowerShell script to validate and fix package.json scripts
Write-Host "Validating package.json files..." -ForegroundColor Cyan

# Check root package.json
$rootPackageJson = Get-Content -Path .\package.json -Raw | ConvertFrom-Json
$scriptsModified = $false

# Check if 'dev' script exists in root package.json
if (-not $rootPackageJson.scripts.dev) {
    Write-Host "Adding missing 'dev' script to root package.json..." -ForegroundColor Yellow
    $rootPackageJson.scripts | Add-Member -Name "dev" -Value "cd frontend && npm run dev" -MemberType NoteProperty
    $scriptsModified = $true
}

# Save changes to root package.json if needed
if ($scriptsModified) {
    $rootPackageJson | ConvertTo-Json -Depth 10 | Set-Content -Path .\package.json
    Write-Host "Root package.json updated successfully." -ForegroundColor Green
} else {
    Write-Host "Root package.json is valid." -ForegroundColor Green
}

# Check frontend package.json
if (Test-Path -Path .\frontend\package.json) {
    $frontendPackageJson = Get-Content -Path .\frontend\package.json -Raw | ConvertFrom-Json
    $frontendScriptsModified = $false

    # Check if 'dev' script exists in frontend package.json
    if (-not $frontendPackageJson.scripts.dev) {
        Write-Host "Adding missing 'dev' script to frontend package.json..." -ForegroundColor Yellow
        $frontendPackageJson.scripts | Add-Member -Name "dev" -Value "react-scripts start" -MemberType NoteProperty
        $frontendScriptsModified = $true
    }

    # Save changes to frontend package.json if needed
    if ($frontendScriptsModified) {
        $frontendPackageJson | ConvertTo-Json -Depth 10 | Set-Content -Path .\frontend\package.json
        Write-Host "Frontend package.json updated successfully." -ForegroundColor Green
    } else {
        Write-Host "Frontend package.json is valid." -ForegroundColor Green
    }
} else {
    Write-Host "Warning: frontend package.json not found." -ForegroundColor Red
}

Write-Host "Package.json validation completed." -ForegroundColor Cyan 