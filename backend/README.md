# Fake News Detection - Backend

The backend API server for the Fake News Detection system built with FastAPI.

## Structure

```
backend/
├── app/                # Core application modules
├── models/             # Machine learning models
├── utils/              # Utility functions
│   ├── text_processor.py         # Basic text processing utilities
│   ├── advanced_text_processor.py # Advanced text analysis features
│   └── explainers.py             # Model explanation utilities
├── tests/              # Test files
├── history/            # Analysis history storage
├── reports/            # Generated reports
├── fixed_backend.py    # Main FastAPI application
├── enhanced_predict.py # Enhanced prediction module
├── requirements.txt    # Python dependencies
└── app_new.py          # New application version with enhanced features
```

## Features

### Core Features

- Fake news detection with machine learning
- Text preprocessing and feature extraction
- Model explainability with LIME and SHAP
- REST API for frontend integration
- Analysis history tracking

### Enhanced Text Processing

1. **Language Detection**
   - Automatic identification of text language
   - Confidence scoring for detection

2. **Entity Extraction**
   - Identification of named entities (people, organizations, locations)
   - Entity counting and categorization

3. **Readability Metrics**
   - Flesch Reading Ease score
   - Grade level assessment
   - Multiple readability indices

4. **Text Uniqueness Analysis**
   - Lexical diversity measurement
   - Content density analysis

5. **Propaganda Technique Detection**
   - Identification of common propaganda techniques
   - Overall propaganda scoring

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information |
| `/health` | GET | Health check |
| `/analyze` | POST | Basic fake news analysis |
| `/analyze/enhanced` | POST | Enhanced analysis with additional features |
| `/explain/methods` | GET | List available explanation methods |
| `/explain` | POST | Generate explanation for prediction |
| `/history` | GET | Retrieve analysis history |
| `/history/{item_id}` | GET | Get specific history item |
| `/detect-language` | POST | Detect language of provided text |
| `/analyze/comprehensive` | POST | Comprehensive text analysis |

## Setup Instructions

1. Create a virtual environment (recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the server:
   ```
   python -m uvicorn fixed_backend:app --reload --host 0.0.0.0 --port 8000
   ```

   Or use:
   ```
   python -m uvicorn app_new:app --reload --host 0.0.0.0 --port 8000
   ```

The API will be available at [http://localhost:8000](http://localhost:8000).

## API Documentation

API documentation is automatically generated and available at:

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Testing

To run tests for the enhanced features:

```
python test_enhanced_processing.py
```

## Environment Variables

The following environment variables can be configured:

- `DEBUG_MODE`: Enable debug mode (default: False)
- `MODEL_PATH`: Path to the trained model file
- `LOG_LEVEL`: Logging level (default: "INFO")

## Development Notes

- The backend uses FastAPI for high performance
- CORS is enabled for frontend integration
- The server automatically creates required directories on startup
- Model files are expected in the `models/` directory

## Troubleshooting

1. If the server fails to start:
   - Check that dependencies are installed correctly
   - Ensure required model files are in place
   - Verify port 8000 is not in use by another application

2. If API requests fail:
   - Check the server logs for error messages
   - Verify the request format and parameters
   - Ensure CORS settings are properly configured 