#!/usr/bin/env python3
"""
Enhanced prediction module for fake news detection with comprehensive analysis.
This extends the improved_predict.py with additional features from advanced_text_processor.
"""

import os
import sys
import re
import pandas as pd
import numpy as np
import joblib
import logging
import json
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.pipeline import Pipeline

# Add parent directory to path to allow imports
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)

# Import text processing utilities
from utils.advanced_text_processor import (
    preprocess_text,
    extract_features,
    analyze_writing_style,
    get_ngram_frequencies,
    detect_language,
    extract_entities,
    calculate_readability_metrics,
    calculate_text_uniqueness,
    detect_propaganda_techniques,
    comprehensive_text_analysis
)

# Import explainer utilities
try:
    from utils.explainers import (
        ModelExplainer,
        explain_with_lime,
        explain_with_shap,
        get_combined_explanation
    )
    EXPLAINERS_AVAILABLE = True
except ImportError:
    # If explainers aren't available, we'll still function but without explanations
    EXPLAINERS_AVAILABLE = False
    logging.warning("Explainer modules (LIME/SHAP) not available. Install with: pip install lime shap")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize paths
MODELS_DIR = os.path.join(script_dir, 'models')
REPORTS_DIR = os.path.join(script_dir, 'reports')
os.makedirs(REPORTS_DIR, exist_ok=True)

