import React, { useEffect } from 'react';

/**
 * RouterValidator.js
 * Utility to detect and prevent nested router errors in React applications
 */

// Flag to track if Router has been mounted
let isRouterMounted = false;

/**
 * Function to track router mounts
 * Can be called in router components to ensure only one router is active
 */
export function trackRouterMount(componentName = 'Unknown') {
  if (process.env.NODE_ENV === 'development') {
    if (isRouterMounted) {
      console.error(
        `%c[RouterValidator] ERROR: Multiple Router instances detected!`,
        'color: #ff0000; font-weight: bold; font-size: 14px;'
      );
      console.error(
        `%cA Router was already mounted when another Router was mounted in ${componentName}.`,
        'color: #ff0000;'
      );
      console.error(
        `%cFix: Ensure you have exactly ONE <BrowserRouter> or <Router> in your app, typically in index.js.`,
        'color: #ff9800; font-weight: bold;'
      );

      // Throw error in development to prevent nested routers
      throw new Error(
        `Multiple Router instances detected! Remove nested <BrowserRouter> or <Router> components. ` +
        `Check ${componentName} component.`
      );
    } else {
      console.log(
        `%c[RouterValidator] Router mounted successfully in ${componentName}`,
        'color: #4caf50; font-weight: bold;'
      );
      isRouterMounted = true;
    }
  }
  
  return () => {
    if (process.env.NODE_ENV === 'development') {
      console.log(
        `%c[RouterValidator] Router unmounted from ${componentName}`,
        'color: #2196f3; font-weight: bold;'
      );
      isRouterMounted = false;
    }
  };
}

/**
 * Custom BrowserRouter validator wrapper
 * Example usage:
 * import { ValidatedBrowserRouter } from './utils/RouterValidator';
 * 
 * <ValidatedBrowserRouter>
 *   <App />
 * </ValidatedBrowserRouter>
 */
export function ValidatedBrowserRouter({
  children,
  componentName = 'BrowserRouter'
}) {
  useEffect(() => {
    return trackRouterMount(componentName);
  }, [componentName]);

  return children;
}

// Create a properly named default export
const RouterValidator = {
  trackRouterMount,
  ValidatedBrowserRouter
};

export default RouterValidator; 