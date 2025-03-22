import React, { useState } from 'react';
import { ChevronDownIcon, ChevronUpIcon } from '@heroicons/react/24/solid';

function DetailedAnalysisPanel({ analysis }) {
  const [expandedSections, setExpandedSections] = useState({
    sentimentAnalysis: true,
    languageMetrics: false,
    sourceAnalysis: false,
    factChecking: false,
    contentFeatures: false
  });

  // Toggle section expansion
  const toggleSection = (section) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }));
  };

  // Render a collapsible section
  const Section = ({ id, title, children }) => {
    const isExpanded = expandedSections[id];
    
    return (
      <div className="border rounded-md mb-3 overflow-hidden">
        <button 
          className="w-full flex justify-between items-center p-3 bg-gray-50 hover:bg-gray-100 text-left font-medium"
          onClick={() => toggleSection(id)}
        >
          {title}
          {isExpanded ? (
            <ChevronUpIcon className="h-5 w-5 text-gray-500" />
          ) : (
            <ChevronDownIcon className="h-5 w-5 text-gray-500" />
          )}
        </button>
        
        {isExpanded && (
          <div className="p-4 bg-white">
            {children}
          </div>
        )}
      </div>
    );
  };

  // Format confidence level as color and text
  const formatConfidence = (score) => {
    let color;
    let label;
    
    if (score >= 0.8) {
      color = 'bg-green-100 text-green-800';
      label = 'High';
    } else if (score >= 0.5) {
      color = 'bg-yellow-100 text-yellow-800';
      label = 'Medium';
    } else {
      color = 'bg-red-100 text-red-800';
      label = 'Low';
    }
    
    return (
      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${color}`}>
        {label} ({(score * 100).toFixed(1)}%)
      </span>
    );
  };

  // Generate a bar chart for a metric
  const BarMeter = ({ value, label, colorClass = "bg-blue-500" }) => {
    // Ensure value is between 0 and 1
    const safeValue = Math.max(0, Math.min(1, value));
    const percentage = (safeValue * 100).toFixed(1);
    
    return (
      <div className="mb-2">
        <div className="flex justify-between mb-1">
          <span className="text-sm text-gray-600">{label}</span>
          <span className="text-sm font-medium">{percentage}%</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2.5">
          <div 
            className={`h-2.5 rounded-full ${colorClass}`}
            style={{ width: `${percentage}%` }}
          ></div>
        </div>
      </div>
    );
  };

  return (
    <div className="card">
      <h3 className="text-lg font-semibold mb-3">Detailed Analysis</h3>
      
      {analysis.sentiment && (
        <Section id="sentimentAnalysis" title="Sentiment Analysis">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <h4 className="font-medium mb-2">Overall Sentiment</h4>
              <div className="flex items-center mb-4">
                <div className="text-lg font-semibold">
                  {analysis.sentiment.label}
                </div>
                <div className="ml-2">
                  {formatConfidence(analysis.sentiment.confidence)}
                </div>
              </div>
              
              <BarMeter 
                label="Positive" 
                value={analysis.sentiment.scores?.positive || 0}
                colorClass="bg-green-500"
              />
              <BarMeter 
                label="Neutral" 
                value={analysis.sentiment.scores?.neutral || 0}
                colorClass="bg-gray-500"
              />
              <BarMeter 
                label="Negative" 
                value={analysis.sentiment.scores?.negative || 0}
                colorClass="bg-red-500"
              />
            </div>
            
            <div>
              <h4 className="font-medium mb-2">Emotional Tone</h4>
              {analysis.sentiment.emotions && Object.entries(analysis.sentiment.emotions).map(([emotion, value]) => (
                <BarMeter 
                  key={emotion}
                  label={emotion.charAt(0).toUpperCase() + emotion.slice(1)} 
                  value={value}
                  colorClass="bg-indigo-500"
                />
              ))}
            </div>
          </div>
        </Section>
      )}
      
      {analysis.language_metrics && (
        <Section id="languageMetrics" title="Language & Readability Metrics">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <h4 className="font-medium mb-2">Readability</h4>
              {analysis.language_metrics.readability && (
                <>
                  <div className="mb-3">
                    <div className="text-sm text-gray-600">Flesch Reading Ease</div>
                    <div className="flex items-center">
                      <div className="text-lg font-semibold">
                        {analysis.language_metrics.readability.flesch_reading_ease?.toFixed(1) || 'N/A'}
                      </div>
                      <div className="ml-2 text-sm text-gray-500">
                        {analysis.language_metrics.readability.flesch_reading_ease >= 80 ? 'Easy' : 
                         analysis.language_metrics.readability.flesch_reading_ease >= 60 ? 'Standard' : 'Difficult'}
                      </div>
                    </div>
                  </div>
                  
                  <div className="mb-3">
                    <div className="text-sm text-gray-600">Grade Level</div>
                    <div className="text-lg font-semibold">
                      {analysis.language_metrics.readability.grade_level?.toFixed(1) || 'N/A'}
                    </div>
                  </div>
                </>
              )}
            </div>
            
            <div>
              <h4 className="font-medium mb-2">Complexity Metrics</h4>
              {analysis.language_metrics.complexity && (
                <>
                  <BarMeter 
                    label="Lexical Diversity" 
                    value={analysis.language_metrics.complexity.lexical_diversity || 0}
                  />
                  <BarMeter 
                    label="Sentence Complexity" 
                    value={analysis.language_metrics.complexity.sentence_complexity || 0}
                  />
                </>
              )}
              
              <h4 className="font-medium mt-4 mb-2">Structure</h4>
              <div className="grid grid-cols-2 gap-2">
                <div className="text-center p-2 bg-gray-50 rounded">
                  <div className="text-sm text-gray-600">Words</div>
                  <div className="font-semibold">
                    {analysis.language_metrics.word_count || 0}
                  </div>
                </div>
                <div className="text-center p-2 bg-gray-50 rounded">
                  <div className="text-sm text-gray-600">Sentences</div>
                  <div className="font-semibold">
                    {analysis.language_metrics.sentence_count || 0}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </Section>
      )}
      
      {analysis.source_analysis && (
        <Section id="sourceAnalysis" title="Source & Authority Analysis">
          <div>
            {analysis.source_analysis.credibility_indicators && (
              <div className="mb-4">
                <h4 className="font-medium mb-2">Credibility Indicators</h4>
                <div className="space-y-2">
                  {Object.entries(analysis.source_analysis.credibility_indicators).map(([indicator, present]) => (
                    <div key={indicator} className="flex items-center">
                      <div className={`w-4 h-4 rounded-full mr-2 ${present ? 'bg-green-500' : 'bg-red-500'}`}></div>
                      <div className="text-sm">{indicator.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())}</div>
                    </div>
                  ))}
                </div>
              </div>
            )}
            
            {analysis.source_analysis.references && (
              <div>
                <h4 className="font-medium mb-2">References & Citations</h4>
                <div className="p-3 bg-gray-50 rounded">
                  <div className="mb-2">
                    <span className="text-sm text-gray-600">References Found:</span>
                    <span className="ml-2 font-semibold">{analysis.source_analysis.references.count || 0}</span>
                  </div>
                  
                  {analysis.source_analysis.references.sources && analysis.source_analysis.references.sources.length > 0 && (
                    <div>
                      <div className="text-sm text-gray-600 mb-1">Sources:</div>
                      <ul className="list-disc list-inside text-sm space-y-1">
                        {analysis.source_analysis.references.sources.map((source, index) => (
                          <li key={index}>{source}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        </Section>
      )}
      
      {analysis.fact_checking && (
        <Section id="factChecking" title="Fact Checking Results">
          <div>
            <h4 className="font-medium mb-2">Claim Verification</h4>
            
            {analysis.fact_checking.claims && analysis.fact_checking.claims.length > 0 ? (
              <div className="space-y-4">
                {analysis.fact_checking.claims.map((claim, index) => (
                  <div key={index} className="border-l-4 border-blue-500 pl-4">
                    <div className="font-medium">{claim.text}</div>
                    <div className="flex items-center mt-1">
                      <div className="text-sm text-gray-600 mr-2">Verification:</div>
                      <span 
                        className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium
                          ${claim.verified ? 'bg-green-100 text-green-800' : 
                             claim.verified === false ? 'bg-red-100 text-red-800' : 
                             'bg-yellow-100 text-yellow-800'}`}
                      >
                        {claim.verified ? 'Verified' : 
                         claim.verified === false ? 'Not Verified' : 
                         'Uncertain'}
                      </span>
                    </div>
                    {claim.explanation && (
                      <div className="text-sm mt-1">{claim.explanation}</div>
                    )}
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-gray-500">No specific claims were extracted for verification.</div>
            )}
            
            {analysis.fact_checking.consistency_score !== undefined && (
              <div className="mt-4">
                <div className="text-sm text-gray-600 mb-1">Overall Information Consistency</div>
                <BarMeter 
                  label="Consistency Score" 
                  value={analysis.fact_checking.consistency_score}
                  colorClass="bg-purple-500"
                />
              </div>
            )}
          </div>
        </Section>
      )}
      
      {analysis.content_features && (
        <Section id="contentFeatures" title="Content Features Analysis">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <h4 className="font-medium mb-2">Style Indicators</h4>
              {analysis.content_features.style_metrics && Object.entries(analysis.content_features.style_metrics).map(([metric, value]) => (
                <BarMeter 
                  key={metric}
                  label={metric.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())} 
                  value={value}
                  colorClass="bg-teal-500"
                />
              ))}
            </div>
            
            <div>
              <h4 className="font-medium mb-2">Content Red Flags</h4>
              {analysis.content_features.red_flags ? (
                <div className="space-y-2">
                  {Object.entries(analysis.content_features.red_flags).map(([flag, present]) => (
                    <div key={flag} className="flex items-center">
                      <div className={`w-4 h-4 rounded-full mr-2 ${present ? 'bg-red-500' : 'bg-gray-300'}`}></div>
                      <div className="text-sm">{flag.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())}</div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-gray-500">No content red flags detected.</div>
              )}
              
              {analysis.content_features.bias_indicators && (
                <div className="mt-4">
                  <h4 className="font-medium mb-2">Bias Detection</h4>
                  <div>
                    <div className="text-sm text-gray-600 mb-1">Political Bias</div>
                    <div className="relative h-6 bg-gray-200 rounded-full overflow-hidden">
                      <div className="absolute inset-0 flex items-center justify-center text-xs font-medium">
                        {analysis.content_features.bias_indicators.political_bias?.label || 'Neutral'}
                      </div>
                      <div 
                        className="absolute top-0 bottom-0 bg-blue-500 opacity-20"
                        style={{ 
                          left: '50%', 
                          right: analysis.content_features.bias_indicators.political_bias?.value > 0 ? 0 : undefined,
                          width: analysis.content_features.bias_indicators.political_bias?.value === 0 ? 0 :
                                 Math.abs(analysis.content_features.bias_indicators.political_bias?.value || 0) * 50 + '%'
                        }}
                      ></div>
                      <div 
                        className="absolute top-0 bottom-0 bg-red-500 opacity-20"
                        style={{ 
                          right: '50%', 
                          left: analysis.content_features.bias_indicators.political_bias?.value < 0 ? 0 : undefined,
                          width: analysis.content_features.bias_indicators.political_bias?.value === 0 ? 0 :
                                 Math.abs(analysis.content_features.bias_indicators.political_bias?.value || 0) * 50 + '%'
                        }}
                      ></div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </Section>
      )}
    </div>
  );
}

export default DetailedAnalysisPanel; 