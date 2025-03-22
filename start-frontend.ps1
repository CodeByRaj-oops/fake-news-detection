# PowerShell script to start and monitor the frontend server
Write-Host "=== Starting Frontend Server ===`n" -ForegroundColor Cyan

# Ensure we are in the correct directory
function Set-FrontendDirectory {
    # Check if we're already in the frontend directory
    if ((Test-Path "package.json") -and ((Get-Content "package.json" -Raw) -match "fake-news-detector-frontend")) {
        return $true
    }
    
    # Try to find and navigate to frontend directory
    if ((Test-Path "frontend\package.json") -and ((Get-Content "frontend\package.json" -Raw) -match "fake-news-detector-frontend")) {
        Set-Location "frontend"
        return $true
    } elseif ((Test-Path "..\frontend\package.json") -and ((Get-Content "..\frontend\package.json" -Raw) -match "fake-news-detector-frontend")) {
        Set-Location "..\frontend"
        return $true
    } else {
        Write-Host "ERROR: Cannot find frontend directory with package.json" -ForegroundColor Red
        return $false
    }
}

# Verify and fix package.json dev script
function Ensure-DevScript {
    if (-not (Test-Path "package.json")) {
        Write-Host "ERROR: package.json not found" -ForegroundColor Red
        return $false
    }
    
    # Load package.json
    try {
        $packageJson = Get-Content "package.json" -Raw | ConvertFrom-Json
        
        # Check if scripts section exists
        if (-not (Get-Member -InputObject $packageJson -Name "scripts" -MemberType Properties)) {
            Write-Host "ERROR: No scripts section in package.json" -ForegroundColor Red
            return $false
        }
        
        # Check if dev script exists
        $hasDevScript = Get-Member -InputObject $packageJson.scripts -Name "dev" -MemberType Properties
        if (-not $hasDevScript) {
            # Add dev script
            Write-Host "Adding 'dev' script to package.json..." -ForegroundColor Yellow
            $packageJson.scripts | Add-Member -Name "dev" -Value "react-scripts start" -MemberType NoteProperty
            
            # Save updated package.json
            $packageJson | ConvertTo-Json -Depth 10 | Set-Content "package.json"
            Write-Host "Updated package.json with 'dev' script" -ForegroundColor Green
        }
        
        return $true
    } catch {
        Write-Host "ERROR: Failed to parse or update package.json - $_" -ForegroundColor Red
        return $false
    }
}

# Check for required files
function Ensure-RequiredFiles {
    # Check for public/index.html
    if (-not (Test-Path "public\index.html")) {
        if (-not (Test-Path "public")) {
            Write-Host "Creating 'public' directory..." -ForegroundColor Yellow
            New-Item -ItemType Directory -Path "public" | Out-Null
        }
        
        Write-Host "Creating minimal 'public/index.html'..." -ForegroundColor Yellow
        $htmlContent = @"
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <link rel="icon" href="%PUBLIC_URL%/favicon.ico" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta name="description" content="Fake News Detection System" />
    <link rel="manifest" href="%PUBLIC_URL%/manifest.json" />
    <title>Fake News Detector</title>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
  </body>
</html>
"@
        Set-Content -Path "public\index.html" -Value $htmlContent
    }
    
    # Check for manifest.json
    if (-not (Test-Path "public\manifest.json")) {
        Write-Host "Creating minimal 'public/manifest.json'..." -ForegroundColor Yellow
        $manifestContent = @"
{
  "short_name": "Fake News Detector",
  "name": "Fake News Detection System",
  "icons": [
    {
      "src": "favicon.ico",
      "sizes": "64x64 32x32 24x24 16x16",
      "type": "image/x-icon"
    }
  ],
  "start_url": ".",
  "display": "standalone",
  "theme_color": "#000000",
  "background_color": "#ffffff"
}
"@
        Set-Content -Path "public\manifest.json" -Value $manifestContent
    }
}

# Install dependencies
function Install-Dependencies {
    # Check if node_modules exists
    if (-not (Test-Path "node_modules")) {
        Write-Host "Installing npm dependencies..." -ForegroundColor Cyan
        npm install
        if ($LASTEXITCODE -ne 0) {
            Write-Host "ERROR: Failed to install dependencies" -ForegroundColor Red
            return $false
        }
        Write-Host "Successfully installed dependencies" -ForegroundColor Green
    }
    return $true
}

# Check if backend is running
function Test-BackendRunning {
    $backendURL = "http://localhost:8000/health"
    try {
        $response = Invoke-WebRequest -Uri $backendURL -TimeoutSec 5 -ErrorAction SilentlyContinue
        if ($response.StatusCode -eq 200) {
            Write-Host "Backend server is running" -ForegroundColor Green
            return $true
        }
    } catch {
        Write-Host "WARNING: Backend server is not running or not responding" -ForegroundColor Yellow
        return $false
    }
}

# Start the frontend server
function Start-FrontendServer {
    # Set environment variables for consistent port
    $env:PORT = 3000
    
    # Start the server
    Write-Host "`nStarting React development server..." -ForegroundColor Cyan
    npm run dev
}

# Main execution flow
if (-not (Set-FrontendDirectory)) {
    exit 1
}

if (-not (Ensure-DevScript)) {
    exit 1
}

Ensure-RequiredFiles

if (-not (Install-Dependencies)) {
    exit 1
}

# Check if backend is running before starting frontend
$backendRunning = Test-BackendRunning
if (-not $backendRunning) {
    Write-Host "WARNING: Backend server is not running. API requests may fail." -ForegroundColor Yellow
    Write-Host "TIP: Run 'start-backend.ps1' in another terminal window first" -ForegroundColor Yellow
    $confirmStart = Read-Host "Do you want to continue anyway? (Y/N)"
    if ($confirmStart -ne "Y" -and $confirmStart -ne "y") {
        Write-Host "Frontend server start aborted. Start the backend server first." -ForegroundColor Cyan
        exit 0
    }
}

# Start the frontend server
Start-FrontendServer 