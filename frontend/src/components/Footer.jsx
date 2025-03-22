function Footer() {
  return (
    <footer className="bg-gray-800 text-white py-6">
      <div className="container mx-auto px-6">
        <div className="flex flex-col md:flex-row justify-between items-center">
          <div className="mb-4 md:mb-0">
            <p className="text-center md:text-left">&copy; {new Date().getFullYear()} Fake News Detector - All rights reserved</p>
          </div>
          <div className="flex space-x-4">
            <a href="https://github.com" className="hover:text-blue-400" target="_blank" rel="noopener noreferrer">GitHub</a>
            <a href="#" className="hover:text-blue-400">Privacy Policy</a>
            <a href="#" className="hover:text-blue-400">Terms of Service</a>
          </div>
        </div>
      </div>
    </footer>
  )
}

export default Footer 