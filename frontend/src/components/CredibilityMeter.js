import React from 'react';

function CredibilityMeter({ score }) {
  // Ensure score is between 0 and 100
  const validScore = Math.max(0, Math.min(100, score));
  
  // Determine color based on score
  const getColorClass = () => {
    if (validScore >= 70) return 'text-real';
    if (validScore >= 40) return 'text-neutral';
    return 'text-fake';
  };

  // Get score label
  const getScoreLabel = () => {
    if (validScore >= 80) return 'Very Credible';
    if (validScore >= 60) return 'Credible';
    if (validScore >= 40) return 'Neutral';
    if (validScore >= 20) return 'Questionable';
    return 'Not Credible';
  };

  // Calculate rotation for gauge needle (0 to 180 degrees)
  const needleRotation = (validScore / 100) * 180;

  return (
    <div className="flex flex-col items-center">
      <div className="text-center mb-1">
        <span className="text-sm text-gray-600">Credibility Score</span>
      </div>
      
      {/* Score number */}
      <div className={`text-2xl font-bold ${getColorClass()}`}>
        {validScore}%
      </div>
      
      {/* Score label */}
      <div className={`text-sm font-medium ${getColorClass()}`}>
        {getScoreLabel()}
      </div>
      
      {/* Semicircular gauge */}
      <div className="relative w-24 h-12 mt-1">
        {/* Gauge background */}
        <div className="absolute w-full h-full overflow-hidden">
          <div className="absolute bottom-0 w-full h-full rounded-t-full bg-gradient-to-r from-red-500 via-yellow-400 to-green-500 opacity-20"></div>
        </div>
        
        {/* Gauge needle */}
        <div className="absolute bottom-0 left-1/2 w-1 h-11 bg-gray-800 origin-bottom transform -translate-x-1/2" 
             style={{ transform: `translateX(-50%) rotate(${needleRotation - 90}deg)` }}>
          <div className="absolute -top-1 -left-1 w-3 h-3 rounded-full bg-gray-800"></div>
        </div>
        
        {/* Gauge ticks */}
        <div className="absolute bottom-0 w-full flex justify-between px-1">
          <div className="h-2 w-0.5 bg-gray-400"></div>
          <div className="h-1 w-0.5 bg-gray-300"></div>
          <div className="h-2 w-0.5 bg-gray-400"></div>
          <div className="h-1 w-0.5 bg-gray-300"></div>
          <div className="h-2 w-0.5 bg-gray-400"></div>
        </div>
      </div>
    </div>
  );
}

export default CredibilityMeter; 