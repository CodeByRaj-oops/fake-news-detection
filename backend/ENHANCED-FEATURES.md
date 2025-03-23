# Enhanced Text Processing Features

This document outlines the enhanced text processing features added to the fake news detection system.

## Overview

The enhanced text processing capabilities extend the existing system with:

1. **Language Detection**: Identify the language of input text and prevent analysis of unsupported languages
2. **Entity Extraction**: Extract and analyze named entities in the text
3. **Readability Metrics**: Calculate multiple standardized readability scores
4. **Text Uniqueness Analysis**: Measure lexical diversity and uniqueness
5. **Propaganda Technique Detection**: Identify common propaganda techniques
6. **Comprehensive Analysis**: Combine all features into a single analysis

## New API Endpoints

The following new endpoints have been added to the API:

### 1. Enhanced Analysis
```
POST /analyze/enhanced
```
Performs enhanced analysis with all advanced features.

**Request Body:**
```json
{
  "text": "Text to analyze...",
  "detailed": true,
  "comprehensive": true,
  "save_report": false,
  "explain": false,
  "explanation_method": "lime",
  "num_features": 10,
  "detect_language": true
}
```

### 2. Language Detection
```
POST /detect-language
```
Detects the language of the provided text.

**Request Body:**
```json
{
  "text": "Text to analyze language..."
}
```

### 3. Comprehensive Text Analysis
```
POST /analyze/comprehensive
```
Performs comprehensive analysis with all text processing features.

**Request Body:**
```json
{
  "text": "Text to analyze..."
}
```

## Feature Details

### Language Detection

The language detection feature:
- Identifies the language of input text
- Returns language code, language name, and confidence score
- Indicates whether the language is supported by the models
- Prevents incorrect analysis of non-English content

### Entity Extraction

Entity extraction identifies named entities such as:
- PERSON: People's names
- ORGANIZATION: Company and organization names
- LOCATION: Geographic locations
- DATE: Date references
- TIME: Time references
- MONEY: Monetary values
- PERCENT: Percentage values
- GPE: Geopolitical entities

### Readability Metrics

Calculates standard readability metrics including:
- Flesch Reading Ease
- Flesch-Kincaid Grade Level
- Gunning Fog Index
- SMOG Index
- Coleman-Liau Index
- Automated Readability Index

### Text Uniqueness Analysis

Measures text uniqueness through:
- Unique words ratio
- Lexical diversity (type-token ratio)
- Content hash (for duplicate detection)

### Propaganda Technique Detection

Detects common propaganda techniques like:
- Name Calling: Using negative labels to discredit ideas or persons
- Glittering Generalities: Using vague, emotionally appealing words
- Transfer: Projecting positive/negative qualities of a person/entity/value to another
- Testimonial: Using quotes from authorities or celebrities
- Plain Folks: Presenting ideas as common sense from ordinary people
- Card Stacking: Selectively presenting facts to support a conclusion
- Bandwagon: Appealing to popularity or "everyone is doing it"
- Fear: Instilling anxiety or concern
- Black and White Fallacy: Presenting only two choices or polarizing an issue
- Exaggeration: Overstating or magnifying facts

## Implementation Details

The enhanced features are implemented in the following files:

- `utils/advanced_text_processor.py`: Contains all enhanced text processing functions
- `enhanced_predict.py`: Enhanced prediction module using advanced text processing 
- `app_new.py`: Updated API with new endpoints for enhanced features

## Usage Examples

### Basic Enhanced Analysis

```python
from enhanced_predict import EnhancedFakeNewsDetector

detector = EnhancedFakeNewsDetector()
result = detector.predict(text, detailed=True)
print(result['credibility_score'])
```

### Comprehensive Analysis

```python
from utils.advanced_text_processor import comprehensive_text_analysis

result = comprehensive_text_analysis(text)
print(result['language'])
print(result['readability'])
print(result['propaganda'])
```

## Configuration

No additional configuration is needed beyond installing the required dependencies:

```
pip install -r requirements.txt
```

## Limitations

- Language detection is only for identification. Analysis is currently optimized for English content.
- Entity extraction requires sufficient context to be accurate.
- Propaganda detection is based on keyword matching and may require refinement for specific domains. 