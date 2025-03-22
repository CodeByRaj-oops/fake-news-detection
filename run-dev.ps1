# PowerShell script to run the frontend dev server
Write-Host "Starting frontend development server..." -ForegroundColor Green

# Change directory to frontend
Set-Location -Path .\frontend

# Run the development server
npm run dev

# Keep the console open
Write-Host "`nPress any key to exit..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
