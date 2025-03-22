import { useState, useEffect } from 'react'
import NewsAnalysisForm from '../components/NewsAnalysisForm'
import ResultCard from '../components/ResultCard'

function Home() {
  const [result, setResult] = useState(null)
  const [history, setHistory] = useState([])
  
  useEffect(() => {
    // Load history from localStorage on component mount
    const savedHistory = localStorage.getItem('analysisHistory')
    if (savedHistory) {
      setHistory(JSON.parse(savedHistory))
    }
  }, [])
  
  const handleResultReceived = (newResult) => {
    setResult(newResult)
    
    // Update history and save to localStorage
    const updatedHistory = [newResult, ...history].slice(0, 10) // Keep last 10 items
    setHistory(updatedHistory)
    localStorage.setItem('analysisHistory', JSON.stringify(updatedHistory))
  }
  
  return (
    <div className="container">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Fake News Detection</h1>
        <p className="text-gray-600">
          Enter news text and our AI-powered system will analyze whether it's likely to be real or fake.
        </p>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div>
          <NewsAnalysisForm onResultReceived={handleResultReceived} />
        </div>
        <div>
          {result && <ResultCard result={result} />}
          {!result && (
            <div className="card h-full flex items-center justify-center bg-gray-50">
              <div className="text-center p-8">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-16 w-16 text-gray-400 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
                <h3 className="text-xl font-semibold mb-2">No Results Yet</h3>
                <p className="text-gray-500">
                  Enter news text and analyze it to see the results here.
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default Home 