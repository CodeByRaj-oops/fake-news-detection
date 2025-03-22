import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useAnalysis } from '../contexts/AnalysisContext';
import { 
  DocumentChartBarIcon, 
  ChartBarIcon,
  DocumentTextIcon,
  ArrowDownTrayIcon,
  TrashIcon,
  ArrowLeftIcon,
  ArrowRightIcon,
  ClockIcon
} from '@heroicons/react/24/outline';

function ReportsPage() {
  const { reports, loadReports, loading, error } = useAnalysis();
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage] = useState(10);

  useEffect(() => {
    loadReports(itemsPerPage, (currentPage - 1) * itemsPerPage);
  }, [currentPage, itemsPerPage, loadReports]);

  // Calculate total pages
  const totalPages = Math.ceil((reports?.total || 0) / itemsPerPage);

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

  if (loading) {
    return (
      <div className="max-w-5xl mx-auto px-4 py-8">
        <div className="text-center mb-8">
          <DocumentChartBarIcon className="h-12 w-12 text-indigo-600 mx-auto" />
          <h1 className="mt-2 text-3xl font-extrabold text-gray-900 sm:text-4xl">
            Analysis Reports
          </h1>
        </div>
        <div className="flex justify-center items-center min-h-[300px]">
          <div className="animate-pulse space-y-6 w-full max-w-2xl">
            <div className="h-10 bg-gray-200 rounded w-1/2 mx-auto"></div>
            <div className="space-y-3">
              <div className="h-20 bg-gray-200 rounded"></div>
              <div className="h-20 bg-gray-200 rounded"></div>
              <div className="h-20 bg-gray-200 rounded"></div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-5xl mx-auto px-4 py-8">
        <div className="text-center mb-8">
          <DocumentChartBarIcon className="h-12 w-12 text-indigo-600 mx-auto" />
          <h1 className="mt-2 text-3xl font-extrabold text-gray-900 sm:text-4xl">
            Analysis Reports
          </h1>
        </div>
        <div className="bg-red-50 border-l-4 border-red-400 p-4 mb-6">
          <div className="flex">
            <div>
              <p className="text-red-700">
                Error loading reports: {error}
              </p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      <div className="text-center mb-8">
        <DocumentChartBarIcon className="h-12 w-12 text-indigo-600 mx-auto" />
        <h1 className="mt-2 text-3xl font-extrabold text-gray-900 sm:text-4xl">
          Analysis Reports
        </h1>
        <p className="mt-3 max-w-2xl mx-auto text-xl text-gray-500 sm:mt-4">
          View and download your detailed analysis reports.
        </p>
      </div>

      {/* Reports list */}
      {!reports || reports.items?.length === 0 ? (
        <div className="text-center py-12">
          <DocumentTextIcon className="h-16 w-16 text-gray-300 mx-auto mb-4" />
          <h3 className="text-xl font-medium text-gray-900">No Reports Available</h3>
          <p className="text-gray-500 mt-2 mb-8">
            You don't have any saved analysis reports yet.
          </p>
          <Link to="/analyzer" className="btn-primary">
            Create Your First Report
          </Link>
          <div className="mt-8 max-w-2xl mx-auto">
            <div className="bg-blue-50 rounded-lg p-4 text-left">
              <h4 className="font-medium text-blue-800 mb-2">How to Create Reports</h4>
              <p className="text-blue-700 text-sm">
                When analyzing content, check the "Save as Report" option before submitting. 
                Reports include more comprehensive analysis than standard history items, 
                including detailed fact-checking and content analysis.
              </p>
            </div>
          </div>
        </div>
      ) : (
        <div className="space-y-4">
          <div className="overflow-hidden bg-white shadow sm:rounded-md">
            <ul className="divide-y divide-gray-200">
              {reports.items.map((report) => (
                <li key={report.id}>
                  <Link to={`/reports/${report.id}`} className="block hover:bg-gray-50">
                    <div className="px-4 py-4 sm:px-6">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center">
                          <ChartBarIcon className="h-5 w-5 text-indigo-600" />
                          <p className="ml-2 text-sm font-medium text-gray-900">
                            {report.title || `Report #${report.id}`}
                          </p>
                        </div>
                        <div className="flex items-center">
                          <ArrowDownTrayIcon className="h-5 w-5 text-gray-400 hover:text-indigo-600 cursor-pointer" />
                          <TrashIcon className="ml-2 h-5 w-5 text-gray-400 hover:text-red-600 cursor-pointer" />
                        </div>
                      </div>
                      <div className="mt-2 sm:flex sm:justify-between">
                        <div className="sm:flex-grow">
                          <p className="text-sm text-gray-500 line-clamp-2">
                            {truncateText(report.summary || report.text, 150)}
                          </p>
                        </div>
                        <div className="mt-2 flex items-center text-sm text-gray-500 sm:mt-0">
                          <ClockIcon className="h-4 w-4 mr-1" />
                          {formatDate(report.timestamp)}
                        </div>
                      </div>
                      <div className="mt-2">
                        <div className="flex flex-wrap">
                          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800 mr-2 mb-1">
                            {report.prediction === 'REAL' ? 'Likely Real' : 
                             report.prediction === 'FAKE' ? 'Likely Fake' : 'Uncertain'}
                          </span>
                          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800 mr-2 mb-1">
                            Confidence: {(report.confidence * 100).toFixed(1)}%
                          </span>
                          {report.detailed_analysis && (
                            <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800 mr-2 mb-1">
                              Detailed
                            </span>
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
                      {Math.min(currentPage * itemsPerPage, reports.total)}
                    </span>{' '}
                    of <span className="font-medium">{reports.total}</span> results
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
      )}

      {/* About reports section */}
      <div className="mt-12">
        <div className="card">
          <h2 className="text-xl font-semibold mb-4">About Saved Reports</h2>
          <p className="text-gray-600 mb-4">
            Saved reports provide comprehensive analysis of content and include:
          </p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="bg-gray-50 p-4 rounded-md">
              <h3 className="font-medium text-gray-900 mb-2">Report Features</h3>
              <ul className="text-gray-600 space-y-1 list-disc list-inside">
                <li>Detailed sentiment analysis</li>
                <li>Source credibility assessment</li>
                <li>Linguistic pattern examination</li>
                <li>Fact verification results</li>
                <li>Content bias indicators</li>
              </ul>
            </div>
            <div className="bg-gray-50 p-4 rounded-md">
              <h3 className="font-medium text-gray-900 mb-2">Available Actions</h3>
              <ul className="text-gray-600 space-y-1 list-disc list-inside">
                <li>Download reports as PDF</li>
                <li>Share reports via link</li>
                <li>Compare multiple analyses</li>
                <li>View historical trends</li>
                <li>Delete unwanted reports</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ReportsPage; 