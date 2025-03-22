import React from 'react';
import { Link } from 'react-router-dom';
import { ExclamationCircleIcon } from '@heroicons/react/24/outline';

function NotFoundPage() {
  return (
    <div className="min-h-screen flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="text-center">
          <ExclamationCircleIcon className="h-16 w-16 text-indigo-600 mx-auto" />
          <h1 className="mt-6 text-3xl font-extrabold text-gray-900">Page Not Found</h1>
          <p className="mt-2 text-base text-gray-500">
            The page you're looking for doesn't exist or has been moved.
          </p>
        </div>
        
        <div className="mt-8 text-center">
          <Link to="/" className="inline-flex items-center px-4 py-2 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700">
            Return to Homepage
          </Link>
        </div>
        
        <div className="mt-12 border-t border-gray-200 pt-8">
          <div className="space-y-4">
            <p className="text-center text-base text-gray-500">
              You might be interested in:
            </p>
            <ul className="space-y-3">
              <li>
                <Link to="/analyzer" className="block text-center text-indigo-600 hover:text-indigo-500">
                  Analyze Content
                </Link>
              </li>
              <li>
                <Link to="/history" className="block text-center text-indigo-600 hover:text-indigo-500">
                  View Analysis History
                </Link>
              </li>
              <li>
                <Link to="/reports" className="block text-center text-indigo-600 hover:text-indigo-500">
                  Check Analysis Reports
                </Link>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}

export default NotFoundPage; 