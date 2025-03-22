import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAnalysis } from '../contexts/AnalysisContext';
import { 
  CheckCircleIcon, 
  ExclamationCircleIcon,
  InformationCircleIcon,
  ArrowLeftIcon,
  ArrowRightIcon,
  DocumentTextIcon,
  ClockIcon
} from '@heroicons/react/24/solid';

function HistoryList() {
  const { historyItems, loading, loadHistory } = useAnalysis();
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage] = useState(10);

  useEffect(() => {
    loadHistory(itemsPerPage, (currentPage - 1) * itemsPerPage);
  }, [currentPage, itemsPerPage, loadHistory]);

  // Calculate total pages
  const totalPages = Math.ceil((historyItems?.total || 0) / itemsPerPage);

  // Handle page navigation
  const handlePrevPage = () => {
    if (currentPage > 1) {
      setCurrentPage(currentPage - 1);
    }
  };

  const handleNextPage = () => {
    if (currentPage < totalPages) {
      setCurrentPage(currentPage + 1);
    }
  };

  // Format timestamp for display
  const formatDate = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleString();
  };

  // Truncate text to specified length with ellipsis
  const truncateText = (text, maxLength = 100) => {
    if (!text || text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
  };

  // Get appropriate icon based on prediction
  const getPredictionIcon = (prediction) => {
    if (prediction === 'REAL') {
      return <CheckCircleIcon className="h-5 w-5 text-real" />;
    } else if (prediction === 'FAKE') {
      return <ExclamationCircleIcon className="h-5 w-5 text-fake" />;
    } else {
      return <InformationCircleIcon className="h-5 w-5 text-neutral" />;
    }
  };

  // Get appropriate color class based on prediction
  const getPredictionColorClass = (prediction) => {
    if (prediction === 'REAL') return 'text-real';
    if (prediction === 'FAKE') return 'text-fake';
    return 'text-neutral';
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-[200px]">
        <div className="animate-pulse flex space-x-4">
          <div className="w-10 h-10 bg-gray-200 rounded-full"></div>
          <div className="flex-1 space-y-3 py-1">
            <div className="h-4 bg-gray-200 rounded w-3/4"></div>
            <div className="h-4 bg-gray-200 rounded"></div>
            <div className="h-4 bg-gray-200 rounded w-1/2"></div>
          </div>
        </div>
      </div>
    );
  }

  if (!historyItems || historyItems.items?.length === 0) {
    return (
      <div className="text-center py-8">
        <DocumentTextIcon className="h-16 w-16 text-gray-300 mx-auto mb-4" />
        <h3 className="text-xl font-medium text-gray-900">No Analysis History</h3>
        <p className="text-gray-500 mt-2">
          Your past analyses will appear here once you've analyzed some content.
        </p>
        <Link to="/analyzer" className="btn-primary inline-block mt-4">
          Analyze New Content
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* History list */}
      <div className="overflow-hidden bg-white shadow sm:rounded-md">
        <ul className="divide-y divide-gray-200">
          {historyItems.items.map((item) => (
            <li key={item.id}>
              <Link to={`/history/${item.id}`} className="block hover:bg-gray-50">
                <div className="px-4 py-4 sm:px-6">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center">
                      {getPredictionIcon(item.prediction)}
                      <p className={`ml-2 text-sm font-medium ${getPredictionColorClass(item.prediction)}`}>
                        {item.prediction === 'REAL' ? 'Likely Real' : 
                         item.prediction === 'FAKE' ? 'Likely Fake' : 'Uncertain'}
                      </p>
                    </div>
                    <div className="flex items-center text-sm text-gray-500">
                      <ClockIcon className="h-4 w-4 mr-1" />
                      {formatDate(item.timestamp)}
                    </div>
                  </div>
                  <div className="mt-2 sm:flex sm:justify-between">
                    <div className="sm:flex-grow">
                      <p className="text-sm text-gray-900 line-clamp-2">
                        {truncateText(item.text, 150)}
                      </p>
                      {item.confidence && (
                        <p className="mt-1 text-xs text-gray-500">
                          Confidence: <span className="font-medium">{(item.confidence * 100).toFixed(1)}%</span>
                        </p>
                      )}
                    </div>
                  </div>
                </div>
              </Link>
            </li>
          ))}
        </ul>
      </div>
      
      {/* Pagination */}
      {totalPages > 1 && (
        <nav className="flex items-center justify-between px-4 py-3 bg-white border sm:px-6 rounded-md">
          <div className="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
            <div>
              <p className="text-sm text-gray-700">
                Showing <span className="font-medium">{(currentPage - 1) * itemsPerPage + 1}</span> to{' '}
                <span className="font-medium">
                  {Math.min(currentPage * itemsPerPage, historyItems.total)}
                </span>{' '}
                of <span className="font-medium">{historyItems.total}</span> results
              </p>
            </div>
            <div>
              <div className="flex space-x-2">
                <button
                  onClick={handlePrevPage}
                  disabled={currentPage === 1}
                  className={`relative inline-flex items-center px-4 py-2 text-sm font-medium rounded-md
                    ${currentPage === 1
                      ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                      : 'bg-white text-gray-700 hover:bg-gray-50 border'
                    }`}
                >
                  <ArrowLeftIcon className="h-4 w-4 mr-1" />
                  Previous
                </button>
                <button
                  onClick={handleNextPage}
                  disabled={currentPage >= totalPages}
                  className={`relative inline-flex items-center px-4 py-2 text-sm font-medium rounded-md
                    ${currentPage >= totalPages
                      ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                      : 'bg-white text-gray-700 hover:bg-gray-50 border'
                    }`}
                >
                  Next
                  <ArrowRightIcon className="h-4 w-4 ml-1" />
                </button>
              </div>
            </div>
          </div>
        </nav>
      )}
    </div>
  );
}

export default HistoryList; 