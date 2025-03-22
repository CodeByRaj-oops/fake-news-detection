# PowerShell script to run both frontend and backend
# Use Start-Process to run the backend in a new window
Start-Process powershell -ArgumentList "-File `"$PSScriptRoot\run-backend.ps1`""

# Run the frontend in the current window
Write-Host "Starting frontend..." -ForegroundColor Green
Set-Location -Path .\frontend
npm run dev 