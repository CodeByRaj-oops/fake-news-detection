import axios from 'axios';

// Create axios instance with base URL
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

// API functions for news analysis
export const analyzeText = async (text, detailed = false, saveReport = false) => {
  try {
    const response = await api.post('/analyze', {
      text,
      detailed,
      save_report: saveReport,
    });
    return response.data;
  } catch (error) {
    throw handleApiError(error);
  }
};

// Get analysis history
export const getHistory = async (limit = 10, offset = 0) => {
  try {
    const response = await api.get(`/history?limit=${limit}&offset=${offset}`);
    return response.data;
  } catch (error) {
    throw handleApiError(error);
  }
};

// Get specific history item
export const getHistoryItem = async (historyId) => {
  try {
    const response = await api.get(`/history/${historyId}`);
    return response.data;
  } catch (error) {
    throw handleApiError(error);
  }
};

// Get reports list
export const getReports = async (limit = 10, offset = 0) => {
  try {
    const response = await api.get(`/reports?limit=${limit}&offset=${offset}`);
    return response.data;
  } catch (error) {
    throw handleApiError(error);
  }
};

// Get specific report
export const getReport = async (reportId) => {
  try {
    const response = await api.get(`/reports/${reportId}`);
    return response.data;
  } catch (error) {
    throw handleApiError(error);
  }
};

// Helper function to handle API errors
const handleApiError = (error) => {
  if (error.response) {
    // The request was made and the server responded with a status code
    // that falls out of the range of 2xx
    const { data, status } = error.response;
    return {
      message: data.detail || 'An error occurred with the API',
      status,
      data,
    };
  } else if (error.request) {
    // The request was made but no response was received
    return {
      message: 'No response received from the server. Please check your connection.',
      status: 0,
    };
  } else {
    // Something happened in setting up the request that triggered an Error
    return {
      message: error.message || 'An unexpected error occurred',
      status: 0,
    };
  }
};

export default {
  analyzeText,
  getHistory,
  getHistoryItem,
  getReports,
  getReport,
}; 