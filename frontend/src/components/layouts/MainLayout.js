import React, { useState } from 'react';
import { Outlet, NavLink, Link } from 'react-router-dom';
import { Bars3Icon, XMarkIcon } from '@heroicons/react/24/outline';

const navigation = [
  { name: 'Home', to: '/' },
  { name: 'Analyzer', to: '/analyzer' },
  { name: 'History', to: '/history' },
  { name: 'Reports', to: '/reports' },
  { name: 'About', to: '/about' },
];

function MainLayout() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <div className="flex flex-col min-h-screen">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <nav className="mx-auto flex max-w-7xl items-center justify-between gap-x-6 p-4 lg:px-8" aria-label="Global">
          <div className="flex lg:flex-1">
            <Link to="/" className="-m-1.5 p-1.5 flex items-center">
              <span className="text-primary-600 font-bold text-2xl mr-2">✓</span>
              <span className="font-display font-bold text-xl text-gray-900">FakeNewsDetector</span>
            </Link>
          </div>
          <div className="hidden lg:flex lg:gap-x-8">
            {navigation.map((item) => (
              <NavLink
                key={item.name}
                to={item.to}
                className={({ isActive }) => 
                  isActive 
                    ? 'text-primary-600 font-semibold' 
                    : 'text-gray-700 hover:text-primary-600'
                }
              >
                {item.name}
              </NavLink>
            ))}
          </div>
          <div className="flex flex-1 items-center justify-end gap-x-6">
            <button
              type="button"
              className="btn btn-primary"
              onClick={() => window.location.href = '/analyzer'}
            >
              Analyze Text
            </button>
          </div>
          <div className="flex lg:hidden">
            <button
              type="button"
              className="-m-2.5 inline-flex items-center justify-center rounded-md p-2.5 text-gray-700"
              onClick={() => setMobileMenuOpen(true)}
            >
              <span className="sr-only">Open main menu</span>
              <Bars3Icon className="h-6 w-6" aria-hidden="true" />
            </button>
          </div>
        </nav>
        
        {/* Mobile menu */}
        {mobileMenuOpen && (
          <div className="lg:hidden" role="dialog" aria-modal="true">
            <div className="fixed inset-0 z-10 bg-black bg-opacity-25"></div>
            <div className="fixed inset-y-0 right-0 z-10 w-full overflow-y-auto bg-white px-6 py-6 sm:max-w-sm sm:ring-1 sm:ring-gray-900/10">
              <div className="flex items-center justify-between">
                <Link to="/" className="-m-1.5 p-1.5 flex items-center" onClick={() => setMobileMenuOpen(false)}>
                  <span className="text-primary-600 font-bold text-2xl mr-2">✓</span>
                  <span className="font-display font-bold text-xl text-gray-900">FakeNewsDetector</span>
                </Link>
                <button
                  type="button"
                  className="-m-2.5 rounded-md p-2.5 text-gray-700"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  <span className="sr-only">Close menu</span>
                  <XMarkIcon className="h-6 w-6" aria-hidden="true" />
                </button>
              </div>
              <div className="mt-6 flow-root">
                <div className="-my-6 divide-y divide-gray-500/10">
                  <div className="space-y-2 py-6">
                    {navigation.map((item) => (
                      <NavLink
                        key={item.name}
                        to={item.to}
                        className={({ isActive }) => 
                          `-mx-3 block rounded-lg px-3 py-2 text-base font-semibold leading-7 ${
                            isActive 
                              ? 'bg-gray-50 text-primary-600' 
                              : 'text-gray-900 hover:bg-gray-50'
                          }`
                        }
                        onClick={() => setMobileMenuOpen(false)}
                      >
                        {item.name}
                      </NavLink>
                    ))}
                  </div>
                  <div className="py-6">
                    <Link
                      to="/analyzer"
                      className="btn btn-primary w-full justify-center"
                      onClick={() => setMobileMenuOpen(false)}
                    >
                      Analyze Text
                    </Link>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </header>

      {/* Main content */}
      <main className="flex-grow">
        <Outlet />
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 text-white py-6">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="mb-4 md:mb-0">
              <p className="text-lg font-semibold mb-2">Fake News Detector</p>
              <p className="text-gray-300 text-sm">
                An AI-powered tool to detect fake news and misinformation
              </p>
            </div>
            <div>
              <ul className="flex flex-wrap gap-4 justify-center">
                {navigation.map((item) => (
                  <li key={item.name}>
                    <NavLink 
                      to={item.to}
                      className="text-gray-300 hover:text-white text-sm"
                    >
                      {item.name}
                    </NavLink>
                  </li>
                ))}
              </ul>
            </div>
          </div>
          <div className="mt-8 pt-4 border-t border-gray-700 text-center text-gray-400 text-sm">
            <p>&copy; {new Date().getFullYear()} Fake News Detector. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default MainLayout; 