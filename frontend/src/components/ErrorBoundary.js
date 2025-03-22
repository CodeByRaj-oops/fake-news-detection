import React, { Component } from 'react';
import newsApi from '../api/newsApi';

class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { 
      hasError: false,
      errorInfo: null,
      serverOnline: true,
      retryCount: 0,
      lastCheck: 0
    };
    
    // Check server status every 30 seconds when in error state
    this.intervalId = null;
  }

  static getDerivedStateFromError(error) {
    // Update state so the next render will show the fallback UI
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    this.setState({ 
      errorInfo,
      lastCheck: Date.now()
    });
    
    // Check if server is online
    this.checkServerStatus();
    
    // Start periodic checks
    this.startPeriodicChecks();
    
    // Log error to an error reporting service
    console.error('Error caught by ErrorBoundary:', error, errorInfo);
  }
  
  componentWillUnmount() {
    // Clear interval when component unmounts
    if (this.intervalId) {
      clearInterval(this.intervalId);
    }
  }
  
  startPeriodicChecks() {
    // Clear any existing interval
    if (this.intervalId) {
      clearInterval(this.intervalId);
    }
    
    // Check every 30 seconds
    this.intervalId = setInterval(() => {
      this.checkServerStatus();
    }, 30000);
  }
  
  async checkServerStatus() {
    try {
      const result = await newsApi.checkServerStatus();
      
      // If server is back online and we were previously offline,
      // reset the error state to allow the app to try again
      if (result.online && !this.state.serverOnline) {
        this.setState({ 
          hasError: false,
          serverOnline: true,
          retryCount: 0
        });
      } else {
        this.setState({ 
          serverOnline: result.online,
          lastCheck: Date.now()
        });
      }
    } catch (error) {
      this.setState({ 
        serverOnline: false,
        lastCheck: Date.now()
      });
    }
  }
  
  handleRetry = () => {
    // Increment retry count
    this.setState(prevState => ({
      retryCount: prevState.retryCount + 1
    }));
    
    // Check server status
    this.checkServerStatus();
    
    // If server is online or we've tried fewer than 3 times, reset error state
    if (this.state.serverOnline || this.state.retryCount < 3) {
      this.setState({ hasError: false });
    }
  }

  render() {
    if (this.state.hasError) {
      const lastCheckTime = new Date(this.state.lastCheck).toLocaleTimeString();
      
      return (
        <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
          <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
            <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
              <div className="text-center">
                <h2 className="mt-2 text-2xl font-bold text-gray-900">
                  Connection Error
                </h2>
                
                <div className="mt-4 bg-red-50 border border-red-200 rounded-md p-4">
                  <div className="flex">
                    <div className="flex-shrink-0">
                      <svg className="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                      </svg>
                    </div>
                    <div className="ml-3">
                      <h3 className="text-sm font-medium text-red-800">
                        No response received from the server
                      </h3>
                      <div className="mt-2 text-sm text-red-700">
                        <p>
                          Server status: <span className={this.state.serverOnline ? "text-green-600 font-semibold" : "text-red-600 font-semibold"}>
                            {this.state.serverOnline ? "Online" : "Offline"}
                          </span>
                          <span className="text-xs text-gray-500 ml-2">
                            (Last checked: {lastCheckTime})
                          </span>
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div className="mt-6">
                  <h3 className="text-sm font-medium text-gray-700">
                    Possible reasons:
                  </h3>
                  <ul className="mt-2 text-sm text-gray-500 list-disc list-inside text-left">
                    <li>The backend server is not running</li>
                    <li>Your internet connection is interrupted</li>
                    <li>The server is temporarily unavailable</li>
                  </ul>
                </div>
                
                <div className="mt-6">
                  <h3 className="text-sm font-medium text-gray-700">
                    Try these solutions:
                  </h3>
                  <ul className="mt-2 text-sm text-gray-500 list-disc list-inside text-left">
                    <li>Check if the backend server is running</li>
                    <li>Verify your internet connection</li>
                    <li>Wait a few moments and try again</li>
                  </ul>
                </div>
                
                <div className="mt-6">
                  <button
                    onClick={this.handleRetry}
                    className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                  >
                    Retry Connection
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      );
    }

    // Render children if no error
    return this.props.children;
  }
}

export default ErrorBoundary; 