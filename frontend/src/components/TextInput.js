import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:8000';

const TextInput = () => {
  const [inputText, setInputText] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [apiStatus, setApiStatus] = useState('unknown');

  // Check API health on component mount
  useEffect(() => {
    checkApiHealth();
  }, []);

  const checkApiHealth = async () => {
    try {
      const response = await axios.get(`${API_URL}/health`);
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

  const handleInputChange = (e) => {
    setInputText(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!inputText.trim()) {
      setError('Please enter some text to analyze');
      return;
    }
    
    setLoading(true);
    setError(null);
    
    try {
      const response = await axios.post(`${API_URL}/analyze`, {
        text: inputText,
        explain: true
      });
      
      setResult(response.data);
      setLoading(false);
    } catch (err) {
      console.error('Error analyzing text:', err);
      setError('Failed to analyze text. Please check the API connection.');
      setLoading(false);
      
      // Recheck API health
      checkApiHealth();
    }
  };

  const handleEnhancedAnalysis = async () => {
    if (!inputText.trim()) {
      setError('Please enter some text to analyze');
      return;
    }
    
    setLoading(true);
    setError(null);
    
    try {
      const response = await axios.post(`${API_URL}/analyze/enhanced`, {
        text: inputText
      });
      
      setResult(response.data);
      setLoading(false);
    } catch (err) {
      console.error('Error performing enhanced analysis:', err);
      setError('Failed to perform enhanced analysis. Please check the API connection.');
      setLoading(false);
      
      // Recheck API health
      checkApiHealth();
    }
  };

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
      
      {result && (
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
                    {Object.entries(result.entities.entities).map(([type, count]) => (
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
                  <p>Grade Level: {result.readability.average_grade_level.toFixed(1)}</p>
                </div>
              )}
              
              {result.propaganda && (
                <div className="result-section">
                  <h5>Propaganda Score:</h5>
                  <p>{result.propaganda.propaganda_score.toFixed(2)}%</p>
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
      )}
      
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
          cursor: pointer;
          transition: background-color 0.3s;
        }
        
        .analyze-btn {
          background-color: #4a6fa5;
          color: white;
        }
        
        .enhanced-btn {
          background-color: #5d8aa8;
          color: white;
        }
        
        button:hover {
          opacity: 0.9;
        }
        
        button:disabled {
          background-color: #cccccc;
          cursor: not-allowed;
        }
        
        .error-message {
          color: #d9534f;
          margin-bottom: 20px;
          padding: 10px;
          background-color: #f8d7da;
          border-radius: 4px;
        }
        
        .result-container {
          background: white;
          padding: 20px;
          border-radius: 8px;
          box-shadow: 0 1px 5px rgba(0, 0, 0, 0.1);
        }
        
        .prediction-badge {
          display: inline-block;
          padding: 8px 16px;
          border-radius: 4px;
          font-weight: bold;
          margin-bottom: 10px;
        }
        
        .fake {
          background-color: #f8d7da;
          color: #721c24;
        }
        
        .real {
          background-color: #d4edda;
          color: #155724;
        }
        
        .confidence {
          margin-bottom: 15px;
          font-size: 14px;
        }
        
        .processed-text {
          margin-top: 20px;
          padding: 15px;
          background: #f5f5f5;
          border-radius: 4px;
        }
        
        .enhanced-results {
          margin-top: 30px;
          border-top: 1px solid #eee;
          padding-top: 20px;
        }
        
        .result-section {
          margin-bottom: 20px;
        }
        
        h3 {
          margin-top: 0;
        }
        
        h4 {
          margin-bottom: 10px;
        }
        
        h5 {
          margin: 10px 0 5px;
        }
        
        ul {
          margin: 5px 0;
          padding-left: 20px;
        }
      `}</style>
    </div>
  );
};

export default TextInput; 