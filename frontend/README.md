# Fake News Detection Frontend

This React frontend application provides a user interface for the fake news detection system, including visualizations for model explanations using LIME and SHAP.

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