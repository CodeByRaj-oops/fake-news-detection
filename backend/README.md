# Fake News Detection Backend

This backend provides a FastAPI server for fake news detection with model explanations using LIME and SHAP.

## Model Explainability

The system now supports model explanations using two interpretability methods:

### LIME (Local Interpretable Model-agnostic Explanations)

LIME works by perturbing the input data and observing how the predictions change. It creates a simpler interpretable model around the instance being explained to understand which features contribute most to the prediction.

Benefits:
- Model-agnostic: Works with any model (SVM, Random Forest, Neural Networks, etc.)
- Intuitive: Shows which words contribute to or against a specific prediction
- Local fidelity: Accurate for explaining individual predictions

### SHAP (SHapley Additive exPlanations)

SHAP uses concepts from game theory to assign each feature an importance value for a particular prediction. It calculates Shapley values which represent the contribution of each feature to the difference between the actual prediction and the average prediction.

Benefits:
- Solid theoretical foundation in game theory
- Consistency: Provides consistent explanations
- Global insights: Can be aggregated to understand overall model behavior

## API Endpoints

### Analysis with Explanations

```
POST /analyze
```

Request body:
```json
{
  "text": "Text to analyze...",
  "detailed": true,
  "save_report": false,
  "explain": true,
  "explanation_method": "lime",  // Options: "lime", "shap", or "both"
  "num_features": 10
}
```

### Direct Explanation Endpoint

```
POST /explain
```

Request body:
```json
{
  "text": "Text to explain...",
  "method": "lime",  // Options: "lime", "shap", or "both"
  "num_features": 10
}
```

### Available Explanation Methods

```
GET /explain/methods
```

Returns available explanation methods and descriptions.

## Setup

1. Install dependencies:
```
pip install -r requirements.txt
```

2. Run the server:
```
uvicorn app_new:app --reload
```

## Integration with Frontend

The frontend calls these endpoints to generate and display explanations for predictions, showing users which words and phrases most influenced the model's decision. 