/**
 * Backend Runner Script
 * 
 * This script ensures the backend is properly set up and running:
 * 1. Checks if PM2 is installed, installs it if missing
 * 2. Ensures Python dependencies are installed
 * 3. Creates necessary directories
 * 4. Starts the backend with PM2 for automatic restart
 */

const { execSync, spawn } = require('child_process');
const fs = require('fs');
const path = require('path');
const os = require('os');

// Configuration
const PORT = process.env.PORT || 5000;
const PYTHON_CMD = process.platform === 'win32' ? 'python' : 'python3';
const LOG_DIR = path.join(__dirname, '..', 'logs');
const IS_WINDOWS = process.platform === 'win32';

// Create log directory if it doesn't exist
if (!fs.existsSync(LOG_DIR)) {
  fs.mkdirSync(LOG_DIR, { recursive: true });
}

// Log function
function log(message) {
  const timestamp = new Date().toISOString();
  console.log(`[${timestamp}] ${message}`);
  fs.appendFileSync(path.join(LOG_DIR, 'backend-runner.log'), `[${timestamp}] ${message}\n`);
}

// Run a command and return its output
function runCommand(command, options = {}) {
  try {
    log(`Running command: ${command}`);
    return execSync(command, { 
      stdio: options.silent ? 'pipe' : 'inherit',
      shell: true,
      ...options
    }).toString().trim();
  } catch (error) {
    if (options.ignoreError) {
      log(`Command failed (ignored): ${error.message}`);
      return '';
    }
    log(`Command failed: ${error.message}`);
    throw error;
  }
}

// Check if PM2 is installed globally
function checkPM2() {
  try {
    runCommand('pm2 --version', { silent: true });
    log('PM2 is already installed');
    return true;
  } catch (error) {
    log('PM2 not found, will install it');
    return false;
  }
}

// Install PM2 globally
function installPM2() {
  try {
    log('Installing PM2 globally...');
    runCommand('npm install -g pm2');
    log('PM2 installed successfully');
    return true;
  } catch (error) {
    log(`Failed to install PM2: ${error.message}`);
    log('Trying to continue without PM2...');
    return false;
  }
}

// Install Python dependencies
function installPythonDependencies() {
  log('Installing Python dependencies...');
  if (fs.existsSync(path.join(__dirname, 'requirements.txt'))) {
    runCommand(`${PYTHON_CMD} -m pip install -r requirements.txt`);
    log('Python dependencies installed successfully');
  } else {
    log('requirements.txt not found, skipping Python dependencies installation');
  }
}

// Create necessary directories
function createDirectories() {
  const dirs = [
    path.join(__dirname, 'reports'),
    path.join(__dirname, 'history'),
    path.join(__dirname, 'models')
  ];
  
  dirs.forEach(dir => {
    if (!fs.existsSync(dir)) {
      log(`Creating directory: ${dir}`);
      fs.mkdirSync(dir, { recursive: true });
    }
  });
}

// Start backend with PM2
function startWithPM2() {
  log('Starting backend with PM2...');
  
  // Check if already running and stop it
  try {
    runCommand('pm2 delete fake-news-backend', { ignoreError: true, silent: true });
  } catch (error) {
    // Ignore error if process doesn't exist
  }
  
  // Start with ecosystem config if it exists
  if (fs.existsSync(path.join(__dirname, 'ecosystem.config.js'))) {
    runCommand('pm2 start ecosystem.config.js');
  } else {
    // Fallback to manual configuration
    runCommand(`pm2 start ${PYTHON_CMD} --name fake-news-backend -- app_new.py --watch`);
  }
  
  log('Backend started with PM2');
  
  // Save PM2 configuration to startup
  try {
    runCommand('pm2 save', { silent: true });
    log('PM2 configuration saved');
  } catch (error) {
    log('Failed to save PM2 configuration (non-critical)');
  }
}

// Start backend without PM2
function startWithoutPM2() {
  log('Starting backend directly...');
  
  const env = {
    ...process.env,
    PORT: PORT.toString()
  };
  
  const pythonProcess = spawn(PYTHON_CMD, ['app_new.py'], { 
    cwd: __dirname,
    env,
    stdio: 'inherit',
    shell: true
  });
  
  pythonProcess.on('close', (code) => {
    log(`Backend process exited with code ${code}`);
    
    if (code !== 0) {
      log('Backend crashed, restarting in 3 seconds...');
      setTimeout(() => startWithoutPM2(), 3000);
    }
  });
  
  process.on('SIGINT', () => {
    log('Received SIGINT, shutting down...');
    pythonProcess.kill('SIGINT');
    process.exit(0);
  });
  
  process.on('SIGTERM', () => {
    log('Received SIGTERM, shutting down...');
    pythonProcess.kill('SIGTERM');
    process.exit(0);
  });
  
  log(`Backend running on http://localhost:${PORT}`);
}

// Main function
async function main() {
  log('Starting backend runner...');
  
  // Create necessary directories
  createDirectories();
  
  // Install Python dependencies
  installPythonDependencies();
  
  // Check and install PM2
  let pm2Available = checkPM2();
  if (!pm2Available) {
    pm2Available = installPM2();
  }
  
  // Start the backend
  if (pm2Available) {
    startWithPM2();
  } else {
    startWithoutPM2();
  }
  
  log(`Backend should be available at http://localhost:${PORT}`);
  log(`Health check: http://localhost:${PORT}/health`);
  log(`API docs: http://localhost:${PORT}/docs`);
}

// Run the main function
main().catch(error => {
  log(`Unhandled error: ${error.message}`);
  process.exit(1);
}); 