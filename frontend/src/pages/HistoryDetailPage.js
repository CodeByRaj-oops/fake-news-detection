import React, { useEffect, useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { useAnalysis } from '../contexts/AnalysisContext';
import AnalysisResult from '../components/AnalysisResult';
import { ArrowLeftIcon } from '@heroicons/react/24/solid';

function HistoryDetailPage() {
  const { historyId } = useParams();
  const { getHistoryItem, loading, error, setAnalysisResult, setAnalysisText } = useAnalysis();
  const [notFound, setNotFound] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchHistoryItem = async () => {
      try {
        const result = await getHistoryItem(historyId);
        if (!result) {
          setNotFound(true);
        } else {
          // Set the analysis result and text in the context so AnalysisResult can display it
          setAnalysisResult(result);
          setAnalysisText(result.text);
        }
      } catch (err) {
        setNotFound(true);
      }
    };

    fetchHistoryItem();
  }, [historyId, getHistoryItem, setAnalysisResult, setAnalysisText]);

  // If the item wasn't found
  if (notFound) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="text-center py-12">
          <h1 className="text-2xl font-semibold text-gray-900 mb-4">Analysis Not Found</h1>
          <p className="text-gray-600 mb-8">
            The analysis item you're looking for doesn't exist or has been removed.
          </p>
          <Link 
            to="/history"
            className="btn-primary"
          >
            Return to History
          </Link>
        </div>
      </div>
    );
  }

  // While loading
  if (loading) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="animate-pulse space-y-4">
          <div className="h-10 bg-gray-200 rounded w-1/4"></div>
          <div className="h-6 bg-gray-200 rounded w-3/4"></div>
          <div className="h-64 bg-gray-200 rounded"></div>
        </div>
      </div>
    );
  }

  // If there's an error
  if (error) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="bg-red-50 border-l-4 border-red-400 p-4 mb-6">
          <div className="flex">
            <div>
              <p className="text-red-700">
                Error loading analysis: {error}
              </p>
            </div>
          </div>
        </div>
        <div className="flex justify-center">
          <Link 
            to="/history"
            className="btn-primary"
          >
            Return to History
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      {/* Back button */}
      <div className="mb-6">
        <button 
          onClick={() => navigate(-1)} 
          className="flex items-center text-indigo-600 hover:text-indigo-800"
        >
          <ArrowLeftIcon className="h-4 w-4 mr-1" />
          Back to History
        </button>
      </div>
      
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Analysis Details</h1>
      
      {/* Analysis Result component will use the context data we set in useEffect */}
      <AnalysisResult />
      
      <div className="mt-8 flex justify-center space-x-4">
        <Link 
          to="/analyzer" 
          className="btn-primary"
        >
          New Analysis
        </Link>
        <Link 
          to="/history" 
          className="btn-secondary"
        >
          View All History
        </Link>
      </div>
    </div>
  );
}

export default HistoryDetailPage; 