/**
 * Backend Health Checker
 * 
 * This script periodically checks if the backend is running properly
 * and restarts it if there are issues.
 */

const http = require('http');
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

// Configuration
const PORT = process.env.PORT || 5000;
const CHECK_INTERVAL = 60000; // 1 minute
const MAX_FAILED_CHECKS = 3;
const LOG_DIR = path.join(__dirname, '..', 'logs');
const LOG_FILE = path.join(LOG_DIR, 'health-checker.log');
const IS_WINDOWS = process.platform === 'win32';

// Create log directory if it doesn't exist
if (!fs.existsSync(LOG_DIR)) {
  fs.mkdirSync(LOG_DIR, { recursive: true });
}

// Log function
function log(message) {
  const timestamp = new Date().toISOString();
  console.log(`[${timestamp}] ${message}`);
  fs.appendFileSync(LOG_FILE, `[${timestamp}] ${message}\n`);
}

// Run a command
function runCommand(command) {
  try {
    log(`Running command: ${command}`);
    execSync(command, { stdio: 'inherit', shell: true });
    return true;
  } catch (error) {
    log(`Command failed: ${error.message}`);
    return false;
  }
}

// Check backend health
function checkHealth() {
  return new Promise((resolve) => {
    const req = http.get(`http://localhost:${PORT}/health`, (res) => {
      let data = '';
      
      res.on('data', (chunk) => {
        data += chunk;
      });
      
      res.on('end', () => {
        if (res.statusCode === 200) {
          try {
            const healthData = JSON.parse(data);
            log(`Health check successful: ${healthData.status}`);
            resolve(true);
          } catch (error) {
            log(`Health check returned invalid JSON: ${error.message}`);
            resolve(false);
          }
        } else {
          log(`Health check failed with status code: ${res.statusCode}`);
          resolve(false);
        }
      });
    });
    
    req.on('error', (error) => {
      log(`Health check request failed: ${error.message}`);
      resolve(false);
    });
    
    // Set timeout for the request
    req.setTimeout(5000, () => {
      log('Health check request timed out');
      req.destroy();
      resolve(false);
    });
  });
}

// Restart backend
function restartBackend() {
  log('Attempting to restart backend...');
  
  // Check if using PM2
  try {
    const pmList = execSync('pm2 list', { stdio: 'pipe', shell: true }).toString();
    if (pmList.includes('fake-news-backend')) {
      log('Restarting backend with PM2...');
      return runCommand('pm2 restart fake-news-backend');
    }
  } catch (error) {
    log('PM2 not available, trying alternative restart method');
  }
  
  // Alternative restart method if PM2 is not available
  if (IS_WINDOWS) {
    // On Windows
    runCommand('taskkill /F /IM python.exe /FI "WINDOWTITLE eq fake-news-backend"');
    return runCommand('start /B cmd /C "cd backend && python app_new.py"');
  } else {
    // On Unix-like systems
    runCommand('pkill -f "python.*app_new.py"');
    return runCommand('cd backend && nohup python app_new.py > ../logs/backend.log 2>&1 &');
  }
}

// Main function
async function main() {
  log('Starting backend health checker...');
  
  let failedChecks = 0;
  
  // Run the health check periodically
  setInterval(async () => {
    const isHealthy = await checkHealth();
    
    if (isHealthy) {
      failedChecks = 0;
    } else {
      failedChecks++;
      log(`Failed health checks: ${failedChecks}/${MAX_FAILED_CHECKS}`);
      
      if (failedChecks >= MAX_FAILED_CHECKS) {
        log('Too many failed health checks, attempting to restart backend');
        const restartSuccess = restartBackend();
        
        if (restartSuccess) {
          log('Backend restart initiated successfully');
        } else {
          log('Failed to restart backend');
        }
        
        // Reset counter either way
        failedChecks = 0;
      }
    }
  }, CHECK_INTERVAL);
  
  log(`Health checker running, checking every ${CHECK_INTERVAL / 1000} seconds`);
}

// Run the main function
main().catch(error => {
  log(`Unhandled error: ${error.message}`);
}); 