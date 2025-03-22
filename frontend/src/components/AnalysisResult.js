import React from 'react';
import { useAnalysis } from '../contexts/AnalysisContext';
import { 
  CheckCircleIcon, 
  ExclamationCircleIcon, 
  InformationCircleIcon 
} from '@heroicons/react/24/solid';
import CredibilityMeter from './CredibilityMeter';
import DetailedAnalysisPanel from './DetailedAnalysisPanel';
import ModelExplanationPanel from './ModelExplanationPanel';

function AnalysisResult() {
  const { analysisResult, analysisText } = useAnalysis();

  if (!analysisResult) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-500">No analysis results available. Please analyze some text first.</p>
      </div>
    );
  }

  const { 
    prediction, 
    confidence, 
    credibility_score: credibilityScore,
    explanation, 
    detailed_analysis: detailedAnalysis,
    model_explanations: modelExplanations,
    timestamp 
  } = analysisResult;

  // Format confidence as percentage
  const confidencePercent = (confidence * 100).toFixed(1);
  
  // Format timestamp
  const formattedDate = new Date(timestamp).toLocaleString();

  // Determine result icon and color based on prediction
  const getResultDisplay = () => {
    if (prediction === 'REAL') {
      return {
        icon: <CheckCircleIcon className="h-12 w-12 text-real" />,
        textColor: 'text-real',
        bgColor: 'bg-green-50',
        title: 'Likely Real News',
        description: 'The content appears to be reliable information.',
      };
    } else if (prediction === 'FAKE') {
      return {
        icon: <ExclamationCircleIcon className="h-12 w-12 text-fake" />,
        textColor: 'text-fake',
        bgColor: 'bg-red-50',
        title: 'Likely Fake News',
        description: 'The content appears to contain misinformation.',
      };
    } else {
      return {
        icon: <InformationCircleIcon className="h-12 w-12 text-neutral" />,
        textColor: 'text-neutral',
        bgColor: 'bg-gray-50',
        title: 'Uncertain',
        description: 'Unable to determine reliability with confidence.',
      };
    }
  };

  const resultDisplay = getResultDisplay();

  return (
    <div className="space-y-6">
      {/* Analysis summary */}
      <div className={`${resultDisplay.bgColor} p-6 rounded-lg shadow-sm border`}>
        <div className="flex flex-col md:flex-row md:items-center gap-4">
          <div className="flex-shrink-0">
            {resultDisplay.icon}
          </div>
          <div className="flex-grow">
            <h2 className={`text-xl font-semibold ${resultDisplay.textColor}`}>
              {resultDisplay.title}
            </h2>
            <p className="text-gray-600">{resultDisplay.description}</p>
            <p className="text-gray-500 text-sm mt-1">
              Confidence: <span className="font-semibold">{confidencePercent}%</span>
            </p>
          </div>
          
          {/* Credibility score meter if available */}
          {credibilityScore !== undefined && (
            <div className="flex-shrink-0 mt-4 md:mt-0">
              <CredibilityMeter score={credibilityScore} />
            </div>
          )}
        </div>
      </div>

      {/* Original text */}
      <div className="card">
        <h3 className="text-lg font-semibold mb-3">Analyzed Text</h3>
        <div className="p-4 bg-gray-50 rounded-md border border-gray-200 max-h-48 overflow-y-auto">
          <p className="whitespace-pre-wrap">{analysisText}</p>
        </div>
      </div>

      {/* Explanation if available */}
      {explanation && (
        <div className="card">
          <h3 className="text-lg font-semibold mb-3">Analysis Explanation</h3>
          <div className="p-4 bg-gray-50 rounded-md border border-gray-200">
            <p>{explanation}</p>
          </div>
        </div>
      )}

      {/* Model explanations */}
      {modelExplanations && (
        <ModelExplanationPanel explanations={modelExplanations} />
      )}

      {/* Detailed analysis if available */}
      {detailedAnalysis && (
        <DetailedAnalysisPanel analysis={detailedAnalysis} />
      )}

      {/* Analysis metadata */}
      <div className="text-right text-gray-500 text-sm">
        Analysis performed: {formattedDate}
      </div>
    </div>
  );
}

export default AnalysisResult; 