function About() {
  return (
    <div className="container">
      <h1 className="text-3xl font-bold mb-6">About Fake News Detector</h1>
      
      <div className="card mb-8">
        <h2 className="text-2xl font-bold mb-4">How It Works</h2>
        <p className="mb-4">
          Our fake news detection system uses machine learning to analyze news content and determine 
          if it's likely to be real or fake news. The system has been trained on thousands of labeled news articles 
          to identify patterns and linguistic features commonly associated with misinformation.
        </p>
        <p className="mb-4">
          When you submit text for analysis, our system processes the content through a pre-trained 
          machine learning model that examines various aspects of the text, including:
        </p>
        <ul className="list-disc pl-6 mb-4">
          <li className="mb-2">Language patterns and style</li>
          <li className="mb-2">Emotional tone and sensationalism</li>
          <li className="mb-2">Word choice and syntax</li>
          <li className="mb-2">Structural elements of the content</li>
        </ul>
        <p>
          The model then provides a prediction ("REAL" or "FAKE") along with a confidence score 
          indicating how certain the model is about its classification.
        </p>
      </div>
      
      <div className="card mb-8">
        <h2 className="text-2xl font-bold mb-4">Technology Stack</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 className="text-xl font-semibold mb-2">Frontend</h3>
            <ul className="list-disc pl-6">
              <li>React.js - UI library</li>
              <li>Tailwind CSS - Styling</li>
              <li>Axios - API requests</li>
              <li>React Router - Navigation</li>
            </ul>
          </div>
          <div>
            <h3 className="text-xl font-semibold mb-2">Backend</h3>
            <ul className="list-disc pl-6">
              <li>Python - Backend language</li>
              <li>Flask - Web framework</li>
              <li>Scikit-learn - Machine learning</li>
              <li>NLTK - Natural language processing</li>
            </ul>
          </div>
        </div>
      </div>
      
      <div className="card">
        <h2 className="text-2xl font-bold mb-4">Limitations</h2>
        <p className="mb-4">
          While our system is designed to be accurate, it's important to understand its limitations:
        </p>
        <ul className="list-disc pl-6">
          <li className="mb-2">
            <span className="font-semibold">Not Perfect:</span> No AI system can be 100% accurate in detecting fake news. 
            Always use your critical thinking skills.
          </li>
          <li className="mb-2">
            <span className="font-semibold">Training Data:</span> The system is only as good as the data it was trained on. 
            New types of misinformation may not be recognized.
          </li>
          <li className="mb-2">
            <span className="font-semibold">Context Matters:</span> The system may miss contextual nuances or 
            satire that would be obvious to human readers.
          </li>
          <li className="mb-2">
            <span className="font-semibold">Evolving Landscape:</span> The characteristics of fake news change over time, 
            which may affect the system's accuracy.
          </li>
        </ul>
      </div>
    </div>
  )
}

export default About 