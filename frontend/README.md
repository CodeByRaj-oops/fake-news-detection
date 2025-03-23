# Fake News Detection - Frontend

The frontend application for the Fake News Detection system built with React.

## Structure

```
frontend/
├── public/               # Static assets
├── src/                  # Source code
│   ├── components/       # Reusable React components
│   │   ├── layouts/      # Layout components
│   │   └── ...           # Other components
│   ├── api/              # API integration functions
│   ├── context/          # React context providers
│   ├── pages/            # Page components
│   ├── utils/            # Utility functions
│   ├── assets/           # Images, fonts, etc.
│   ├── App.js            # Main application component
│   ├── index.js          # Application entry point
│   └── config.js         # Application configuration
├── package.json          # Dependencies and scripts
└── vite.config.js        # Vite configuration
```

## Features

- User-friendly interface for fake news detection
- Text input form with analysis options
- Detailed analysis results with visualizations
- Enhanced analysis capabilities
- API connection status monitoring
- Responsive design for mobile and desktop

## Configuration

The frontend communicates with the backend API. You can configure the API URL and endpoints in `src/config.js`:

```javascript
// Configuration for the frontend application
const config = {
  // Backend API URL
  apiUrl: 'http://localhost:8000',
  
  // API endpoints
  endpoints: {
    analyze: '/analyze',
    enhancedAnalyze: '/analyze/enhanced',
    history: '/history',
    health: '/health',
    explain: '/explain'
  },
  
  // Default request timeout in milliseconds
  timeout: 30000
};

export default config;
```

## Available Scripts

In the project directory, you can run:

### `npm install`

Installs the dependencies required for the application.

### `npm start`

Runs the app in development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.\
You will also see any lint errors in the console.

### `npm run build`

Builds the app for production to the `dist` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

## Dependencies

Major dependencies include:

- **React**: UI library
- **Axios**: HTTP client for API requests
- **React Router**: Navigation and routing
- **Tailwind CSS**: Utility-first CSS framework for styling

## Development Notes

- Ensure the backend server is running before starting the frontend
- The application uses environment variables for configuration
- Component styling uses CSS modules to avoid style conflicts

## Troubleshooting

If you encounter API connection issues:

1. Check if the backend server is running
2. Verify the API URL in `src/config.js`
3. Look for CORS issues in browser developer tools
4. Ensure the correct API endpoints are being used

## Model Explainability Features

The frontend now includes components to visualize model explanations:

### ModelExplanationPanel Component

Located at `src/components/ModelExplanationPanel.js`, this component provides:

- Tabbed interface to toggle between LIME and SHAP explanations
- Visualization of feature importance with positive/negative contributions
- Highlighting of important words in the original text
- Visual explanations of how each explanation method works

### TextAnalysisForm Updates

The `TextAnalysisForm` component has been extended with:

- Option to include model explanations in analysis
- Dropdown to select explanation method (LIME, SHAP, or both)
- Tooltip explaining what model explanations provide

### AnalysisResult Updates

The `AnalysisResult` component now displays the `ModelExplanationPanel` when explanation data is available.

## How Explanations Work

### LIME Explanations

LIME (Local Interpretable Model-agnostic Explanations) shows which words contribute positively or negatively to the model's prediction. Words in green push the prediction toward "Real News," while words in red push toward "Fake News."

### SHAP Explanations

SHAP (SHapley Additive exPlanations) uses game theory to explain how each word contributes to the prediction relative to a baseline value. It provides a different perspective on word importance than LIME.

## Integration with Backend

The frontend integrates with the backend explainability API endpoints:

- `POST /analyze` with `explain=true` to get analysis with explanations
- `POST /explain` for direct explanations of text
- `GET /explain/methods` to retrieve available explanation methods

## Running the Application

1. Install dependencies:
```
npm install
```

2. Start the development server:
```
npm start
```

3. Make sure the backend server is running to enable model explanations.

## Best Practices for Explainability

- Include explanations for critical decisions or when high confidence is needed
- Compare LIME and SHAP explanations for more robust understanding
- Use the detailed view to see exact contribution values for important words 