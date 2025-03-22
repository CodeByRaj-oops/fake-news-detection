import React from 'react';
import HistoryList from '../components/HistoryList';
import { ClockIcon } from '@heroicons/react/24/outline';

function HistoryPage() {
  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      <div className="text-center mb-8">
        <ClockIcon className="h-12 w-12 text-indigo-600 mx-auto" />
        <h1 className="mt-2 text-3xl font-extrabold text-gray-900 sm:text-4xl">
          Analysis History
        </h1>
        <p className="mt-3 max-w-2xl mx-auto text-xl text-gray-500 sm:mt-4">
          View and access your past content analyses.
        </p>
      </div>

      <HistoryList />

      <div className="mt-8">
        <div className="card bg-gray-50">
          <h2 className="text-xl font-semibold mb-4">About Your History</h2>
          <p className="text-gray-600 mb-3">
            Your analysis history is stored locally in your browser. This allows you to:
          </p>
          <ul className="list-disc list-inside text-gray-600 space-y-1 mb-3">
            <li>Review past analyses for reference</li>
            <li>Compare results across different content</li>
            <li>Track analysis patterns over time</li>
            <li>Access detailed reports from your previous sessions</li>
          </ul>
          <p className="text-gray-600 text-sm">
            <strong>Note:</strong> Clearing your browser data will also clear your analysis history.
          </p>
        </div>
      </div>
    </div>
  );
}

export default HistoryPage; 