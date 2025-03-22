# PowerShell script to fix connection issues between the backend and frontend
Write-Host "`n=== Backend Connection Fixer ===`n" -ForegroundColor Cyan
Write-Host "This script will diagnose and fix backend-frontend connection issues" -ForegroundColor Cyan

# Step 1: Check if backend directory exists
Write-Host "`n[1/6] Checking backend directory..." -ForegroundColor Green
if (-not (Test-Path "backend")) {
    Write-Host "❌ Backend directory not found. Make sure you're in the correct project root." -ForegroundColor Red
    exit 1
} else {
    Write-Host "✓ Backend directory found." -ForegroundColor Green
}

# Step 2: Check if frontend directory exists
Write-Host "`n[2/6] Checking frontend directory..." -ForegroundColor Yellow
if (-not (Test-Path "frontend")) {
    Write-Host "❌ Frontend directory not found. Make sure you're in the correct project root." -ForegroundColor Red
    exit 1
} else {
    Write-Host "✓ Frontend directory found." -ForegroundColor Yellow
}

# Step 3: Update the frontend API configuration
Write-Host "`n[3/6] Updating frontend API configuration..." -ForegroundColor Yellow
$apiFilePath = "frontend/src/api/newsApi.js"
if (Test-Path $apiFilePath) {
    $apiContent = Get-Content $apiFilePath -Raw
    $updatedApiContent = $apiContent -replace '(timeout: )\d+', 'timeout: 30000'
    
    if ($apiContent -ne $updatedApiContent) {
        Set-Content -Path $apiFilePath -Value $updatedApiContent
        Write-Host "✓ Updated API timeout settings in newsApi.js" -ForegroundColor Yellow
    } else {
        Write-Host "✓ API timeout settings already configured correctly." -ForegroundColor Yellow
    }
} else {
    Write-Host "❌ API file not found. Check project structure." -ForegroundColor Red
}

# Step 4: Update frontend package.json proxy settings
Write-Host "`n[4/6] Updating frontend proxy settings..." -ForegroundColor Yellow
$packageJsonPath = "frontend/package.json"
if (Test-Path $packageJsonPath) {
    $packageJson = Get-Content $packageJsonPath -Raw | ConvertFrom-Json
    $hasChanged = $false
    
    if (-not (Get-Member -InputObject $packageJson -Name "proxy" -MemberType Properties) -or 
        $packageJson.proxy -ne "http://localhost:8000") {
        $packageJson | Add-Member -Name "proxy" -Value "http://localhost:8000" -MemberType NoteProperty -Force
        $hasChanged = $true
    }
    
    if ($hasChanged) {
        $packageJson | ConvertTo-Json -Depth 10 | Set-Content $packageJsonPath
        Write-Host "✓ Updated proxy settings in package.json" -ForegroundColor Yellow
    } else {
        Write-Host "✓ Proxy settings already configured correctly." -ForegroundColor Yellow
    }
} else {
    Write-Host "❌ package.json not found. Check project structure." -ForegroundColor Red
}

