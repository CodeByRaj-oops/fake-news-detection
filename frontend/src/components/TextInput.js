import React, { useState, useEffect } from 'react';
import axios from 'axios';
import config from '../config.js';

/**
 * TextInput Component
 * Handles text submission and displaying analysis results
 */
const TextInput = () => {
  const [inputText, setInputText] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [apiStatus, setApiStatus] = useState('unknown');

  // Check API health on component mount
  useEffect(() => {
    checkApiHealth();
    // Set up periodic health checks
    const interval = setInterval(checkApiHealth, 30000); // Check every 30 seconds
    return () => clearInterval(interval); // Cleanup on unmount
  }, []);

  /**
   * Check backend API health status
   */
  const checkApiHealth = async () => {
    try {
      const response = await axios.get(`${config.apiUrl}${config.endpoints.health}`, { timeout: config.timeout });
      if (response.data && response.data.status === 'ok') {
        setApiStatus('connected');
      } else {
        setApiStatus('error');
      }
    } catch (err) {
      console.error('API Health check failed:', err);
      setApiStatus('disconnected');
    }
  };

  /**
   * Handle text input changes
   */
  const handleInputChange = (e) => {
    setInputText(e.target.value);
  };

  /**
   * Handle form submission for basic analysis
   */
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!inputText.trim()) {
      setError('Please enter some text to analyze');
      return;
    }
    
    setLoading(true);
    setError(null);
    
    try {
      const response = await axios.post(`${config.apiUrl}${config.endpoints.analyze}`, {
        text: inputText,
        explain: true
      }, { timeout: config.timeout });
      
      setResult(response.data);
      setLoading(false);
    } catch (err) {
      console.error('Error analyzing text:', err);
      setError(`Failed to analyze text: ${err.message || 'Unknown error'}. Please check the API connection.`);
      setLoading(false);
      
      // Recheck API health
      checkApiHealth();
    }
  };

  /**
   * Handle enhanced analysis request
   */
  const handleEnhancedAnalysis = async () => {
    if (!inputText.trim()) {
      setError('Please enter some text to analyze');
      return;
    }
    
    setLoading(true);
    setError(null);
    
    try {
      const response = await axios.post(`${config.apiUrl}${config.endpoints.enhancedAnalyze}`, {
        text: inputText
      }, { timeout: config.timeout });
      
      setResult(response.data);
      setLoading(false);
    } catch (err) {
      console.error('Error performing enhanced analysis:', err);
      setError(`Failed to perform enhanced analysis: ${err.message || 'Unknown error'}. Please check the API connection.`);
      setLoading(false);
      
      // Recheck API health
      checkApiHealth();
    }
  };

  /**
   * Get color based on API status
   */
  const getStatusColor = () => {
    switch (apiStatus) {
      case 'connected':
        return 'green';
      case 'disconnected':
        return 'red';
      case 'error':
        return 'orange';
      default:
        return 'gray';
    }
  };

  /**
   * Render appropriate result content based on what data is available
   */
  const renderResultContent = () => {
    if (!result) return null;

    return (
      <div className="result-container">
        <h3>Analysis Result:</h3>
        <div className={`prediction-badge ${result.label === 'FAKE' ? 'fake' : 'real'}`}>
          {result.label}
        </div>
        <div className="confidence">
          Confidence: {(result.confidence * 100).toFixed(2)}%
        </div>
        
        {result.processed_text && (
          <div className="processed-text">
            <h4>Processed Text:</h4>
            <p>{result.processed_text}</p>
          </div>
        )}
        
        {/* Display enhanced analysis results if available */}
        {result.language && (
          <div className="enhanced-results">
            <h4>Enhanced Analysis:</h4>
            
            <div className="result-section">
              <h5>Language:</h5>
              <p>Detected: {result.language.language_name} ({result.language.language_code})</p>
              <p>Confidence: {(result.language.confidence * 100).toFixed(2)}%</p>
            </div>
            
            {result.entities && (
              <div className="result-section">
                <h5>Entities:</h5>
                <ul>
                  {result.entities.entities && Object.entries(result.entities.entities).map(([type, count]) => (
                    <li key={type}>
                      {type}: {count}
                    </li>
                  ))}
                </ul>
              </div>
            )}
            
            {result.readability && (
              <div className="result-section">
                <h5>Readability:</h5>
                <p>Flesch Reading Ease: {result.readability.flesch_reading_ease.toFixed(2)}</p>
                <p>Grade Level: {result.readability.average_grade_level ? result.readability.average_grade_level.toFixed(1) : 'N/A'}</p>
              </div>
            )}
            
            {result.propaganda && (
              <div className="result-section">
                <h5>Propaganda Techniques:</h5>
                <p>Score: {result.propaganda.propaganda_score ? (result.propaganda.propaganda_score).toFixed(2) : 'N/A'}%</p>
                {result.propaganda.techniques && Object.entries(result.propaganda.techniques).length > 0 && (
                  <ul>
                    {Object.entries(result.propaganda.techniques).map(([technique, count]) => (
                      count > 0 && (
                        <li key={technique}>
                          {technique.replace('_', ' ')}: {count}
                        </li>
                      )
                    ))}
                  </ul>
                )}
              </div>
            )}
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="text-input-container">
      <div className="api-status" style={{ color: getStatusColor() }}>
        API Status: {apiStatus === 'connected' ? 'Connected' : apiStatus === 'disconnected' ? 'Disconnected' : 'Error'}
      </div>
      
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="textInput">Enter text to analyze:</label>
          <textarea
            id="textInput"
            value={inputText}
            onChange={handleInputChange}
            rows={6}
            placeholder="Enter news article or text to analyze for fakeness..."
            className="text-area"
          />
        </div>
        
        <div className="button-group">
          <button type="submit" className="analyze-btn" disabled={loading}>
            {loading ? 'Analyzing...' : 'Analyze Text'}
          </button>
          <button 
            type="button" 
            className="enhanced-btn"
            onClick={handleEnhancedAnalysis} 
            disabled={loading}
          >
            Enhanced Analysis
          </button>
        </div>
      </form>
      
      {error && (
        <div className="error-message">
          {error}
        </div>
      )}
      
      {result && renderResultContent()}
      
      <style jsx>{`
        .text-input-container {
          max-width: 800px;
          margin: 0 auto;
          padding: 20px;
          background: #f9f9f9;
          border-radius: 8px;
          box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
        
        .api-status {
          margin-bottom: 15px;
          font-weight: bold;
        }
        
        .form-group {
          margin-bottom: 20px;
        }
        
        label {
          display: block;
          margin-bottom: 8px;
          font-weight: bold;
        }
        
        .text-area {
          width: 100%;
          padding: 12px;
          border: 1px solid #ddd;
          border-radius: 4px;
          font-family: inherit;
          font-size: 16px;
        }
        
        .button-group {
          display: flex;
          gap: 15px;
          margin-bottom: 20px;
        }
        
        button {
          padding: 10px 20px;
          border: none;
          border-radius: 4px;
          font-size: 16px;
          font-weight: bold;
          cursor: pointer;
          transition: background-color 0.3s;
        }
        
        .analyze-btn {
          background-color: #4a90e2;
          color: white;
        }
        
        .analyze-btn:hover {
          background-color: #3a80d2;
        }
        
        .enhanced-btn {
          background-color: #6c5ce7;
          color: white;
        }
        
        .enhanced-btn:hover {
          background-color: #5c4cd7;
        }
        
        button:disabled {
          background-color: #cccccc;
          cursor: not-allowed;
        }
        
        .error-message {
          padding: 10px;
          margin-bottom: 20px;
          background-color: #ffebee;
          color: #d32f2f;
          border-radius: 4px;
        }
        
        .result-container {
          padding: 15px;
          background-color: #e3f2fd;
          border-radius: 4px;
        }
        
        .prediction-badge {
          display: inline-block;
          padding: 5px 15px;
          border-radius: 20px;
          font-weight: bold;
          margin: 10px 0;
        }
        
        .fake {
          background-color: #ff6b6b;
          color: white;
        }
        
        .real {
          background-color: #51cf66;
          color: white;
        }
        
        .confidence {
          margin-bottom: 15px;
          font-weight: bold;
        }
        
        .processed-text {
          margin-top: 15px;
          padding: 10px;
          background-color: #f8f9fa;
          border-radius: 4px;
        }
        
        .enhanced-results {
          margin-top: 20px;
          border-top: 1px solid #ddd;
          padding-top: 15px;
        }
        
        .result-section {
          margin-bottom: 15px;
          padding: 10px;
          background-color: #f8f9fa;
          border-radius: 4px;
        }
        
        .result-section h5 {
          margin-top: 0;
          color: #333;
        }
      `}</style>
    </div>
  );
};

export default TextInput; 