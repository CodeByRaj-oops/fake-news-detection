function ResultCard({ result }) {
  if (!result) return null
  
  const { prediction, confidence, text, timestamp } = result
  
  // Format confidence as percentage
  const confidencePercent = (confidence * 100).toFixed(2)
  
  // Format timestamp
  const formattedDate = new Date(timestamp).toLocaleString()
  
  return (
    <div className="card mt-8">
      <h2 className="text-2xl font-bold mb-4">Analysis Result</h2>
      
      <div className="flex justify-between items-center mb-6">
        <div>
          <span className="text-gray-500">Prediction:</span>
          <span className={`text-2xl font-bold ml-2 ${prediction === 'REAL' ? 'text-green-600' : 'text-red-600'}`}>
            {prediction}
          </span>
        </div>
        <div>
          <span className="text-gray-500">Confidence:</span>
          <span className="text-xl font-semibold ml-2">
            {confidencePercent}%
          </span>
        </div>
      </div>
      
      <div className="w-full bg-gray-200 rounded-full h-2.5 mb-6">
        <div 
          className={`h-2.5 rounded-full ${prediction === 'REAL' ? 'bg-green-600' : 'bg-red-600'}`}
          style={{ width: `${confidencePercent}%` }}
        ></div>
      </div>
      
      <div className="mb-4">
        <h3 className="text-lg font-semibold mb-2">Text Analyzed:</h3>
        <div className="bg-gray-50 p-3 rounded border border-gray-200 max-h-32 overflow-y-auto">
          <p className="text-gray-700">{text}</p>
        </div>
      </div>
      
      <div className="text-right text-sm text-gray-500">
        <span>Analyzed on: {formattedDate}</span>
      </div>
    </div>
  )
}

export default ResultCard 