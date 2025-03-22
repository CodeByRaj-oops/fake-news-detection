import React, { useState } from 'react';
import { useAnalysis } from '../contexts/AnalysisContext';
import { InformationCircleIcon } from '@heroicons/react/24/outline';

function TextAnalysisForm() {
  const { analyzeText, isAnalyzing, explanationMethods } = useAnalysis();
  const [text, setText] = useState('');
  const [detailed, setDetailed] = useState(true);
  const [saveReport, setSaveReport] = useState(false);
  const [explain, setExplain] = useState(false);
  const [explanationMethod, setExplanationMethod] = useState('lime');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validate text input
    if (!text.trim()) {
      setError('Please enter text to analyze');
      return;
    }
    
    if (text.trim().length < 50) {
      setError('Text is too short. Please enter at least 50 characters for meaningful analysis.');
      return;
    }
    
    setError('');
    
    // Submit analysis request
    try {
      await analyzeText(text, detailed, saveReport, explain, explanationMethod, 10);
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
          For best results, enter complete paragraphs or full articles (minimum 50 characters).
        </p>
      </div>

      {/* Analysis options */}
      <div className="bg-gray-50 p-4 rounded-md border">
        <h3 className="text-md font-medium mb-3">Analysis Options</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-3">
            <div className="flex items-center">
              <input
                id="detailed-analysis"
                name="detailed-analysis"
                type="checkbox"
                className="h-4 w-4 rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                checked={detailed}
                onChange={(e) => {
                  setDetailed(e.target.checked);
                  // If detailed is turned off, disable save report
                  if (!e.target.checked) {
                    setSaveReport(false);
                  }
                }}
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
          
          <div className="space-y-3">
            <div className="flex items-center">
              <input
                id="model-explanations"
                name="model-explanations"
                type="checkbox"
                className="h-4 w-4 rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                checked={explain}
                onChange={(e) => setExplain(e.target.checked)}
                disabled={isAnalyzing}
              />
              <label htmlFor="model-explanations" className="ml-2 text-sm text-gray-700">
                Include model explanations
              </label>
              <div className="ml-1 group relative">
                <InformationCircleIcon className="h-4 w-4 text-gray-400" />
                <div className="hidden group-hover:block absolute z-10 w-64 p-2 bg-white shadow-lg rounded text-xs text-gray-600 -left-8 -top-24">
                  Model explanations show which words and phrases most influenced the prediction, using techniques like LIME and SHAP.
                </div>
              </div>
            </div>
            
            {explain && (
              <div>
                <label htmlFor="explanation-method" className="block text-sm text-gray-700 mb-1">
                  Explanation method
                </label>
                <select
                  id="explanation-method"
                  className="form-select text-sm"
                  value={explanationMethod}
                  onChange={(e) => setExplanationMethod(e.target.value)}
                  disabled={isAnalyzing || !explain}
                >
                  {explanationMethods.map(method => (
                    <option key={method.id} value={method.id}>
                      {method.name} - {method.description}
                    </option>
                  ))}
                  {explanationMethods.length === 0 && (
                    <option value="lime">LIME - Local explanations</option>
                  )}
                </select>
              </div>
            )}
          </div>
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