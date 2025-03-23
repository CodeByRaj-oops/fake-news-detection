# Fake News Detection with Enhanced Text Processing

## Overview

This application provides a comprehensive fake news detection system with enhanced text processing capabilities. The system analyzes news articles and determines their credibility using machine learning and advanced linguistic analysis.

## New Enhanced Features

The system now includes enhanced text processing capabilities:

### 1. Language Detection
- Automatically identifies the language of input text
- Supports multiple languages with confidence scores
- Prevents analysis of unsupported languages

### 2. Entity Extraction
- Identifies named entities (people, organizations, locations, etc.)
- Provides entity counts by type
- Useful for analyzing source credibility

### 3. Readability Metrics
- Calculates multiple standardized readability scores
- Includes Flesch Reading Ease, Gunning Fog Index, and more
- Identifies content with suspiciously simple or complex language

### 4. Text Uniqueness Analysis
- Measures lexical diversity and uniqueness
- Generates content hash for duplicate detection
- Identifies machine-generated or repetitive content

### 5. Propaganda Technique Detection
- Identifies common propaganda techniques
- Calculates overall propaganda score
- Highlights specific techniques used in the text

## Directory Structure

- `/backend`: API server and machine learning models
  - `/utils`: Text processing utilities
    - `advanced_text_processor.py`: Enhanced text processing features
    - `improved_text_processor.py`: Base text processing
  - `enhanced_predict.py`: Enhanced prediction module
  - `app_new.py`: API with enhanced endpoints
  
- `/frontend`: React frontend application

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
```
cd backend
```

2. Install required dependencies:
```
pip install -r requirements.txt
```

3. Run the backend server:
```
python app_new.py
```

The API server will start on http://localhost:8000.

### Frontend Setup

1. Navigate to the frontend directory:
```
cd frontend
```

2. Install dependencies:
```
npm install
```

3. Start the development server:
```
npm run dev
```

The frontend will be available at http://localhost:3000.

## Testing Enhanced Features

To test the enhanced text processing features:

```
cd backend
python test_enhanced_processing.py
```

This script demonstrates all the new enhanced text processing capabilities with sample texts.

## API Documentation

API documentation is available at:
- http://localhost:8000/docs (Swagger UI)
- http://localhost:8000/redoc (ReDoc)

## Enhanced API Endpoints

- `POST /analyze/enhanced`: Full analysis with enhanced features
- `POST /detect-language`: Language detection
- `POST /analyze/comprehensive`: Comprehensive text analysis

## Detailed Documentation

For more detailed information about the enhanced features, refer to:
- [Enhanced Features Documentation](backend/ENHANCED-FEATURES.md)
- [Backend README](backend/README.md) 