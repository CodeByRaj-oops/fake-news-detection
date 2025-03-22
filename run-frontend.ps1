# Run the frontend development server
Set-Location -Path frontend

# Install missing dev dependencies
Write-Host "Installing missing dependencies..." -ForegroundColor Cyan
npm install @vitejs/plugin-react vite --save-dev

# Create public directory structure if it doesn't exist
if (-not (Test-Path public)) {
    Write-Host "Creating necessary public directory structure..." -ForegroundColor Cyan
    New-Item -ItemType Directory -Path public -Force | Out-Null
}

# Run the development server
Write-Host "Starting development server..." -ForegroundColor Green
npm run dev 