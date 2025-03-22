#!/usr/bin/env python3
"""
Improved prediction module for fake news detection with detailed analysis.
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
from utils.improved_text_processor import (
    preprocess_text, 
    extract_features, 
    analyze_writing_style,
    get_ngram_frequencies
)

# Import explainer utilities (new)
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

# Warning phrases commonly found in fake news
MISINFORMATION_INDICATORS = [
    # Clickbait phrases
    "you won't believe", "shocking", "mind blowing", "incredible", "unbelievable",
    
    # Sensationalism
    "shocking truth", "what they don't want you to know", "secret", "conspiracy",
    
    # Generalized claims
    "everyone knows", "studies show", "scientists say", "doctors reveal",
    
    # Urgent language
    "urgent", "breaking", "alert", "warning", "must read", "share now",
    
    # Source credibility issues
    "according to anonymous sources", "insider reveals", "leaked information",
    
    # Extreme language
    "miracle", "cure", "perfect", "revolutionary", "guaranteed", "proven"
]

# Reliability phrases often found in credible news
RELIABILITY_INDICATORS = [
    # Source attribution
    "according to", "cited in", "published in", "researchers at", 
    
    # Nuanced language
    "suggests", "indicates", "appears to", "may", "could", 
    
    # Specific attribution
    "professor", "Dr.", "spokesperson", "report by", "analysis shows",
    
    # Statistical language
    "percent", "proportion", "survey found", "study shows", "data indicates",
    
    # Balanced reporting
    "however", "on the other hand", "critics say", "proponents argue"
]

class ImprovedFakeNewsDetector:
    """Advanced fake news detection with detailed analysis and explanation."""
    
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
            
    def predict(self, text, detailed=False, explain=False, explanation_method="lime", num_features=10):
        """
        Predict whether a text is fake or real news.
        
        Args:
            text (str): Input text
            detailed (bool): Whether to return detailed analysis
            explain (bool): Whether to return model explanations
            explanation_method (str): Method for explanations ('lime', 'shap', or 'both')
            num_features (int): Number of features to include in explanations
            
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
                'timestamp': datetime.now().isoformat()
            }
            
            # Add detailed analysis if requested
            if detailed:
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
        
        # Find warning signs
        warning_signs = self._identify_warning_signs(raw_text)
        
        # Create word clouds and phrase analysis
        word_analysis = self._analyze_word_usage(raw_text)
        
        # Generate explanation
        explanation = self._generate_explanation(features, style_analysis, warning_signs, prediction, confidence)
        
        # Return detailed analysis
        return {
            'detailed_analysis': {
                'text_features': features,
                'writing_style': style_analysis,
                'warning_signs': warning_signs,
                'word_analysis': word_analysis,
            },
            'explanation': explanation,
            'credibility_score': self._calculate_credibility_score(features, style_analysis, warning_signs, confidence)
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
            return {"error": "Explainers not available"}
        
        try:
            # Get explanations
            if method.lower() == "lime":
                explanations = self.explainer.explain_with_lime(text, num_features=num_features)
                return {
                    "method": "LIME",
                    "explanations": explanations,
                    "highlighted_text": self.explainer.get_highlighted_text(text, explanations)
                }
            
            elif method.lower() == "shap":
                explanations = self.explainer.explain_with_shap(text, num_features=num_features)
                return {
                    "method": "SHAP",
                    "explanations": explanations,
                    "highlighted_text": self.explainer.get_highlighted_text(text, explanations)
                }
            
            elif method.lower() == "both":
                result = self.explainer.explain_prediction(text, method="both", num_features=num_features)
                return {
                    "method": "LIME+SHAP",
                    "lime_explanations": result["explanations"].get("lime"),
                    "shap_explanations": result["explanations"].get("shap"),
                    "highlighted_text": result.get("highlighted_text_html")
                }
            
            else:
                return {"error": f"Unknown explanation method: {method}"}
                
        except Exception as e:
            logger.error(f"Error generating model explanations: {e}", exc_info=True)
            return {"error": f"Failed to generate explanations: {str(e)}"}
    
    def _identify_warning_signs(self, text):
        """
        Identify warning signs of misinformation in the text.
        
        Args:
            text (str): Input text
            
        Returns:
            dict: Warning signs analysis
        """
        text_lower = text.lower()
        
        # Find misinformation indicators
        misinformation_matches = []
        for phrase in MISINFORMATION_INDICATORS:
            if phrase.lower() in text_lower:
                misinformation_matches.append(phrase)
        
        # Find reliability indicators
        reliability_matches = []
        for phrase in RELIABILITY_INDICATORS:
            if phrase.lower() in text_lower:
                reliability_matches.append(phrase)
        
        # Check for excessive punctuation
        excessive_punctuation = False
        punctuation_count = sum(1 for char in text if char in '!?.')
        if punctuation_count > len(text.split()) * 0.2:  # More than 20% of word count
            excessive_punctuation = True
        
        # Check for excessive capitalization
        excessive_caps = False
        words = text.split()
        caps_count = sum(1 for word in words if word.isupper() and len(word) > 1)
        if caps_count > len(words) * 0.1:  # More than 10% of words in ALL CAPS
            excessive_caps = True
        
        # Check for social media callouts
        social_media_callout = any(phrase in text_lower for phrase in 
                                  ['share this', 'like and share', 'retweet', 'spread the word'])
        
        # Check for source credibility issues
        source_issues = any(phrase in text_lower for phrase in 
                           ['anonymous sources', 'unnamed sources', 'sources say',
                            'someone told me', 'they don\'t want you to know'])
        
        return {
            'misinformation_indicators': misinformation_matches,
            'reliability_indicators': reliability_matches,
            'excessive_punctuation': excessive_punctuation,
            'excessive_capitalization': excessive_caps,
            'social_media_callout': social_media_callout,
            'source_credibility_issues': source_issues
        }
    
    def _analyze_word_usage(self, text):
        """
        Analyze word usage patterns in the text.
        
        Args:
            text (str): Input text
            
        Returns:
            dict: Word usage analysis
        """
        # Get most common words
        words = re.findall(r'\b\w+\b', text.lower())
        word_freq = pd.Series(words).value_counts().head(10).to_dict()
        
        # Get bigrams
        bigram_freq = get_ngram_frequencies(text, n=2)
        top_bigrams = dict(sorted(bigram_freq.items(), key=lambda x: x[1], reverse=True)[:10])
        
        # Emotional language assessment
        emotional_words = ['shocking', 'outrageous', 'amazing', 'incredible', 'terrifying',
                          'alarming', 'devastating', 'horrific', 'scandalous', 'appalling']
        emotional_count = sum(1 for word in words if word in emotional_words)
        
        # Scientific/technical language assessment
        scientific_words = ['study', 'research', 'analysis', 'evidence', 'data', 
                           'experiment', 'statistics', 'journal', 'publication', 'conclusion']
        scientific_count = sum(1 for word in words if word in scientific_words)
        
        return {
            'top_words': word_freq,
            'top_bigrams': top_bigrams,
            'emotional_language_count': emotional_count,
            'scientific_language_count': scientific_count
        }
    
    def _calculate_credibility_score(self, features, style_analysis, warning_signs, model_confidence):
        """
        Calculate an overall credibility score (0-100) based on multiple factors.
        
        Args:
            features (dict): Text features
            style_analysis (dict): Writing style analysis
            warning_signs (dict): Warning signs
            model_confidence (float): Model confidence
            
        Returns:
            float: Credibility score (0-100)
        """
        # Start with base score (model confidence scaled to 0-100)
        if model_confidence > 0.5:  # If prediction is REAL
            base_score = model_confidence * 100
        else:  # If prediction is FAKE
            base_score = (1 - model_confidence) * 100
        
        # Adjust for warning signs
        misinformation_penalty = len(warning_signs['misinformation_indicators']) * 5
        reliability_bonus = len(warning_signs['reliability_indicators']) * 3
        
        # Penalties for other warning signs
        other_penalties = 0
        if warning_signs['excessive_punctuation']:
            other_penalties += 10
        if warning_signs['excessive_capitalization']:
            other_penalties += 10
        if warning_signs['social_media_callout']:
            other_penalties += 15
        if warning_signs['source_credibility_issues']:
            other_penalties += 20
        
        # Adjust for writing style
        style_score = 0
        if style_analysis['reading_ease'] > 60:  # More readable text is typically more credible
            style_score += 5
        
        # Penalties for high subjectivity and extreme polarity
        if features['subjectivity'] > 0.7:  # High subjectivity
            style_score -= 10
        
        if abs(features['polarity']) > 0.7:  # Extreme sentiment
            style_score -= 10
        
        # Calculate final score and ensure it's within 0-100 range
        final_score = base_score + reliability_bonus - misinformation_penalty - other_penalties + style_score
        final_score = max(0, min(100, final_score))
        
        return round(final_score, 1)
    
    def _generate_explanation(self, features, style_analysis, warning_signs, prediction, confidence):
        """
        Generate a human-readable explanation for the prediction.
        
        Args:
            features (dict): Text features
            style_analysis (dict): Writing style analysis
            warning_signs (dict): Warning signs
            prediction (str): Prediction label
            confidence (float): Prediction confidence
            
        Returns:
            str: Human-readable explanation
        """
        explanation = []
        
        # Start with the model's prediction
        if prediction == "FAKE":
            explanation.append(f"This text appears to be potentially misleading or fake news (model confidence: {confidence:.1%}).")
        else:
            explanation.append(f"This text appears to be potentially reliable or real news (model confidence: {confidence:.1%}).")
        
        # Add explanation based on warning signs
        misinformation_count = len(warning_signs['misinformation_indicators'])
        reliability_count = len(warning_signs['reliability_indicators'])
        
        if misinformation_count > 0:
            explanation.append(f"Found {misinformation_count} indicators of potential misinformation, including: {', '.join(warning_signs['misinformation_indicators'][:3])}.")
        
        if reliability_count > 0:
            explanation.append(f"Found {reliability_count} indicators of potential reliability, including: {', '.join(warning_signs['reliability_indicators'][:3])}.")
        
        # Add style analysis
        if warning_signs['excessive_punctuation']:
            explanation.append("The text contains excessive punctuation, which is common in sensationalized content.")
        
        if warning_signs['excessive_capitalization']:
            explanation.append("The text contains excessive capitalization, which is common in sensationalized content.")
        
        if warning_signs['social_media_callout']:
            explanation.append("The text contains calls to share on social media, which is common in viral misinformation.")
        
        if warning_signs['source_credibility_issues']:
            explanation.append("The text references anonymous or vague sources, which reduces credibility.")
        
        # Add sentiment analysis
        if features['subjectivity'] > 0.7:
            explanation.append(f"The text is highly subjective (score: {features['subjectivity']:.2f}), which may indicate opinion rather than fact-based reporting.")
        
        if abs(features['polarity']) > 0.7:
            explanation.append(f"The text has extreme sentiment (polarity: {features['polarity']:.2f}), which may indicate emotional language rather than balanced reporting.")
        
        # Add writing style analysis
        if style_analysis['exaggeration_phrases'] > 2:
            explanation.append(f"The text contains {style_analysis['exaggeration_phrases']} exaggeration phrases, which may indicate overstatement.")
        
        if style_analysis['hedging_phrases'] > 2:
            explanation.append(f"The text contains {style_analysis['hedging_phrases']} hedging phrases, which may indicate uncertainty.")
        
        # Join all explanations
        return " ".join(explanation)
    
    def save_report(self, text, prediction_result, filename=None):
        """
        Save a detailed prediction report to file.
        
        Args:
            text (str): Original text
            prediction_result (dict): Prediction result
            filename (str): Optional filename
            
        Returns:
            str: Path to saved report
        """
        if filename is None:
            # Generate filename from timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"report_{timestamp}.json"
        
        # Create full report
        report = {
            'original_text': text,
            'prediction': prediction_result,
            'timestamp': datetime.now().isoformat()
        }
        
        # Save to file
        report_path = os.path.join(REPORTS_DIR, filename)
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Report saved to {report_path}")
        return report_path
    
    def explain_prediction_with_lime(self, text, num_features=10):
        """
        Generate LIME explanations for a text prediction.
        
        Args:
            text (str): Text to analyze
            num_features (int): Number of features to include
            
        Returns:
            dict: LIME explanation results
        """
        if not EXPLAINERS_AVAILABLE or not self.explainer:
            return {"error": "LIME explainer not available"}
        
        return self.explainer.explain_with_lime(text, num_features=num_features)
    
    def explain_prediction_with_shap(self, text, num_features=10):
        """
        Generate SHAP explanations for a text prediction.
        
        Args:
            text (str): Text to analyze
            num_features (int): Number of features to include
            
        Returns:
            dict: SHAP explanation results
        """
        if not EXPLAINERS_AVAILABLE or not self.explainer:
            return {"error": "SHAP explainer not available"}
        
        return self.explainer.explain_with_shap(text, num_features=num_features)
    
    def get_combined_explanation(self, text, num_features=10):
        """
        Get both LIME and SHAP explanations for a text.
        
        Args:
            text (str): Text to analyze
            num_features (int): Number of features to include
            
        Returns:
            dict: Combined explanation results
        """
        if not EXPLAINERS_AVAILABLE or not self.explainer:
            return {"error": "Explainers not available"}
        
        return self.explainer.explain_prediction(text, method="both", num_features=num_features)

# Example usage
if __name__ == "__main__":
    # Initialize detector
    detector = ImprovedFakeNewsDetector()
    
    # Example texts
    fake_news_example = """
    SHOCKING NEWS! Scientists discover that vaccines cause autism! 
    The government doesn't want YOU to know this INCREDIBLE truth. 
    According to sources close to the investigation, this conspiracy has been 
    going on for YEARS! Share this with everyone you know!!!
    """
    
    real_news_example = """
    A new study published in the Journal of Medical Research has found a correlation 
    between regular exercise and improved mental health. The researchers at Stanford 
    University followed 500 participants over the course of two years and observed 
    that those who exercised at least three times per week reported 25% fewer symptoms 
    of depression and anxiety compared to the control group.
    """
    
    # Predict with detailed analysis
    fake_result = detector.predict(fake_news_example, detailed=True)
    real_result = detector.predict(real_news_example, detailed=True)
    
    # Print results
    print("\nPrediction for potentially fake news:")
    print(f"Prediction: {fake_result['prediction']}")
    print(f"Confidence: {fake_result['confidence']:.2%}")
    if 'credibility_score' in fake_result:
        print(f"Credibility Score: {fake_result['credibility_score']}/100")
    if 'explanation' in fake_result:
        print(f"Explanation: {fake_result['explanation']}")
    
    print("\nPrediction for potentially real news:")
    print(f"Prediction: {real_result['prediction']}")
    print(f"Confidence: {real_result['confidence']:.2%}")
    if 'credibility_score' in real_result:
        print(f"Credibility Score: {real_result['credibility_score']}/100")
    if 'explanation' in real_result:
        print(f"Explanation: {real_result['explanation']}")
    
    # Generate explanations if available
    if EXPLAINERS_AVAILABLE:
        print("\n--- LIME and SHAP Explanations ---")
        
        # Get explanations for fake news
        fake_explanations = detector.get_combined_explanation(fake_news_example)
        
        if "error" not in fake_explanations:
            print("\nFake News LIME Explanation:")
            lime_features = fake_explanations["explanations"]["lime"]["top_features"]
            for i, feature in enumerate(lime_features[:5]):
                print(f"  {i+1}. {feature['word']}: {feature['importance']:.4f}")
                
            print("\nFake News SHAP Explanation:")
            if "shap" in fake_explanations["explanations"]:
                shap_features = fake_explanations["explanations"]["shap"]["top_features"]
                for i, feature in enumerate(shap_features[:5]):
                    print(f"  {i+1}. {feature['word']}: {feature['importance']:.4f}")
        
        # Save reports
        detector.save_report(fake_news_example, fake_result, "fake_news_report.json")
        detector.save_report(real_news_example, real_result, "real_news_report.json") 