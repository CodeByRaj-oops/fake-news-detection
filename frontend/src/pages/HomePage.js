import React from 'react';
import { Link } from 'react-router-dom';
import { 
  NewspaperIcon, 
  MagnifyingGlassCircleIcon, 
  ChartBarIcon, 
  ShieldCheckIcon,
  LightBulbIcon,
  DocumentTextIcon
} from '@heroicons/react/24/outline';

function HomePage() {
  // Features data for the feature grid
  const features = [
    {
      name: 'Advanced Analysis Engine',
      description: 'Powered by state-of-the-art machine learning models trained on vast datasets of real and fake news.',
      icon: LightBulbIcon,
    },
    {
      name: 'Real-time Detection',
      description: 'Analyze news articles, social media posts, or any text content in seconds to determine authenticity.',
      icon: MagnifyingGlassCircleIcon,
    },
    {
      name: 'Detailed Insights',
      description: 'Get comprehensive reports with confidence scores, sentiment analysis, and specific misinformation indicators.',
      icon: ChartBarIcon,
    },
    {
      name: 'Save & Track Results',
      description: 'Build a personal library of analyzed content and track patterns over time with saved reports.',
      icon: DocumentTextIcon,
    },
  ];

  // How it works steps
  const steps = [
    {
      number: '01',
      title: 'Input Content',
      description: 'Paste any news article, social media post, or suspicious text content into our analyzer.',
    },
    {
      number: '02',
      title: 'Advanced Analysis',
      description: 'Our AI model examines multiple factors like writing style, emotional manipulation, and factual consistency.',
    },
    {
      number: '03',
      title: 'Get Results',
      description: 'Receive a comprehensive analysis with classification, confidence score, and detailed explanation.',
    },
  ];

  return (
    <div className="space-y-16 py-8">
      {/* Hero section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <h1 className="text-4xl font-extrabold tracking-tight text-gray-900 sm:text-5xl md:text-6xl">
            <span className="block">Detect Fake News with</span>
            <span className="block text-indigo-600">Advanced AI Technology</span>
          </h1>
          <p className="mt-3 max-w-md mx-auto text-base text-gray-500 sm:text-lg md:mt-5 md:text-xl md:max-w-3xl">
            Our cutting-edge machine learning system helps you identify misinformation and verify news authenticity with high accuracy.
          </p>
          <div className="mt-10 max-w-md mx-auto sm:flex sm:justify-center md:mt-8">
            <div className="rounded-md shadow">
              <Link to="/analyzer" className="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 md:py-4 md:text-lg md:px-10">
                Try It Now
              </Link>
            </div>
            <div className="mt-3 rounded-md shadow sm:mt-0 sm:ml-3">
              <Link to="/about" className="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-indigo-600 bg-white hover:bg-gray-50 md:py-4 md:text-lg md:px-10">
                Learn More
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Stats section */}
      <div className="bg-indigo-800 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 gap-y-8 gap-x-6 sm:grid-cols-2 lg:grid-cols-3">
            <div className="text-center">
              <p className="text-5xl font-extrabold text-white">95%</p>
              <p className="mt-2 text-xl font-medium text-indigo-100">Detection Accuracy</p>
            </div>
            <div className="text-center">
              <p className="text-5xl font-extrabold text-white">3M+</p>
              <p className="mt-2 text-xl font-medium text-indigo-100">Articles Analyzed</p>
            </div>
            <div className="text-center sm:col-span-2 lg:col-span-1">
              <p className="text-5xl font-extrabold text-white">&lt;5s</p>
              <p className="mt-2 text-xl font-medium text-indigo-100">Average Analysis Time</p>
            </div>
          </div>
        </div>
      </div>

      {/* Features section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <h2 className="text-base font-semibold text-indigo-600 tracking-wide uppercase">Features</h2>
          <p className="mt-2 text-3xl font-extrabold text-gray-900 sm:text-4xl">
            Powerful Tools to Combat Misinformation
          </p>
          <p className="mt-4 max-w-2xl text-xl text-gray-500 mx-auto">
            Our platform offers comprehensive tools to help you identify and understand misinformation in digital content.
          </p>
        </div>

        <div className="mt-12">
          <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-2">
            {features.map((feature) => (
              <div key={feature.name} className="pt-6">
                <div className="flow-root bg-gray-50 rounded-lg px-6 pb-8">
                  <div className="-mt-6">
                    <div>
                      <span className="inline-flex items-center justify-center p-3 bg-indigo-500 rounded-md shadow-lg">
                        <feature.icon className="h-6 w-6 text-white" aria-hidden="true" />
                      </span>
                    </div>
                    <h3 className="mt-8 text-lg font-medium text-gray-900 tracking-tight">{feature.name}</h3>
                    <p className="mt-5 text-base text-gray-500">{feature.description}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* How it works section */}
      <div className="bg-gray-50 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h2 className="text-base font-semibold text-indigo-600 tracking-wide uppercase">How It Works</h2>
            <p className="mt-2 text-3xl font-extrabold text-gray-900 sm:text-4xl">
              Simple Process, Powerful Results
            </p>
          </div>

          <div className="mt-12">
            <div className="grid grid-cols-1 gap-8 md:grid-cols-3">
              {steps.map((step) => (
                <div key={step.number} className="bg-white overflow-hidden shadow rounded-lg">
                  <div className="px-4 py-5 sm:p-6">
                    <div className="flex items-center">
                      <div className="flex-shrink-0 bg-indigo-500 rounded-md p-3">
                        <span className="text-xl font-bold text-white">{step.number}</span>
                      </div>
                      <h3 className="ml-3 text-lg font-medium text-gray-900">{step.title}</h3>
                    </div>
                    <p className="mt-4 text-gray-500">{step.description}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* CTA section */}
      <div className="bg-indigo-700">
        <div className="max-w-2xl mx-auto text-center py-16 px-4 sm:py-20 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-extrabold text-white sm:text-4xl">
            <span className="block">Ready to detect fake news?</span>
            <span className="block">Start using our tool today.</span>
          </h2>
          <p className="mt-4 text-lg leading-6 text-indigo-200">
            Protect yourself and others from misinformation. Our advanced AI helps you make informed decisions about the content you consume.
          </p>
          <Link
            to="/analyzer"
            className="mt-8 w-full inline-flex items-center justify-center px-5 py-3 border border-transparent text-base font-medium rounded-md text-indigo-600 bg-white hover:bg-indigo-50 sm:w-auto"
          >
            <NewspaperIcon className="h-5 w-5 mr-2" />
            Analyze Content Now
          </Link>
        </div>
      </div>

      {/* Trust indicators */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <h2 className="text-base font-semibold text-indigo-600 tracking-wide uppercase">Why Trust Us</h2>
          <p className="mt-2 text-3xl font-extrabold text-gray-900 sm:text-4xl">
            Built on Science and Transparency
          </p>
        </div>

        <div className="mt-12 bg-white shadow overflow-hidden rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
              <div className="flex">
                <div className="flex-shrink-0">
                  <ShieldCheckIcon className="h-6 w-6 text-indigo-600" />
                </div>
                <div className="ml-3">
                  <h3 className="text-lg font-medium text-gray-900">Research-Backed Models</h3>
                  <p className="mt-2 text-base text-gray-500">
                    Our algorithms are developed based on peer-reviewed research in natural language processing and misinformation detection.
                  </p>
                </div>
              </div>
              <div className="flex">
                <div className="flex-shrink-0">
                  <ChartBarIcon className="h-6 w-6 text-indigo-600" />
                </div>
                <div className="ml-3">
                  <h3 className="text-lg font-medium text-gray-900">Continuous Improvement</h3>
                  <p className="mt-2 text-base text-gray-500">
                    We regularly update our models with new data and techniques to keep up with evolving misinformation tactics.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default HomePage; 