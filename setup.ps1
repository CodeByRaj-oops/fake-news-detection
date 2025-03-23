# PowerShell Setup script for Fake News Detection project

Write-Host "Installing root dependencies..." -ForegroundColor Green
npm install

Write-Host "Installing frontend dependencies..." -ForegroundColor Green
cd frontend
npm install
cd ..

Write-Host "Installing backend dependencies..." -ForegroundColor Green
cd backend
npm install
cd ..

Write-Host "Installing Python dependencies..." -ForegroundColor Green
cd backend
# Create virtual environment if it doesn't exist
if (-not (Test-Path ".venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
}

# Activate virtual environment
try {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    if (Test-Path ".venv\Scripts\Activate.ps1") {
        & .venv\Scripts\Activate.ps1
    } else {
        & .venv\bin\Activate.ps1
    }
    
    # Install Python dependencies
    Write-Host "Installing Python packages..." -ForegroundColor Yellow
    pip install -r requirements.txt
}
catch {
    Write-Host "Error activating virtual environment: $_" -ForegroundColor Red
    Write-Host "Please run the following commands manually:" -ForegroundColor Red
    Write-Host ".venv\Scripts\Activate.ps1" -ForegroundColor Cyan
    Write-Host "pip install -r requirements.txt" -ForegroundColor Cyan
}

cd ..
Write-Host "Setup complete! Run 'npm run dev' to start the application." -ForegroundColor Green 