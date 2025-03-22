import { useState, useEffect } from 'react'
import ResultCard from '../components/ResultCard'

function History() {
  const [history, setHistory] = useState([])
  const [isEmpty, setIsEmpty] = useState(true)
  
  useEffect(() => {
    // Load history from localStorage
    const savedHistory = localStorage.getItem('analysisHistory')
    if (savedHistory) {
      const parsedHistory = JSON.parse(savedHistory)
      setHistory(parsedHistory)
      setIsEmpty(parsedHistory.length === 0)
    }
  }, [])
  
  const clearHistory = () => {
    localStorage.removeItem('analysisHistory')
    setHistory([])
    setIsEmpty(true)
  }
  
  return (
    <div className="container">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold mb-2">Analysis History</h1>
          <p className="text-gray-600">
            View your recent news analysis results
          </p>
        </div>
        {!isEmpty && (
          <button 
            onClick={clearHistory}
            className="btn btn-secondary"
          >
            Clear History
          </button>
        )}
      </div>
      
      {isEmpty ? (
        <div className="card text-center py-12">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-16 w-16 text-gray-400 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <h2 className="text-2xl font-bold mb-2">No History Found</h2>
          <p className="text-gray-500 mb-6">
            You haven't analyzed any news articles yet.
          </p>
          <a href="/" className="btn btn-primary inline-block">
            Analyze News Now
          </a>
        </div>
      ) : (
        <div className="space-y-8">
          {history.map((result, index) => (
            <ResultCard key={index} result={result} />
          ))}
        </div>
      )}
    </div>
  )
}

export default History 