# Step 5: Fix CORS in backend
Write-Host "`n[5/6] Updating backend CORS settings..." -ForegroundColor Green
$backendAppPath = "backend/app_new.py"
if (Test-Path $backendAppPath) {
    $appContent = Get-Content $backendAppPath -Raw
    
    # Check if CORS middleware is already properly configured
    if ($appContent -match "CORSMiddleware" -and 
        -not ($appContent -match "allow_origins=\[.*(localhost:3000|127.0.0.1:3000).*\]")) {
        
        # Replace the CORS configuration with a proper one
        $newCorsConfig = @"
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "*"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "Accept", "Origin", "X-Requested-With"],
    max_age=3600,  # Cache preflight requests for 1 hour
)
"@
        
        $updatedContent = $appContent -replace "app\.add_middleware\(\s*CORSMiddleware[\s\S]*?\)", $newCorsConfig
        
        if ($appContent -ne $updatedContent) {
            Set-Content -Path $backendAppPath -Value $updatedContent
            Write-Host "✓ Updated CORS configuration in app_new.py" -ForegroundColor Green
        }
    } else {
        Write-Host "✓ CORS configuration appears to be correct already." -ForegroundColor Green
    }
    
    # Check for health endpoint
    if (-not ($appContent -match "@app\.get\(\s*['\"]\/health['\"]")) {
        $healthEndpoint = @"

@app.get("/health", tags=["General"])
async def health_check():
    """API health check endpoint"""
    return {
        "status": "ok",
        "service": "fake-news-detection-backend",
        "version": "2.0.0",
        "timestamp": datetime.now().isoformat()
    }
"@
        
        # We need to find a good place to insert it - after the root endpoint is ideal
        if ($appContent -match "@app\.get\(\s*['\"]\/['\"][\s\S]*?\)\s*\n") {
            $updatedContent = $appContent -replace "(@app\.get\(\s*['\"]\/['\"][\s\S]*?\)\s*\n)", "`$1$healthEndpoint`n"
            
            if ($appContent -ne $updatedContent) {
                Set-Content -Path $backendAppPath -Value $updatedContent
                Write-Host "✓ Added health check endpoint to app_new.py" -ForegroundColor Green
            }
        } else {
            Write-Host "⚠️ Couldn't find a suitable place to add health endpoint. Manual addition may be required." -ForegroundColor Yellow
        }
    } else {
        Write-Host "✓ Health check endpoint already exists." -ForegroundColor Green
    }
} else {
    Write-Host "❌ Backend app file not found. Check project structure." -ForegroundColor Red
}

# Step 6: Create fixed startup script
Write-Host "`n[6/6] Creating improved startup script..." -ForegroundColor Cyan
$startupScript = @"
# Simplified PowerShell script to run both backend and frontend
Write-Host "`n=== Fake News Detection System ===`n" -ForegroundColor Cyan
Write-Host "Starting both servers with proper configuration..." -ForegroundColor Cyan

# Start backend in a new window
Write-Host "`nStarting backend server..." -ForegroundColor Green
Start-Process -FilePath "powershell.exe" -ArgumentList "-NoExit", "-Command", "cd '$((Get-Location).Path)\backend'; python app_new.py"

# Wait for backend to initialize
Write-Host "Waiting for backend to initialize (5 seconds)..." -ForegroundColor Cyan
Start-Sleep -Seconds 5

# Start frontend in a new window
Write-Host "`nStarting frontend server..." -ForegroundColor Yellow
Start-Process -FilePath "powershell.exe" -ArgumentList "-NoExit", "-Command", "cd '$((Get-Location).Path)\frontend'; npm run dev"

Write-Host "`nBoth servers should now be starting in separate windows." -ForegroundColor Cyan
Write-Host "Once they're running, access the application at: http://localhost:3000" -ForegroundColor Cyan
Write-Host "Backend API is available at: http://localhost:8000" -ForegroundColor Cyan
"@

$startupScriptPath = "start-app.ps1"
Set-Content -Path $startupScriptPath -Value $startupScript
Write-Host "✓ Created improved startup script: start-app.ps1" -ForegroundColor Cyan

# Final instructions
Write-Host "`n=== Fix Complete ===`n" -ForegroundColor Cyan
Write-Host "To run the application with all fixes applied:" -ForegroundColor White
Write-Host "   powershell -ExecutionPolicy Bypass -File start-app.ps1" -ForegroundColor Yellow
Write-Host "`nTroubleshooting tips:" -ForegroundColor White
Write-Host "1. If the API still fails to connect, try restarting both servers." -ForegroundColor Cyan
Write-Host "2. Ensure ports 3000 and 8000 are not in use by other applications." -ForegroundColor Cyan
Write-Host "3. Check browser console for specific error messages." -ForegroundColor Cyan
Write-Host "4. If using Python 3.13+, ensure distutils is installed (pip install setuptools)." -ForegroundColor Cyan

Write-Host "`nPress any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")