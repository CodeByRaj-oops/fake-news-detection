import axios from 'axios';

// Create axios instance with base URL and additional configuration
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
  // Increased timeout for slow connections/initial startup
  timeout: 60000,
  // Add withCredentials to ensure cookies are sent if needed
  withCredentials: true,
});

// Maximum number of retries for failed requests
const MAX_RETRIES = 3;
// Delay between retries in milliseconds (starts at 1s, increases with each retry)
const RETRY_DELAY = 1000;

/**
 * Makes an API request with automatic retry on network errors
 * @param {Function} apiCall - The API call function to execute
 * @returns {Promise} - Promise with the API response or error
 */
async function makeRequestWithRetry(apiCall) {
  let retries = 0;
  let lastError = null;

  while (retries < MAX_RETRIES) {
    try {
      return await apiCall();
    } catch (error) {
      lastError = error;
      
      // Only retry on network errors or timeout, not on 4xx or 5xx responses
      if (!error.response && retries < MAX_RETRIES - 1) {
        // Capture retries in a local constant to avoid ESLint warning
        const currentRetry = retries + 1;
        console.log(`Request failed. Retrying (${currentRetry}/${MAX_RETRIES})...`);
        
        // Increment retries count
        retries++;
        
        // Wait with exponential backoff before retrying
        await new Promise(resolve => 
          setTimeout(resolve, RETRY_DELAY * Math.pow(2, currentRetry - 1))
        );
      } else {
        // If it's a response error or we've exhausted retries, throw the error
        break;
      }
    }
  }
  
  // If all retries fail, handle the error
  throw handleApiError(lastError);
}

// API functions for news analysis
export const analyzeText = async (text, detailed = false, saveReport = false, 
                                 explain = false, explanationMethod = 'lime', numFeatures = 10) => {
  return makeRequestWithRetry(() => 
    api.post('/analyze', {
      text,
      detailed,
      save_report: saveReport,
      explain,
      explanation_method: explanationMethod,
      num_features: numFeatures
    })
  ).then(response => response.data);
};

// Get analysis history
export const getHistory = async (limit = 10, offset = 0) => {
  return makeRequestWithRetry(() => 
    api.get(`/history?limit=${limit}&offset=${offset}`)
  ).then(response => response.data);
};

// Get specific history item
export const getHistoryItem = async (historyId) => {
  return makeRequestWithRetry(() => 
    api.get(`/history/${historyId}`)
  ).then(response => response.data);
};

// Get reports list
export const getReports = async (limit = 10, offset = 0) => {
  return makeRequestWithRetry(() => 
    api.get(`/reports?limit=${limit}&offset=${offset}`)
  ).then(response => response.data);
};

// Get specific report
export const getReport = async (reportId) => {
  return makeRequestWithRetry(() => 
    api.get(`/reports/${reportId}`)
  ).then(response => response.data);
};

// Get explanation method options
export const getExplanationMethods = async () => {
  return makeRequestWithRetry(() => 
    api.get('/explain/methods')
  ).then(response => response.data.methods);
};

// Generate explanation for text
export const explainText = async (text, method = 'lime', numFeatures = 10) => {
  return makeRequestWithRetry(() => 
    api.post('/explain', {
      text,
      method,
      num_features: numFeatures
    })
  ).then(response => response.data);
};

// Check if backend server is available
export const checkServerStatus = async () => {
  try {
    const response = await api.get('/health', { timeout: 3000 });
    return { online: true, status: response.status };
  } catch (error) {
    if (error.response) {
      // Server responded with non-2xx status
      return { online: true, status: error.response.status };
    } else {
      // No response - server is offline
      return { online: false, status: 0 };
    }
  }
};

// Enhanced error handling with more informative messages
const handleApiError = (error) => {
  if (error.response) {
    // Request received a response with an error status code (4xx/5xx)
    const { data, status } = error.response;
    return {
      message: data.detail || `Server error: ${status}. Please try again.`,
      status,
      data,
      isServerError: status >= 500,
      isClientError: status >= 400 && status < 500,
    };
  } else if (error.request) {
    // Request made but no response received (network error)
    const isTimeout = error.code === 'ECONNABORTED';
    return {
      message: isTimeout 
        ? 'Request timed out. The server may be under high load.' 
        : 'No response received from the server. Please check if the backend server is running.',
      status: 0,
      isNetworkError: true,
      isTimeout,
    };
  } else {
    // Error in setting up the request
    return {
      message: error.message || 'An unexpected error occurred',
      status: 0,
      isConfigError: true,
    };
  }
};

// Return all API functions
const newsApi = {
  analyzeText,
  getHistory,
  getHistoryItem,
  getReports,
  getReport,
  getExplanationMethods,
  explainText,
  checkServerStatus
};

export default newsApi; 