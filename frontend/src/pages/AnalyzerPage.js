import React from 'react';
import TextAnalysisForm from '../components/TextAnalysisForm';
import AnalysisResult from '../components/AnalysisResult';
import { useAnalysis } from '../contexts/AnalysisContext';
import { NewspaperIcon } from '@heroicons/react/24/outline';

function AnalyzerPage() {
  const { analysisResult, loading, error } = useAnalysis();

  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      <div className="text-center mb-8">
        <NewspaperIcon className="h-12 w-12 text-indigo-600 mx-auto" />
        <h1 className="mt-2 text-3xl font-extrabold text-gray-900 sm:text-4xl">
          Fake News Analyzer
        </h1>
        <p className="mt-3 max-w-2xl mx-auto text-xl text-gray-500 sm:mt-4">
          Paste any news article, social media post, or suspicious content to analyze its authenticity.
        </p>
      </div>

      <div className="grid grid-cols-1 gap-8 lg:grid-cols-12">
        {/* Left column - Analysis form */}
        <div className="lg:col-span-5">
          <div className="card">
            <h2 className="text-xl font-semibold mb-4">Submit Text for Analysis</h2>
            <TextAnalysisForm />
          </div>
          
          {/* Error message */}
          {error && (
            <div className="mt-4 bg-red-50 border-l-4 border-red-400 p-4">
              <div className="flex">
                <div>
                  <p className="text-sm text-red-700">
                    {error}
                  </p>
                </div>
              </div>
            </div>
          )}
          
          {/* Analysis tips */}
          <div className="mt-6 bg-blue-50 rounded-lg p-4">
            <h3 className="font-medium text-blue-800 mb-2">Tips for Best Results</h3>
            <ul className="text-sm text-blue-700 space-y-1 list-disc list-inside">
              <li>Include complete article text when possible</li>
              <li>Analysis works best on news content, not opinion pieces</li>
              <li>Longer text provides more accurate analysis</li>
              <li>Check your text for copy/paste errors</li>
            </ul>
          </div>
        </div>
        
        {/* Right column - Analysis results */}
        <div className="lg:col-span-7">
          {loading ? (
            <div className="card">
              <div className="animate-pulse space-y-4">
                <div className="h-24 bg-gray-200 rounded"></div>
                <div className="h-10 bg-gray-200 rounded w-3/4"></div>
                <div className="space-y-2">
                  <div className="h-4 bg-gray-200 rounded"></div>
                  <div className="h-4 bg-gray-200 rounded w-5/6"></div>
                  <div className="h-4 bg-gray-200 rounded w-4/6"></div>
                </div>
                <div className="h-40 bg-gray-200 rounded"></div>
              </div>
            </div>
          ) : (
            <AnalysisResult />
          )}
        </div>
      </div>
      
      {/* How it works section */}
      <div className="mt-16">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">How Our Analyzer Works</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="card">
            <div className="text-indigo-600 text-lg font-semibold mb-2">1. Text Analysis</div>
            <p className="text-gray-600">
              Our system analyzes writing style, tone, emotional content, and linguistic patterns to identify potential fake news.
            </p>
          </div>
          <div className="card">
            <div className="text-indigo-600 text-lg font-semibold mb-2">2. Fact Checking</div>
            <p className="text-gray-600">
              Key claims are extracted and compared with a database of verified information using natural language processing.
            </p>
          </div>
          <div className="card">
            <div className="text-indigo-600 text-lg font-semibold mb-2">3. Source Verification</div>
            <p className="text-gray-600">
              We examine source credibility indicators and assess whether the content follows journalistic standards.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default AnalyzerPage; 