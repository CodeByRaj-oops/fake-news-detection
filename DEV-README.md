# Developer Guide - Running the Fake News Detection App

This guide provides instructions for running the development server and avoiding the "Missing script: 'dev'" error.

## Running the Development Server

### BEST METHOD (Recommended): Using the All-in-One Script

The most reliable way to run the development server is by using our comprehensive monitoring script:

```
powershell -ExecutionPolicy Bypass -File run-all.ps1
```

This script:
- Starts both backend and frontend servers in monitored processes
- Handles proper directory navigation and environment setup
- Automatically installs missing dependencies
- Monitors server health and auto-restarts if needed
- Opens the browser once everything is running
- Provides clear, color-coded logging for easy troubleshooting

### Alternative Methods:

### Backend Server

To start the backend server, run one of the following commands from the project root:

```bash
# Using Python directly
python backend/app_new.py

# Or using uvicorn
uvicorn backend.app_new:app --reload
```

### Frontend Server

#### Option 1: Using Command Prompt

```
npm-dev.cmd
```

This batch file:
- Checks if the frontend directory exists
- Verifies package.json is present
- Changes to the frontend directory
- Runs `npm run dev`

#### Option 2: Using PowerShell

```
.\run-dev.ps1
```

This PowerShell script:
- Changes to the frontend directory
- Runs the development server

#### Option 3: Direct Approach

```bash
cd frontend
npm run dev
```

#### Option 4: From Project Root

```bash
npm run dev
```

## Troubleshooting

If you encounter the "Missing script: 'dev'" error:

1. Run the fix script: `.\fix-and-run.ps1`
2. This will:
   - Check and fix both package.json files
   - Create helper scripts
   - Offer to start the development server

## File Descriptions

- `fix-and-run.ps1`: Comprehensive script that fixes package.json files and creates helper scripts
- `run-dev.ps1`: PowerShell script to run the frontend dev server
- `npm-dev.cmd`: Command Prompt batch file to run the frontend dev server

## Project Structure

```
├── backend/             # FastAPI backend with ML model
├── frontend/            # React frontend application
├── fix-and-run.ps1      # Script to fix package.json issues
├── run-dev.ps1          # Script to run frontend dev server
├── npm-dev.cmd          # Batch file to run frontend dev server
└── package.json         # Root package.json with dev script
``` 