class EnhancedFakeNewsDetector:
    """
    Enhanced fake news detection with comprehensive analysis, language detection,
    entity recognition, and more detailed text analysis.
    """
    
    def __init__(self, model_path=None):
        """
        Initialize the detector with a trained model.
        
        Args:
            model_path (str): Path to the trained model file
        """
        if model_path is None:
            # Use default model path
            model_path = os.path.join(MODELS_DIR, 'improved_fake_news_model.pkl')
        
        try:
            logger.info(f"Loading model from {model_path}")
            self.model = joblib.load(model_path)
            logger.info("Model loaded successfully")
            
            # Initialize explainer if available
            self.explainer = None
            if EXPLAINERS_AVAILABLE:
                self.explainer = ModelExplainer(self.model)
                logger.info("Model explainer initialized")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            self.model = None
            self.explainer = None
            
    def predict(self, text, detailed=False, explain=False, explanation_method="lime", num_features=10, comprehensive=False):
        """
        Predict whether a text is fake or real news with enhanced analysis.
        
        Args:
            text (str): Input text
            detailed (bool): Whether to return detailed analysis
            explain (bool): Whether to return model explanations
            explanation_method (str): Method for explanations ('lime', 'shap', or 'both')
            num_features (int): Number of features to include in explanations
            comprehensive (bool): Whether to perform comprehensive analysis
            
        Returns:
            dict: Prediction results
        """
        if not text or not isinstance(text, str):
            return {
                'error': 'Invalid input text',
                'prediction': 'Unknown',
                'confidence': 0.0,
                'timestamp': datetime.now().isoformat()
            }
        
        if self.model is None:
            return {
                'error': 'Model not loaded',
                'prediction': 'Unknown',
                'confidence': 0.0,
                'timestamp': datetime.now().isoformat()
            }
        
        try:
            # Detect language
            language_info = detect_language(text)
            
            # Only proceed with analysis if the text is in English
            # This prevents incorrect analysis of non-English content
            if language_info['language_code'] != 'en' and language_info['confidence'] > 0.8:
                return {
                    'error': f"Non-English text detected ({language_info['language_name']}). Current model only supports English.",
                    'prediction': 'Unsupported Language',
                    'confidence': 0.0,
                    'language': language_info,
                    'timestamp': datetime.now().isoformat()
                }
            
            # Preprocess the text
            processed_text = preprocess_text(text)
            
            # Make prediction
            label_probabilities = self.model.predict_proba([processed_text])[0]
            prediction_idx = np.argmax(label_probabilities)
            confidence = label_probabilities[prediction_idx]
            
            # Convert prediction index to label
            labels = self.model.classes_
            prediction = labels[prediction_idx]
            
            # Prepare base result
            result = {
                'prediction': prediction,
                'confidence': float(confidence),
                'language': language_info,
                'timestamp': datetime.now().isoformat()
            }
            
            # Add comprehensive analysis if requested
            if comprehensive:
                # Use the comprehensive analysis function that includes all features
                analysis_result = comprehensive_text_analysis(text)
                result['comprehensive_analysis'] = analysis_result
                
                # Add credibility score
                result['credibility_score'] = self._calculate_enhanced_credibility_score(
                    analysis_result, 
                    confidence
                )
                
            # Add detailed analysis if requested
            elif detailed:
                result.update(self._generate_detailed_analysis(text, processed_text, prediction, confidence))
            
            # Add model explanations if requested
            if explain and EXPLAINERS_AVAILABLE and self.explainer:
                result['model_explanations'] = self._generate_model_explanations(
                    text,
                    method=explanation_method,
                    num_features=num_features
                )
            
            return result
            
        except Exception as e:
            logger.error(f"Error during prediction: {e}", exc_info=True)
            return {
                'error': str(e),
                'prediction': 'Error',
                'confidence': 0.0,
                'timestamp': datetime.now().isoformat()
            }
    
    def _generate_detailed_analysis(self, raw_text, processed_text, prediction, confidence):
        """
        Generate detailed analysis of the text.
        
        Args:
            raw_text (str): Original raw text
            processed_text (str): Preprocessed text
            prediction (str): Prediction label
            confidence (float): Prediction confidence
            
        Returns:
            dict: Detailed analysis
        """
        # Extract linguistic features
        features = extract_features(raw_text)
        
        # Analyze writing style
        style_analysis = analyze_writing_style(raw_text)
        
        # Extract entities
        entity_info = extract_entities(raw_text)
        
        # Calculate readability metrics
        readability = calculate_readability_metrics(raw_text)
        
        # Text uniqueness
        uniqueness = calculate_text_uniqueness(raw_text)
        
        # Detect propaganda techniques
        propaganda = detect_propaganda_techniques(raw_text)
        
        # Generate explanation
        explanation = self._generate_explanation(
            features, 
            style_analysis, 
            propaganda,
            readability,
            prediction, 
            confidence
        )
        
        # Return detailed analysis
        return {
            'detailed_analysis': {
                'text_features': features,
                'writing_style': style_analysis,
                'entities': entity_info,
                'readability': readability,
                'text_uniqueness': uniqueness,
                'propaganda_analysis': propaganda
            },
            'explanation': explanation,
            'credibility_score': self._calculate_enhanced_credibility_score({
                'basic_features': features,
                'writing_style': style_analysis,
                'readability': readability,
                'uniqueness': uniqueness,
                'propaganda': propaganda,
                'entities': entity_info
            }, confidence)
        }
    
    def _generate_model_explanations(self, text, method="lime", num_features=10):
        """
        Generate model explanations using LIME and/or SHAP.
        
        Args:
            text (str): Input text
            method (str): Explanation method ('lime', 'shap', or 'both')
            num_features (int): Number of features to include
            
        Returns:
            dict: Model explanations
        """
        if not EXPLAINERS_AVAILABLE or not self.explainer:
            return {"error": "Model explanation not available"}
            
        try:
            if method.lower() == "lime":
                return self.explainer.explain_with_lime(text, num_features=num_features)
            elif method.lower() == "shap":
                return self.explainer.explain_with_shap(text, num_features=num_features)
            elif method.lower() == "both":
                return self.explainer.get_combined_explanation(text, num_features=num_features)
            else:
                return {"error": f"Unknown explanation method: {method}"}
        except Exception as e:
            logger.error(f"Error generating model explanation: {e}", exc_info=True)
            return {"error": str(e)}
    
    def _calculate_enhanced_credibility_score(self, analysis_results, model_confidence):
        """
        Calculate an enhanced credibility score based on comprehensive analysis.
        
        Args:
            analysis_results (dict): Results from text analysis
            model_confidence (float): Model prediction confidence
            
        Returns:
            float: Credibility score (0-100)
        """
        # Extract components from analysis results
        if 'basic_features' in analysis_results:
            features = analysis_results['basic_features']
        else:
            features = {}
            
        if 'writing_style' in analysis_results:
            style = analysis_results['writing_style']
        else:
            style = {}
            
        if 'readability' in analysis_results:
            readability = analysis_results['readability']
        else:
            readability = {}
            
        if 'uniqueness' in analysis_results:
            uniqueness = analysis_results['uniqueness']
        else:
            uniqueness = {}
            
        if 'propaganda' in analysis_results:
            propaganda = analysis_results['propaganda']
        else:
            propaganda = {}
        
        # Calculate base credibility score (0-100 scale, higher is more credible)
        base_score = (1 - model_confidence) * 100 if model_confidence <= 0.5 else (1 - model_confidence) * 200
        
        # Adjust for clickbait
        clickbait_penalty = features.get('clickbait_score', 0) * 5
        
        # Adjust for subjectivity
        subjectivity_penalty = features.get('subjectivity', 0) * 10
        
        # Adjust for exaggeration phrases
        exaggeration_penalty = style.get('exaggeration_phrases', 0) * 2
        
        # Adjust for propaganda techniques
        propaganda_penalty = propaganda.get('propaganda_score', 0) * 0.5
        
        # Adjust for readability (extremely high or low readability might be suspicious)
        reading_ease = readability.get('flesch_reading_ease', 50)
        if reading_ease < 30 or reading_ease > 70:
            readability_penalty = min(abs(reading_ease - 50) * 0.2, 10)
        else:
            readability_penalty = 0
            
        # Adjust for text diversity (very high might indicate machine-generated text,
        # very low might indicate simplified propaganda)
        lexical_diversity = uniqueness.get('lexical_diversity', 0.5)
        if lexical_diversity < 0.3 or lexical_diversity > 0.8:
            diversity_penalty = min(abs(lexical_diversity - 0.5) * 20, 10)
        else:
            diversity_penalty = 0
        
        # Calculate final score
        score = base_score - clickbait_penalty - subjectivity_penalty - exaggeration_penalty - propaganda_penalty - readability_penalty - diversity_penalty
        
        # Ensure score is in range 0-100
        score = max(0, min(100, score))
        
        return round(score, 1)
    
    def _generate_explanation(self, features, style_analysis, propaganda, readability, prediction, confidence):
        """
        Generate a human-readable explanation of the analysis.
        
        Args:
            features (dict): Text features
            style_analysis (dict): Writing style analysis
            propaganda (dict): Propaganda analysis
            readability (dict): Readability metrics
            prediction (str): Prediction label
            confidence (float): Prediction confidence
            
        Returns:
            str: Human-readable explanation
        """
        # Start with prediction
        if prediction.lower() == 'fake':
            explanation = f"This text appears to be fake news (confidence: {confidence:.2f}). "
            credibility = "low"
        elif prediction.lower() == 'real':
            explanation = f"This text appears to be real news (confidence: {confidence:.2f}). "
            credibility = "high"
        else:
            explanation = f"The credibility of this text is uncertain (confidence: {confidence:.2f}). "
            credibility = "medium"
        
        # Add details about language features
        clickbait_score = features.get('clickbait_score', 0)
        capitalized_ratio = features.get('capitalized_ratio', 0)
        exclamation_count = features.get('exclamation_count', 0)
        question_count = features.get('question_count', 0)
        
        if clickbait_score > 2:
            explanation += f"It contains {clickbait_score} clickbait phrases, which is characteristic of sensationalized content. "
        
        if capitalized_ratio > 0.1:
            explanation += f"It has an unusually high proportion of CAPITALIZED words ({capitalized_ratio:.2f}), often used for emphasis in misleading content. "
        
        if exclamation_count > 3:
            explanation += f"The text uses {exclamation_count} exclamation marks, which can indicate emotional manipulation. "
        
        # Add details about writing style
        hedging = style_analysis.get('hedging_phrases', 0)
        exaggeration = style_analysis.get('exaggeration_phrases', 0)
        
        if hedging > 2:
            explanation += f"It contains {hedging} hedging phrases (like 'allegedly', 'reportedly'), which can indicate uncertainty. "
        
        if exaggeration > 2:
            explanation += f"It uses {exaggeration} exaggeration phrases, which may indicate overstatement of facts. "
        
        # Add details about propaganda techniques
        propaganda_score = propaganda.get('propaganda_score', 0)
        propaganda_techniques = propaganda.get('techniques', {})
        
        if propaganda_score > 20:
            explanation += f"The text shows strong indicators of propaganda techniques ({propaganda_score:.1f}% score). "
            top_techniques = sorted(propaganda_techniques.items(), key=lambda x: x[1], reverse=True)[:2]
            if top_techniques:
                technique_list = ", ".join([f"{name} ({count})" for name, count in top_techniques])
                explanation += f"Most common techniques: {technique_list}. "
        
        # Add readability assessment
        reading_ease = readability.get('flesch_reading_ease', 50)
        grade_level = readability.get('average_grade_level', 10)
        
        if reading_ease < 30:
            explanation += f"The text is very difficult to read (grade level {grade_level:.1f}), which can obscure critical assessment. "
        elif reading_ease > 70:
            explanation += f"The text is very easy to read (grade level {grade_level:.1f}), which is common in simplified propaganda. "
        
        # Add summary
        if credibility == "low":
            explanation += "Overall, this content displays multiple characteristics commonly associated with fake news and should be treated with skepticism."
        elif credibility == "medium":
            explanation += "This content shows some concerning characteristics and should be verified with trusted sources."
        else:
            explanation += "This content appears to follow journalistic standards, but critical reading is always recommended."
        
        return explanation
        
    def save_report(self, text, prediction_result, filename=None):
        """
        Save analysis report to file.
        
        Args:
            text (str): Original text
            prediction_result (dict): Prediction results
            filename (str): Filename to save report
            
        Returns:
            str: Path to saved report
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"report_{timestamp}.json"
            
        report_path = os.path.join(REPORTS_DIR, filename)
        
        # Create report data
        report_data = {
            'original_text': text,
            'prediction': prediction_result,
            'timestamp': datetime.now().isoformat()
        }
        
        # Save to file
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
            
        return report_path

# Example usage
if __name__ == "__main__":
    # Initialize detector
    detector = EnhancedFakeNewsDetector()
    
    # Sample text
    sample_text = """
    SHOCKING DISCOVERY: Scientists find definitive link between vaccines and autism!
    The government has been HIDING this information from the public for YEARS!
    According to anonymous sources, this conspiracy goes all the way to the top.
    Share this with everyone you know before it gets taken down!!!
    """
    
    # Get prediction with comprehensive analysis
    result = detector.predict(sample_text, comprehensive=True)
    
    # Print result
    print(json.dumps(result, indent=2)) 