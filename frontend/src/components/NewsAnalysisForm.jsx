import { useState } from 'react'
import axios from 'axios'

function NewsAnalysisForm({ onResultReceived }) {
  const [newsText, setNewsText] = useState('')
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [error, setError] = useState('')
  
  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!newsText.trim()) {
      setError('Please enter some news text to analyze')
      return
    }
    
    setError('')
    setIsAnalyzing(true)
    
    try {
      const response = await axios.post('/api/analyze', { text: newsText })
      onResultReceived({
        ...response.data,
        text: newsText,
        timestamp: new Date().toISOString()
      })
      setNewsText('')
    } catch (err) {
      console.error('Error analyzing news:', err)
      setError('Failed to analyze news. Please try again.')
    } finally {
      setIsAnalyzing(false)
    }
  }
  
  return (
    <div className="card">
      <h2 className="text-2xl font-bold mb-4">Analyze News</h2>
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label htmlFor="newsText" className="block text-gray-700 mb-2">
            Enter news text or paste an article
          </label>
          <textarea
            id="newsText"
            className="input-field h-40"
            value={newsText}
            onChange={(e) => setNewsText(e.target.value)}
            placeholder="Paste news article or type text here..."
          ></textarea>
          {error && <p className="text-red-500 mt-1">{error}</p>}
        </div>
        <button 
          type="submit" 
          className="btn btn-primary w-full"
          disabled={isAnalyzing}
        >
          {isAnalyzing ? 'Analyzing...' : 'Analyze'}
        </button>
      </form>
    </div>
  )
}

export default NewsAnalysisForm 