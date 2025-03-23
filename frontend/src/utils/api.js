/**
 * API Client for Fake News Detection System
 * 
 * This module provides a robust API client that handles:
 * - Properly formatted requests to the backend
 * - Error handling with meaningful messages
 * - Request timeouts
 * - Automatic retries for failed requests
 * - Consistent error format
 */

// Use API_URL from config if it exists, otherwise default to localhost:8000
let API_URL = 'http://localhost:8000';
try {
  const config = require('../config');
  API_URL = config.API_URL || API_URL;
} catch (error) {
  console.warn('Config file not found, using default API URL:', API_URL);
}

// Default timeout in milliseconds
const DEFAULT_TIMEOUT = 30000; // 30 seconds

// Maximum number of retries for failed requests
const MAX_RETRIES = 2;

/**
 * Creates a promise that rejects after a specified timeout
 * @param {number} ms - Timeout in milliseconds
 * @returns {Promise<never>} A promise that rejects after the timeout
 */
const timeoutPromise = (ms) => {
  return new Promise((_, reject) => {
    setTimeout(() => {
      reject(new Error(`Request timed out after ${ms}ms`));
    }, ms);
  });
};

/**
 * Makes an API request with timeout, error handling, and retries
 * @param {string} endpoint - API endpoint (without base URL)
 * @param {Object} options - Fetch options
 * @param {number} timeout - Timeout in milliseconds
 * @param {number} retries - Number of retries left
 * @returns {Promise<any>} - Response data
 */
const makeRequest = async (endpoint, options = {}, timeout = DEFAULT_TIMEOUT, retries = MAX_RETRIES) => {
  const url = `${API_URL}/${endpoint.startsWith('/') ? endpoint.slice(1) : endpoint}`;
  
  try {
    // Race between fetch and timeout
    const response = await Promise.race([
      fetch(url, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...(options.headers || {})
        }
      }),
      timeoutPromise(timeout)
    ]);

    // Handle HTTP errors
    if (!response.ok) {
      let errorData = { message: `Server returned ${response.status} ${response.statusText}` };
      
      try {
        // Try to parse error response as JSON
        errorData = await response.json();
      } catch (e) {
        // If parsing fails, use text response
        try {
          const textResponse = await response.text();
          if (textResponse) {
            errorData.message = textResponse;
          }
        } catch (textError) {
          // Ignore text parsing errors
        }
      }
      
      throw new Error(errorData.message || errorData.detail || 'Unknown server error');
    }

    // Parse successful response
    return await response.json();
  } catch (error) {
    // Handle connection errors and timeouts
    if (error.message === 'Failed to fetch' || error.message.includes('timed out')) {
      console.error(`Connection error: ${error.message}`);
      
      // Check if we should retry
      if (retries > 0) {
        console.log(`Retrying request to ${endpoint}... (${retries} retries left)`);
        // Exponential backoff for retries
        await new Promise(resolve => setTimeout(resolve, (MAX_RETRIES - retries + 1) * 1000));
        return makeRequest(endpoint, options, timeout, retries - 1);
      }
      
      if (error.message === 'Failed to fetch') {
        throw new Error('No response received from the server. Please check if the backend server is running.');
      }
    }
    
    throw error;
  }
};

/**
 * API client for making requests to the backend
 */
const apiClient = {
  /**
   * Make a GET request
   * @param {string} endpoint - API endpoint
   * @param {Object} options - Additional fetch options
   * @returns {Promise<any>} Response data
   */
  get: (endpoint, options = {}) => {
    return makeRequest(endpoint, { method: 'GET', ...options });
  },
  
  /**
   * Make a POST request
   * @param {string} endpoint - API endpoint
   * @param {Object} data - Request payload
   * @param {Object} options - Additional fetch options
   * @returns {Promise<any>} Response data
   */
  post: (endpoint, data, options = {}) => {
    return makeRequest(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
      ...options
    });
  },
  
  /**
   * Check backend health
   * @returns {Promise<Object>} Health status
   */
  checkHealth: () => {
    return apiClient.get('/health')
      .then(() => ({ status: 'connected' }))
      .catch(error => ({ status: 'disconnected', error: error.message }));
  },
  
  /**
   * Analyze text for fake news
   * @param {string} text - Text to analyze
   * @param {Object} options - Analysis options
   * @returns {Promise<Object>} Analysis results
   */
  analyzeText: (text, options = {}) => {
    const payload = {
      text,
      detailed: options.detailed ?? false,
      save_report: options.saveReport ?? false,
      explain: options.explain ?? false,
      explanation_method: options.explanationMethod ?? 'lime',
      num_features: options.numFeatures ?? 10
    };
    
    return apiClient.post('/analyze', payload);
  }
};

export default apiClient; 