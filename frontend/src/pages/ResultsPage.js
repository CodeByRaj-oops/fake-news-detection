import React from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { ArrowLeftIcon, DocumentTextIcon, StarIcon } from '@heroicons/react/24/outline';
import AnalysisResult from '../components/AnalysisResult';
import { useAnalysis } from '../contexts/AnalysisContext';

const ResultsPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { analysisResult, analyzeText, clearAnalysis } = useAnalysis();
  
  // If no result and no state, redirect to analyzer
  React.useEffect(() => {
    if (!analysisResult && !location.state?.result) {
      navigate('/analyzer');
    }
  }, [analysisResult, location.state, navigate]);

  // Use result from state if passed, otherwise use context
  const result = location.state?.result || analysisResult;
  
  // Handle saving report
  const handleSaveReport = () => {
    if (result) {
      // You would implement the save functionality here
      alert('Report saved successfully!');
    }
  };

  if (!result) {
    return <div className="p-8 text-center">Loading...</div>;
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-6 flex items-center justify-between">
        <Link
          to="/analyzer"
          className="flex items-center text-blue-600 hover:text-blue-800"
        >
          <ArrowLeftIcon className="mr-2 h-4 w-4" />
          Back to Analyzer
        </Link>
        
        <div className="flex space-x-4">
          <button
            onClick={handleSaveReport}
            className="flex items-center rounded-md bg-blue-50 px-4 py-2 text-sm font-medium text-blue-700 hover:bg-blue-100"
          >
            <DocumentTextIcon className="mr-2 h-5 w-5" />
            Save as Report
          </button>
        </div>
      </div>

      {/* Analysis Results */}
      <div className="rounded-lg bg-white p-6 shadow-md">
        <h1 className="mb-6 text-2xl font-bold">Analysis Results</h1>
        
        <AnalysisResult result={result} showDetailedView={true} />
        
        <div className="mt-8 flex flex-col space-y-4 sm:flex-row sm:space-x-4 sm:space-y-0">
          <Link 
            to="/analyzer" 
            className="flex-1 rounded-md border border-gray-300 bg-white px-4 py-2 text-center text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50"
          >
            Analyze Another Text
          </Link>
          <Link 
            to="/history" 
            className="flex-1 rounded-md border border-blue-600 bg-blue-600 px-4 py-2 text-center text-sm font-medium text-white shadow-sm hover:bg-blue-700"
          >
            View Analysis History
          </Link>
        </div>
      </div>
    </div>
  );
};

export default ResultsPage; 