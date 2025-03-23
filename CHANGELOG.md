# Changelog

## Version 3.0.0 - Enhanced Text Processing

### New Features
- Added language detection to identify the language of input text
- Implemented entity extraction to identify named entities in text
- Added readability metrics calculation (Flesch Reading Ease, Gunning Fog, etc.)
- Implemented text uniqueness analysis with lexical diversity metrics
- Added propaganda technique detection with scoring
- Created comprehensive text analysis that combines all features

### New API Endpoints
- `/analyze/enhanced`: Enhanced analysis with additional features
- `/detect-language`: Language detection endpoint
- `/analyze/comprehensive`: Comprehensive text analysis endpoint

### New Files
- `utils/advanced_text_processor.py`: Enhanced text processing utilities
- `enhanced_predict.py`: Enhanced prediction module
- `test_enhanced_processing.py`: Test script for enhanced features
- `ENHANCED-FEATURES.md`: Documentation for enhanced features

### Documentation
- Updated README.md with enhanced feature information
- Created detailed documentation for API endpoints
- Added usage examples and test instructions

### Other Improvements
- Improved credibility scoring with more linguistic features
- Enhanced explanation generation with propaganda detection
- Added support for multi-language text identification
- Fixed issues in basic text processor implementation

## Version 2.0.0 - Model Explainability

### Features
- Added model explanations using LIME and SHAP
- Implemented detailed text analysis with linguistic features
- Created API for frontend integration
- Added history and report management

### API Endpoints
- `/analyze`: Main analysis endpoint with explanation options
- `/explain`: Model explanation endpoint
- `/history` and `/reports`: History and report management

## Version 1.0.0 - Initial Release

### Features
- Basic fake news detection using machine learning
- Simple text preprocessing
- API for frontend integration