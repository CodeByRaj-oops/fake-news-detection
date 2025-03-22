import React, { useEffect } from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import './index.css';
import App from './App';
import { trackRouterMount } from './utils/RouterValidator';
import { AnalysisProvider } from './contexts/AnalysisContext';
import { Toaster } from 'react-hot-toast';

// Router wrapper with validation
const ValidatedRouter = ({ children }) => {
  useEffect(() => {
    // Register and track this router instance
    return trackRouterMount('index.js');
  }, []);
  
  return children;
};

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <BrowserRouter>
      <ValidatedRouter>
        <AnalysisProvider>
          <App />
          <Toaster position="top-right" />
        </AnalysisProvider>
      </ValidatedRouter>
    </BrowserRouter>
  </React.StrictMode>
); 