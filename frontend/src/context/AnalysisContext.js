import React, { createContext, useState, useContext } from 'react';

// Create context
const AnalysisContext = createContext();

// Analysis provider component
export const AnalysisProvider = ({ children }) => {
  const [analysisResult, setAnalysisResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [history, setHistory] = useState([]);

  // Set analysis result
  const setAnalysis = (result) => {
    setAnalysisResult(result);
  };

  // Clear analysis result
  const clearAnalysis = () => {
    setAnalysisResult(null);
    setError(null);
  };

  // Add to history
  const addToHistory = (item) => {
    setHistory((prevHistory) => [item, ...prevHistory]);
  };

  // Return provider
  return (
    <AnalysisContext.Provider
      value={{
        analysisResult,
        setAnalysis,
        clearAnalysis,
        loading,
        setLoading,
        error,
        setError,
        history,
        setHistory,
        addToHistory
      }}
    >
      {children}
    </AnalysisContext.Provider>
  );
};

// Custom hook to use the analysis context
export const useAnalysis = () => {
  const context = useContext(AnalysisContext);
  if (!context) {
    throw new Error('useAnalysis must be used within an AnalysisProvider');
  }
  return context;
};

export default AnalysisContext; 