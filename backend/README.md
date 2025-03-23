# Fake News Detection Backend

This is the backend service for the fake news detection application, featuring enhanced text processing capabilities.

## Features

- Machine learning-based fake news detection
- Detailed text analysis with linguistic feature extraction
- Enhanced text processing with language detection
- Entity extraction and propaganda technique detection
- Model explanations using LIME and SHAP
- Comprehensive text analysis with readability metrics
- API for frontend integration

## Installation

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

### Setup Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-folder>/backend
```

2. Create and activate a virtual environment:
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download required NLTK data:
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('maxent_ne_chunker'); nltk.download('words'); nltk.download('averaged_perceptron_tagger')"
```

## Running the Application

Start the backend server:

```bash
python app_new.py
```

By default, the API will be available at http://localhost:8000.

## API Documentation

Once the server is running, access the API documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing Enhanced Features

To test the enhanced text processing features:

```bash
python test_enhanced_processing.py
```

This will run a series of tests demonstrating language detection, entity extraction, readability metrics, propaganda detection, and the overall enhanced analysis capabilities.

## API Endpoints

### Main Endpoints

- `POST /analyze`: Analyze text with standard features
- `POST /analyze/enhanced`: Analyze text with enhanced features
- `POST /analyze/comprehensive`: Perform comprehensive text analysis
- `POST /detect-language`: Detect the language of text

### History and Reports

- `GET /history`: Get all analysis history
- `GET /history/{id}`: Get specific history item
- `GET /reports`: Get all saved reports
- `GET /reports/{id}`: Get specific report
- `DELETE /history/{id}`: Delete history item
- `DELETE /reports/{id}`: Delete report

### Explanations

- `POST /explain`: Get model explanations for text

## Enhanced Features Documentation

For detailed information about the enhanced text processing features, see [ENHANCED-FEATURES.md](ENHANCED-FEATURES.md).

## Troubleshooting

### Common Issues

1. **Missing NLTK Data**
   
   If you encounter errors related to missing NLTK data, run:
   ```python
   import nltk
   nltk.download('punkt')
   nltk.download('stopwords')
   nltk.download('wordnet')
   nltk.download('maxent_ne_chunker')
   nltk.download('words')
   nltk.download('averaged_perceptron_tagger')
   ```

2. **Model Not Found**
   
   Make sure the models directory exists and contains the required model files. Default model path is `models/improved_fake_news_model.pkl`.

3. **Package Dependencies**
   
   If you encounter package-related errors, try:
   ```bash
   pip install -r requirements.txt --upgrade
   ```

## License

[MIT License](LICENSE) 