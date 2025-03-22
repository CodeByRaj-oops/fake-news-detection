import React, { useState } from 'react';
import { ChevronDownIcon, ChevronUpIcon } from '@heroicons/react/24/solid';
import { LightBulbIcon, AdjustmentsHorizontalIcon } from '@heroicons/react/24/outline';

/**
 * Component for displaying model explanations (LIME and SHAP)
 */
function ModelExplanationPanel({ explanations }) {
  const [expanded, setExpanded] = useState(true);
  const [activeTab, setActiveTab] = useState('lime');

  if (!explanations) {
    return null;
  }

  // Toggle panel expansion
  const toggleExpanded = () => {
    setExpanded(!expanded);
  };

  // Handle tab change
  const handleTabChange = (tab) => {
    setActiveTab(tab);
  };

  // Function to render feature importance bars
  const renderFeatureImportance = (features) => {
    if (!features || features.length === 0) {
      return <p className="text-gray-500">No feature importance data available.</p>;
    }

    // Get max absolute importance to normalize
    const maxImportance = Math.max(...features.map(f => Math.abs(f.importance)));

    return (
      <div className="space-y-2 my-3">
        {features.map((feature, index) => {
          // Normalize importance to -100 to 100 range
          const normalizedImportance = (feature.importance / maxImportance) * 100;
          const isPositive = feature.importance >= 0;
          
          return (
            <div key={index} className="flex items-center text-sm">
              <div className="w-32 text-right pr-2 truncate font-medium">
                {feature.word}
              </div>
              <div className="flex-1 relative h-6">
                {/* Show bar from center for positive/negative values */}
                <div className="absolute top-0 bottom-0 w-px bg-gray-300 left-1/2"></div>
                
                {/* The bar */}
                <div 
                  className={`absolute top-0 h-full ${isPositive ? 'bg-green-500 left-1/2' : 'bg-red-500 right-1/2'}`}
                  style={{ 
                    width: `${Math.abs(normalizedImportance) / 2}%`,
                  }}
                ></div>
                
                {/* Value */}
                <div 
                  className={`absolute top-0 h-full flex items-center ${isPositive ? 'left-1/2 pl-1 ml-1' : 'right-1/2 pr-1 mr-1'} text-xs font-medium`}
                >
                  {feature.importance.toFixed(4)}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    );
  };

  // Function to render highlighted text (if available)
  const renderHighlightedText = (highlightedText) => {
    if (!highlightedText) {
      return null;
    }

    return (
      <div className="mt-4">
        <h4 className="text-md font-medium mb-2">Highlighted Text</h4>
        <div 
          className="p-3 bg-gray-50 border rounded-md max-h-48 overflow-y-auto"
          dangerouslySetInnerHTML={{ __html: highlightedText }}
        />
      </div>
    );
  };

  // Get explanations based on active tab
  let tabContent = null;
  let highlightedText = null;

  if (activeTab === 'lime' && explanations.lime_explanations) {
    const limeData = explanations.lime_explanations;
    tabContent = (
      <div>
        <div className="flex items-center gap-2 mb-3">
          <LightBulbIcon className="h-5 w-5 text-yellow-500" />
          <div className="text-sm text-gray-600">
            LIME explains predictions by perturbing the input and seeing how the predictions change.
          </div>
        </div>
        
        <div className="mb-3">
          <div className="text-sm text-gray-600">Prediction:</div>
          <div className="font-medium">
            {limeData.predicted_class} ({(limeData.probability * 100).toFixed(1)}%)
          </div>
        </div>

        <div>
          <h4 className="text-md font-medium mb-1">Top Features</h4>
          {renderFeatureImportance(limeData.top_features)}
        </div>
      </div>
    );
    
    // If highlighted text is available
    highlightedText = explanations.highlighted_text;
    
  } else if (activeTab === 'shap' && explanations.shap_explanations) {
    const shapData = explanations.shap_explanations;
    tabContent = (
      <div>
        <div className="flex items-center gap-2 mb-3">
          <AdjustmentsHorizontalIcon className="h-5 w-5 text-blue-500" />
          <div className="text-sm text-gray-600">
            SHAP (SHapley Additive exPlanations) uses game theory to assign each feature an importance value.
          </div>
        </div>
        
        <div className="mb-3">
          <div className="text-sm text-gray-600">Base Value:</div>
          <div className="font-medium">
            {shapData.base_value ? shapData.base_value.toFixed(4) : 'N/A'}
          </div>
        </div>

        <div>
          <h4 className="text-md font-medium mb-1">Top Features</h4>
          {renderFeatureImportance(shapData.top_features)}
        </div>
      </div>
    );
    
    // If highlighted text is available
    highlightedText = explanations.highlighted_text;
    
  } else {
    tabContent = (
      <div className="text-center py-4 text-gray-500">
        No explanation data available for the selected method.
      </div>
    );
  }

  return (
    <div className="card">
      <div 
        className="flex justify-between items-center cursor-pointer"
        onClick={toggleExpanded}
      >
        <h3 className="text-lg font-semibold">Model Explanations</h3>
        {expanded ? (
          <ChevronUpIcon className="h-5 w-5 text-gray-500" />
        ) : (
          <ChevronDownIcon className="h-5 w-5 text-gray-500" />
        )}
      </div>
      
      {expanded && (
        <div className="mt-3">
          {/* Tabs */}
          <div className="border-b border-gray-200">
            <nav className="flex space-x-4" aria-label="Explanation methods">
              <button
                onClick={() => handleTabChange('lime')}
                className={`px-3 py-2 text-sm font-medium border-b-2 ${
                  activeTab === 'lime'
                    ? 'border-indigo-500 text-indigo-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                LIME
              </button>
              <button
                onClick={() => handleTabChange('shap')}
                className={`px-3 py-2 text-sm font-medium border-b-2 ${
                  activeTab === 'shap'
                    ? 'border-indigo-500 text-indigo-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                SHAP
              </button>
            </nav>
          </div>
          
          {/* Tab content */}
          <div className="py-4">
            {tabContent}
            {renderHighlightedText(highlightedText)}
          </div>
        </div>
      )}
    </div>
  );
}

export default ModelExplanationPanel; 