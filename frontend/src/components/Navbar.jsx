import { Link, useLocation } from 'react-router-dom'

function Navbar() {
  const location = useLocation()
  
  return (
    <nav className="bg-white shadow-md">
      <div className="container mx-auto px-6 py-3 flex justify-between items-center">
        <div className="flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-blue-600 mr-2" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
            <line x1="16" y1="13" x2="8" y2="13"></line>
            <line x1="16" y1="17" x2="8" y2="17"></line>
            <line x1="10" y1="9" x2="8" y2="9"></line>
          </svg>
          <Link to="/" className="text-xl font-bold text-gray-800">Fake News Detector</Link>
        </div>
        <div className="flex space-x-6">
          <Link to="/" className={`${location.pathname === '/' ? 'text-blue-600 font-medium' : 'text-gray-600 hover:text-blue-500'}`}>
            Home
          </Link>
          <Link to="/history" className={`${location.pathname === '/history' ? 'text-blue-600 font-medium' : 'text-gray-600 hover:text-blue-500'}`}>
            History
          </Link>
          <Link to="/about" className={`${location.pathname === '/about' ? 'text-blue-600 font-medium' : 'text-gray-600 hover:text-blue-500'}`}>
            About
          </Link>
        </div>
      </div>
    </nav>
  )
}

export default Navbar 