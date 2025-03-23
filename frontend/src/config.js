/**
 * Frontend application configuration
 * Contains API endpoints and other global settings
 */
const config = {
  // Backend API URL
  apiUrl: 'http://localhost:8001',
  
  // API endpoints
  endpoints: {
    // Core endpoints
    analyze: '/analyze',
    enhancedAnalyze: '/analyze/enhanced',
    history: '/history',
    health: '/health',
    explain: '/explain',
    
    // Additional endpoints
    explainMethods: '/explain/methods',
    detectLanguage: '/detect-language',
    historyItem: (id) => `/history/${id}`,
    report: (id) => `/reports/${id}`,
  },
  
  // Default request timeout in milliseconds
  timeout: 30000,
  
  // Retry configuration
  retry: {
    attempts: 3,
    delay: 1000,
  }
};

export default config; 
