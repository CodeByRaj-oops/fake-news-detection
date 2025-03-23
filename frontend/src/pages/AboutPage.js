import React from 'react';
import { Link } from 'react-router-dom';
import { 
  InformationCircleIcon, 
  ShieldCheckIcon, 
  CodeBracketIcon, 
  AcademicCapIcon,
  BookOpenIcon
} from '@heroicons/react/24/outline';

function AboutPage() {
  // Team members data removed

  return (
    <div className="max-w-5xl mx-auto px-4 py-8 space-y-16">
      {/* About section */}
      <div>
        <div className="text-center mb-12">
          <InformationCircleIcon className="h-12 w-12 text-indigo-600 mx-auto" />
          <h1 className="mt-2 text-3xl font-extrabold text-gray-900 sm:text-4xl">
            About Our Fake News Detection System
          </h1>
          <p className="mt-3 max-w-2xl mx-auto text-xl text-gray-500 sm:mt-4">
            Learn about our mission and technology behind the platform.
          </p>
        </div>

        <div className="prose prose-indigo prose-lg text-gray-500 mx-auto">
          <p>
            The spread of misinformation has become one of the most significant challenges in today's digital landscape. 
            Our platform was created to address this issue by combining cutting-edge artificial intelligence with journalistic 
            principles to help readers identify potentially misleading content.
          </p>
          <p>
            What began as a research project at a leading university has now evolved into a comprehensive tool that 
            analyzes news articles, social media posts, and other text content for indicators of fake news. Our system 
            doesn't just label content as "real" or "fake" - it provides detailed analysis that helps users understand 
            why certain content might be misleading.
          </p>
          <p>
            We believe that promoting media literacy and critical thinking is essential for a well-informed society. 
            By providing this tool for free, we aim to contribute to a healthier information ecosystem where facts 
            and reliable reporting are valued over sensationalism and misinformation.
          </p>
        </div>
      </div>

      {/* Our technology section */}
      <div>
        <div className="text-center mb-8">
          <h2 className="text-2xl font-bold text-gray-900">Our Technology</h2>
          <p className="mt-4 max-w-2xl mx-auto text-lg text-gray-500">
            How our system detects misinformation and fake news.
          </p>
        </div>

        <div className="mt-10">
          <div className="grid grid-cols-1 gap-10 sm:grid-cols-2 lg:grid-cols-3">
            <div className="bg-white shadow overflow-hidden rounded-lg">
              <div className="px-4 py-5 sm:p-6">
                <div className="flex items-center">
                  <ShieldCheckIcon className="h-8 w-8 text-indigo-600" />
                  <h3 className="ml-3 text-lg font-medium text-gray-900">Advanced ML Models</h3>
                </div>
                <div className="mt-4 text-base text-gray-500">
                  <p>
                    Our detection system utilizes ensemble machine learning models trained on verified datasets 
                    of real and fake news articles from various sources.
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-white shadow overflow-hidden rounded-lg">
              <div className="px-4 py-5 sm:p-6">
                <div className="flex items-center">
                  <CodeBracketIcon className="h-8 w-8 text-indigo-600" />
                  <h3 className="ml-3 text-lg font-medium text-gray-900">Natural Language Processing</h3>
                </div>
                <div className="mt-4 text-base text-gray-500">
                  <p>
                    We analyze linguistic patterns, writing style, emotional content, and factual consistency 
                    to identify potential indicators of misinformation.
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-white shadow overflow-hidden rounded-lg">
              <div className="px-4 py-5 sm:p-6">
                <div className="flex items-center">
                  <AcademicCapIcon className="h-8 w-8 text-indigo-600" />
                  <h3 className="ml-3 text-lg font-medium text-gray-900">Research-Backed Approach</h3>
                </div>
                <div className="mt-4 text-base text-gray-500">
                  <p>
                    Our algorithms are developed based on peer-reviewed research in misinformation detection 
                    and are continuously updated as new patterns emerge.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Our team section removed */}

      {/* FAQs section */}
      <div>
        <div className="text-center mb-8">
          <BookOpenIcon className="h-12 w-12 text-indigo-600 mx-auto" />
          <h2 className="mt-2 text-2xl font-bold text-gray-900">Frequently Asked Questions</h2>
        </div>

        <div className="mt-6 border-t border-gray-200 divide-y divide-gray-200">
          <div className="py-6">
            <h3 className="text-lg font-medium text-gray-900">How accurate is your fake news detection?</h3>
            <div className="mt-3 text-base text-gray-500">
              <p>
                Our system achieves approximately 95% accuracy on benchmark datasets. However, detecting misinformation 
                is a complex challenge, and we encourage users to exercise their own judgment alongside our analysis results.
              </p>
            </div>
          </div>

          <div className="py-6">
            <h3 className="text-lg font-medium text-gray-900">How do you protect user privacy?</h3>
            <div className="mt-3 text-base text-gray-500">
              <p>
                We do not store the text content you submit for analysis beyond what's needed to provide the service. 
                All analysis happens on our secure servers, and we don't share user data with third parties.
              </p>
            </div>
          </div>

          <div className="py-6">
            <h3 className="text-lg font-medium text-gray-900">Can I use this tool in my organization or classroom?</h3>
            <div className="mt-3 text-base text-gray-500">
              <p>
                Yes! We offer special plans for educational institutions and organizations that want to promote media 
                literacy. Contact us for more information about bulk usage and educational resources.
              </p>
            </div>
          </div>

          <div className="py-6">
            <h3 className="text-lg font-medium text-gray-900">How often do you update your detection models?</h3>
            <div className="mt-3 text-base text-gray-500">
              <p>
                We continuously train and improve our models with new data. Major updates are deployed quarterly, 
                while minor improvements happen more frequently to keep up with evolving misinformation tactics.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* CTA section */}
      <div className="bg-indigo-700 rounded-lg">
        <div className="max-w-2xl mx-auto text-center py-16 px-4 sm:py-20 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-extrabold text-white sm:text-4xl">
            <span className="block">Ready to try it yourself?</span>
          </h2>
          <p className="mt-4 text-lg leading-6 text-indigo-200">
            Put our technology to the test with your own content.
          </p>
          <Link
            to="/analyzer"
            className="mt-8 w-full inline-flex items-center justify-center px-5 py-3 border border-transparent text-base font-medium rounded-md text-indigo-600 bg-white hover:bg-indigo-50 sm:w-auto"
          >
            Try the Analyzer
          </Link>
        </div>
      </div>
    </div>
  );
}

export default AboutPage; 