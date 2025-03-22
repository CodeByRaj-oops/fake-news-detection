/**
 * checkRouters.js
 * Script to check for potential nested router issues in React components
 * 
 * This script can be run as part of the build process or development workflow
 * to identify potential Router nesting issues before they cause runtime errors.
 */

const fs = require('fs');
const path = require('path');

// Define patterns to search for in files
const routerImportPattern = /import\s+.*?(?:BrowserRouter|Router|HashRouter|MemoryRouter|NativeRouter|StaticRouter).*?from\s+['"]react-router-dom['"]/;
const routerUsagePattern = /<(?:BrowserRouter|Router|HashRouter|MemoryRouter|NativeRouter|StaticRouter)[^>]*>/g;

// Directories to ignore
const ignoreDirs = ['node_modules', 'build', 'dist', '.git'];

// Files or patterns to ignore
const ignoreFiles = [
  'index.js', // Main entry point file is allowed to have a router
  '.test.', '.spec.', // Test files
  'RouterValidator.js', // Our validator file
  'checkRouters.js' // This file
];

// Track found routers
const foundRouters = [];

/**
 * Check if file should be ignored
 * @param {string} filePath 
 * @returns {boolean}
 */
function shouldIgnoreFile(filePath) {
  const relativePath = filePath.split(path.sep).join('/');
  return ignoreFiles.some(pattern => relativePath.includes(pattern));
}

/**
 * Walk directory and check files
 * @param {string} dir Directory to search
 */
function walk(dir) {
  const files = fs.readdirSync(dir);
  
  files.forEach(file => {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);
    
    if (stat.isDirectory() && !ignoreDirs.includes(file)) {
      walk(filePath);
    } else if (stat.isFile() && /\.(js|jsx|tsx)$/.test(file) && !shouldIgnoreFile(filePath)) {
      checkFile(filePath);
    }
  });
}

/**
 * Check a file for Router components
 * @param {string} filePath 
 */
function checkFile(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    
    // Check if file imports a router component
    if (routerImportPattern.test(content)) {
      // Check if file uses a router component
      const routerMatches = content.match(routerUsagePattern);
      
      if (routerMatches) {
        foundRouters.push({
          file: filePath,
          count: routerMatches.length,
          matches: routerMatches
        });
      }
    }
  } catch (error) {
    console.error(`Error processing file ${filePath}:`, error.message);
  }
}

/**
 * Run the router check
 * @param {string} sourceDir Directory to start search from
 * @returns {Array} Found routers
 */
function checkForRouters(sourceDir) {
  const startDir = sourceDir || path.join(process.cwd(), 'src');
  console.log(`Checking for Router components in: ${startDir}`);
  
  foundRouters.length = 0; // Reset array
  walk(startDir);
  
  // Print results
  if (foundRouters.length > 0) {
    console.log('\n🚨 Potential Router nesting issues found:');
    foundRouters.forEach(({ file, count, matches }) => {
      console.log(`\nFile: ${file}`);
      console.log(`Router instances: ${count}`);
      console.log('Matches:');
      matches.forEach(match => console.log(`  - ${match}`));
    });
    
    console.log('\n⚠️ Warning: Multiple Router components can cause "You cannot render a <Router> inside another <Router>" error.');
    console.log('📝 Fix: Ensure you have only ONE <BrowserRouter>, typically in index.js.\n');
    
    if (foundRouters.length > 1) {
      console.log('❌ Found multiple files with Router components.');
      return { success: false, routers: foundRouters };
    } else {
      console.log('✅ Only one file with Router components found. This is likely correct.');
      return { success: true, routers: foundRouters };
    }
  } else {
    console.log('\n✅ No Router components found. Make sure you have at least one <BrowserRouter> in your app (typically in index.js).');
    return { success: true, routers: [] };
  }
}

// Run check if script is executed directly
if (require.main === module) {
  checkForRouters();
}

module.exports = {
  checkForRouters
}; 