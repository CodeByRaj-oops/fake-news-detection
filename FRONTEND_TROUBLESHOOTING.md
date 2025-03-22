# Frontend Troubleshooting Guide

## Common Issues and Solutions

### "Missing script: 'dev'" Error

This error occurs when the npm script you're trying to run doesn't exist in the package.json file.

**Solution:**
1. Check your package.json file in the frontend directory
2. Add the missing script:
   ```json
   "scripts": {
     "dev": "react-scripts start",
     // other scripts
   }
   ```

### "Could not find a required file. Name: index.html" Error

This error occurs when the React application can't find the index.html file in the expected location.

**Solution for Create React App (react-scripts):**
1. Ensure there's an index.html file in the `frontend/public` directory
2. The index.html must contain a div with id="root":
   ```html
   <div id="root"></div>
   ```

### PowerShell Command Syntax Errors

PowerShell doesn't support the `&&` operator for chaining commands like Bash does.

**Solution:**
1. Use PowerShell-specific command chaining:
   ```powershell
   cd frontend; npm run dev
   ```
2. Use our provided PowerShell scripts:
   ```powershell
   ./run-frontend.ps1
   ```

### Mixed Build Tool Configuration

Having mixed configuration files for different build tools (Vite and Create React App) can cause confusion.

**Solution:**
1. Decide which build tool you want to use (react-scripts or Vite)
2. If using Create React App (react-scripts):
   - Ensure the frontend/public directory has the required files (index.html, manifest.json)
   - Use "react-scripts start" for development

3. If using Vite:
   - Keep index.html in the frontend root directory
   - Use "vite" for development
   - Update package.json scripts accordingly

## Prevention Checklist

Before running your application, check:

- [ ] The `package.json` file contains all necessary scripts
- [ ] The correct public/static files exist in the appropriate directories
- [ ] Environment variables are correctly set in a `.env` file
- [ ] All dependencies are installed with `npm install`
- [ ] You're using the correct command syntax for your shell

## Quick Start Commands

### For PowerShell Users
```powershell
# Start frontend only
./run-frontend.ps1

# Start entire application (frontend + backend)
./run-full-app.ps1
```

### For Command Prompt Users
```cmd
cd frontend
npm run dev
```

### For Bash/Linux/Mac Users
```bash
cd frontend && npm run dev
``` 