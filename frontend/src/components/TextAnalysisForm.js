import React, { useState } from 'react';
import { useAnalysis } from '../contexts/AnalysisContext';

function TextAnalysisForm() {
  const { analyzeText, isAnalyzing } = useAnalysis();
  const [text, setText] = useState('');
  const [detailed, setDetailed] = useState(true);
  const [saveReport, setSaveReport] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validate text input
    if (!text.trim()) {
      setError('Please enter text to analyze');
      return;
    }
    
    if (text.trim().length < 10) {
      setError('Text is too short. Please enter at least 10 characters.');
      return;
    }
    
    setError('');
    
    // Submit analysis request
    try {
      await analyzeText(text, detailed, saveReport);
    } catch (err) {
      setError(err.message || 'An error occurred during analysis');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Text entry */}
      <div>
        <label htmlFor="analysis-text" className="form-label">
          Enter text to analyze
        </label>
        <textarea
          id="analysis-text"
          rows={8}
          className="form-input mt-1"
          placeholder="Paste or type the news article or text you want to analyze..."
          value={text}
          onChange={(e) => setText(e.target.value)}
          disabled={isAnalyzing}
          required
        />
        
        {error && (
          <p className="mt-2 text-red-600 text-sm">{error}</p>
        )}
        
        <p className="mt-2 text-sm text-gray-500">
          For best results, enter complete paragraphs or full articles.
        </p>
      </div>

      {/* Analysis options */}
      <div className="flex flex-col sm:flex-row gap-4">
        <div className="flex items-center">
          <input
            id="detailed-analysis"
            name="detailed-analysis"
            type="checkbox"
            className="h-4 w-4 rounded border-gray-300 text-primary-600 focus:ring-primary-500"
            checked={detailed}
            onChange={(e) => setDetailed(e.target.checked)}
            disabled={isAnalyzing}
          />
          <label htmlFor="detailed-analysis" className="ml-2 text-sm text-gray-700">
            Detailed analysis
          </label>
        </div>
        
        <div className="flex items-center">
          <input
            id="save-report"
            name="save-report"
            type="checkbox"
            className="h-4 w-4 rounded border-gray-300 text-primary-600 focus:ring-primary-500"
            checked={saveReport}
            onChange={(e) => setSaveReport(e.target.checked)}
            disabled={isAnalyzing || !detailed}
          />
          <label 
            htmlFor="save-report" 
            className={`ml-2 text-sm ${detailed ? 'text-gray-700' : 'text-gray-400'}`}
          >
            Save report
          </label>
        </div>
      </div>

      {/* Submit button */}
      <div>
        <button
          type="submit"
          className="btn btn-primary w-full sm:w-auto"
          disabled={isAnalyzing}
        >
          {isAnalyzing ? (
            <>
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Analyzing...
            </>
          ) : (
            'Analyze Text'
          )}
        </button>
      </div>
    </form>
  );
}

export default TextAnalysisForm; 