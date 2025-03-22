import React, { useEffect, useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { useAnalysis } from '../contexts/AnalysisContext';
import AnalysisResult from '../components/AnalysisResult';
import { 
  ArrowLeftIcon, 
  ArrowDownTrayIcon, 
  ShareIcon 
} from '@heroicons/react/24/solid';

function ReportDetailPage() {
  const { reportId } = useParams();
  const { getReport, loading, error, setAnalysisResult, setAnalysisText } = useAnalysis();
  const [notFound, setNotFound] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchReport = async () => {
      try {
        const result = await getReport(reportId);
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

    fetchReport();
  }, [reportId, getReport, setAnalysisResult, setAnalysisText]);

  // Handle share button click
  const handleShare = () => {
    // In a real app, generate a shareable link
    alert('Sharing functionality would be implemented here.');
  };

  // Handle download button click
  const handleDownload = () => {
    // In a real app, generate a PDF report
    alert('PDF download functionality would be implemented here.');
  };

  // If the report wasn't found
  if (notFound) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="text-center py-12">
          <h1 className="text-2xl font-semibold text-gray-900 mb-4">Report Not Found</h1>
          <p className="text-gray-600 mb-8">
            The report you're looking for doesn't exist or has been removed.
          </p>
          <Link 
            to="/reports"
            className="btn-primary"
          >
            Return to Reports
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
                Error loading report: {error}
              </p>
            </div>
          </div>
        </div>
        <div className="flex justify-center">
          <Link 
            to="/reports"
            className="btn-primary"
          >
            Return to Reports
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      {/* Navigation and actions */}
      <div className="flex justify-between items-center mb-6">
        <button 
          onClick={() => navigate(-1)} 
          className="flex items-center text-indigo-600 hover:text-indigo-800"
        >
          <ArrowLeftIcon className="h-4 w-4 mr-1" />
          Back to Reports
        </button>
        
        <div className="flex space-x-2">
          <button 
            onClick={handleShare} 
            className="flex items-center text-gray-600 hover:text-indigo-600 bg-white border border-gray-300 rounded-md px-3 py-1.5 text-sm"
          >
            <ShareIcon className="h-4 w-4 mr-1" />
            Share
          </button>
          <button 
            onClick={handleDownload} 
            className="flex items-center text-white bg-indigo-600 hover:bg-indigo-700 rounded-md px-3 py-1.5 text-sm"
          >
            <ArrowDownTrayIcon className="h-4 w-4 mr-1" />
            Download PDF
          </button>
        </div>
      </div>
      
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Detailed Analysis Report</h1>
      
      {/* Analysis Result component will use the context data we set in useEffect */}
      <AnalysisResult />
      
      {/* Additional report information */}
      <div className="mt-10 card bg-gray-50">
        <h2 className="text-xl font-semibold mb-4">Report Information</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 className="text-sm font-medium text-gray-500">REPORT METHODOLOGY</h3>
            <p className="mt-1 text-sm text-gray-900">
              This report was generated using our advanced AI model trained on verified news sources 
              and known misinformation patterns. The analysis examines multiple factors including 
              writing style, factual consistency, emotional manipulation, and source credibility.
            </p>
          </div>
          <div>
            <h3 className="text-sm font-medium text-gray-500">DISCLAIMER</h3>
            <p className="mt-1 text-sm text-gray-900">
              While our system provides a high degree of accuracy, it should be used as a tool to 
              assist critical thinking, not replace it. Always verify important information with 
              trusted sources before making decisions based on this analysis.
            </p>
          </div>
        </div>
      </div>
      
      <div className="mt-8 flex justify-center space-x-4">
        <Link 
          to="/analyzer" 
          className="btn-primary"
        >
          New Analysis
        </Link>
        <Link 
          to="/reports" 
          className="btn-secondary"
        >
          View All Reports
        </Link>
      </div>
    </div>
  );
}

export default ReportDetailPage; 