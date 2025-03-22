import React, { createContext, useContext, useState, useCallback, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import * as newsApi from '../api/newsApi';

// Create the context
const AnalysisContext = createContext();

// Analysis provider component
export function AnalysisProvider({ children }) {
  const navigate = useNavigate();
  
  // State for analysis
  const [analysisText, setAnalysisText] = useState('');
  const [analysisResult, setAnalysisResult] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [error, setError] = useState(null);
  
  // State for history
  const [historyItems, setHistoryItems] = useState([]);
  const [isLoadingHistory, setIsLoadingHistory] = useState(false);
  
  // State for reports
  const [reports, setReports] = useState([]);
  const [isLoadingReports, setIsLoadingReports] = useState(false);
  
  // State for model explanations
  const [explanationMethods, setExplanationMethods] = useState([]);
  const [isLoadingExplanationMethods, setIsLoadingExplanationMethods] = useState(false);

  // Load explanation methods on mount
  useEffect(() => {
    const loadExplanationMethods = async () => {
      setIsLoadingExplanationMethods(true);
      try {
        const methods = await newsApi.getExplanationMethods();
        setExplanationMethods(methods);
      } catch (err) {
        console.error('Failed to load explanation methods:', err);
      } finally {
        setIsLoadingExplanationMethods(false);
      }
    };

    loadExplanationMethods();
  }, []);
  
  // Analyze text function
  const analyzeText = useCallback(async (text, detailed = true, saveReport = false, 
                                       explain = false, explanationMethod = 'lime', numFeatures = 10) => {
    setIsAnalyzing(true);
    setError(null);
    setAnalysisText(text);
    
    try {
      const result = await newsApi.analyzeText(
        text, detailed, saveReport, explain, explanationMethod, numFeatures
      );
      setAnalysisResult(result);
      
      // Navigate to results page
      navigate('/results');
      return result;
    } catch (err) {
      setError(err.message || 'An error occurred during analysis');
      toast.error(err.message || 'Failed to analyze text');
      return null;
    } finally {
      setIsAnalyzing(false);
    }
  }, [navigate]);

  // Generate explanations for text
  const explainText = useCallback(async (text, method = 'lime', numFeatures = 10) => {
    setError(null);
    
    try {
      const result = await newsApi.explainText(text, method, numFeatures);
      return result;
    } catch (err) {
      setError(err.message || 'An error occurred generating explanations');
      toast.error(err.message || 'Failed to generate explanations');
      return null;
    }
  }, []);
  
  // Load history
  const loadHistory = useCallback(async (limit = 10, offset = 0) => {
    setIsLoadingHistory(true);
    setError(null);
    
    try {
      const history = await newsApi.getHistory(limit, offset);
      setHistoryItems(history);
      return history;
    } catch (err) {
      setError(err.message || 'An error occurred loading history');
      toast.error(err.message || 'Failed to load history');
      return [];
    } finally {
      setIsLoadingHistory(false);
    }
  }, []);
  
  // Get history item
  const getHistoryItem = useCallback(async (historyId) => {
    setIsLoadingHistory(true);
    setError(null);
    
    try {
      const historyItem = await newsApi.getHistoryItem(historyId);
      return historyItem;
    } catch (err) {
      setError(err.message || 'An error occurred loading history item');
      toast.error(err.message || 'Failed to load history item');
      return null;
    } finally {
      setIsLoadingHistory(false);
    }
  }, []);
  
  // Load reports
  const loadReports = useCallback(async (limit = 10, offset = 0) => {
    setIsLoadingReports(true);
    setError(null);
    
    try {
      const reportsList = await newsApi.getReports(limit, offset);
      setReports(reportsList);
      return reportsList;
    } catch (err) {
      setError(err.message || 'An error occurred loading reports');
      toast.error(err.message || 'Failed to load reports');
      return [];
    } finally {
      setIsLoadingReports(false);
    }
  }, []);
  
  // Get report
  const getReport = useCallback(async (reportId) => {
    setIsLoadingReports(true);
    setError(null);
    
    try {
      const report = await newsApi.getReport(reportId);
      return report;
    } catch (err) {
      setError(err.message || 'An error occurred loading report');
      toast.error(err.message || 'Failed to load report');
      return null;
    } finally {
      setIsLoadingReports(false);
    }
  }, []);
  
  // Clear current analysis
  const clearAnalysis = useCallback(() => {
    setAnalysisText('');
    setAnalysisResult(null);
    setError(null);
  }, []);
  
  // Create the context value object
  const contextValue = {
    // Analysis
    analysisText,
    setAnalysisText,
    analysisResult,
    isAnalyzing,
    analyzeText,
    clearAnalysis,
    
    // History
    historyItems,
    isLoadingHistory,
    loadHistory,
    getHistoryItem,
    
    // Reports
    reports,
    isLoadingReports,
    loadReports,
    getReport,
    
    // Model Explanations
    explanationMethods,
    isLoadingExplanationMethods,
    explainText,
    
    // Error
    error,
    setError,
  };
  
  return (
    <AnalysisContext.Provider value={contextValue}>
      {children}
    </AnalysisContext.Provider>
  );
}

// Custom hook for using the analysis context
export function useAnalysis() {
  const context = useContext(AnalysisContext);
  
  if (!context) {
    throw new Error('useAnalysis must be used within an AnalysisProvider');
  }
  
  return context;
}

export default AnalysisContext; 