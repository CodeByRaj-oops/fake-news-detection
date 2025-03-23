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
import pickle
import uuid
from typing import Dict, Any, List, Optional, Union, Tuple

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
from utils.text_processor import analyze_text_features, detect_clickbait

# Import explainer utilities
try:
    from utils.explainers import (
        ModelExplainer,
        explain_with_lime,
        explain_with_shap,
        get_combined_explanation,
        generate_lime_explanation,
        generate_shap_explanation
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

# Model paths
MODEL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models')
VECTORIZER_PATH = os.path.join(MODEL_DIR, 'vectorizer.pkl')
MODEL_PATH = os.path.join(MODEL_DIR, 'model.pkl')

# Ensure directories exist
os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'history'), exist_ok=True)

class EnhancedFakeNewsDetector:
    """
    Enhanced fake news detection with comprehensive analysis, language detection,
    entity recognition, and more detailed text analysis.
    """
    
    def __init__(self):
        """
        Initialize the detector with models
        """
        try:
            # Load vectorizer
            with open(VECTORIZER_PATH, 'rb') as f:
                self.vectorizer = pickle.load(f)
                
            # Load model
            with open(MODEL_PATH, 'rb') as f:
                self.model = pickle.load(f)
                
            self.loaded = True
            
            # Initialize explainer if available
            self.explainer = None
            if EXPLAINERS_AVAILABLE:
                self.explainer = ModelExplainer(self.model)
                logger.info("Model explainer initialized")
        except (FileNotFoundError, OSError, pickle.PickleError) as e:
            print(f"Error loading models: {e}")
            self.loaded = False
            self.explainer = None
            
    def predict(self, text: str, explain: bool = False, explanation_method: str = 'lime') -> Dict[str, Any]:
        """
        Predict if text is fake news
        
        Args:
            text (str): Input text to analyze
            explain (bool): Whether to include explanation
            explanation_method (str): Method for generating explanation (lime or shap)
            
        Returns:
            Dict[str, Any]: Prediction results
        """
        if not self.loaded:
            return {"error": "Model not loaded properly"}
        
        if not text or not isinstance(text, str):
            return {"error": "Invalid text input"}
        
        # Generate a unique ID for this prediction
        item_id = str(uuid.uuid4())
        
        # Process text
        processed_text = preprocess_text(text)
        
        # Vectorize
        features = self.vectorizer.transform([processed_text])
        
        # Predict
        prediction_proba = self.model.predict_proba(features)[0]
        prediction_label = 'FAKE' if prediction_proba[1] > 0.5 else 'REAL'
        confidence = prediction_proba[1] if prediction_label == 'FAKE' else prediction_proba[0]
        
        # Create result object
        result = {
            "id": item_id,
            "timestamp": datetime.now().isoformat(),
            "text": text[:1000],  # Limit to first 1000 chars for storage
            "processed_text": processed_text,
            "label": prediction_label,
            "confidence": float(confidence),
            "fake_probability": float(prediction_proba[1])
        }
        
        # Add explanation if requested
        if explain and EXPLAINERS_AVAILABLE:
            try:
                if explanation_method.lower() == 'lime':
                    explanation = generate_lime_explanation(
                        self.model, self.vectorizer, text, processed_text
                    )
                    result["explanation"] = explanation
                elif explanation_method.lower() == 'shap':
                    explanation = generate_shap_explanation(
                        self.model, self.vectorizer, text, processed_text
                    )
                    result["explanation"] = explanation
                else:
                    result["explanation_error"] = f"Unknown explanation method: {explanation_method}"
            except Exception as e:
                result["explanation_error"] = f"Error generating explanation: {str(e)}"
        
        # Save to history
        self._save_to_history(item_id, result)
        
        return result
    
    def enhanced_analysis(self, text: str) -> Dict[str, Any]:
        """
        Enhanced analysis with additional features beyond simple prediction
        
        Args:
            text (str): Input text to analyze
            
        Returns:
            Dict[str, Any]: Analysis results including prediction and additional features
        """
        # Get basic prediction first
        prediction = self.predict(text)
        
        if "error" in prediction:
            return prediction
        
        # Add language detection
        prediction["language"] = detect_language(text)
        
        # Add entity extraction
        prediction["entities"] = extract_entities(text)
        
        # Add readability metrics
        prediction["readability"] = calculate_readability_metrics(text)
        
        # Add text uniqueness analysis
        prediction["uniqueness"] = analyze_text_uniqueness(text)
        
        # Add clickbait detection
        prediction["clickbait"] = detect_clickbait(text)
        
        # Add propaganda techniques detection
        prediction["propaganda"] = detect_propaganda_techniques(text)
        
        # Save enhanced result to history
        self._save_to_history(prediction["id"], prediction, enhanced=True)
        
        return prediction
    
    def comprehensive_analysis(self, text: str) -> Dict[str, Any]:
        """
        Comprehensive analysis that includes all available metrics
        
        Args:
            text (str): Input text to analyze
            
        Returns:
            Dict[str, Any]: Complete analysis results
        """
        # Get basic prediction
        prediction = self.predict(text)
        
        if "error" in prediction:
            return prediction
        
        # Perform comprehensive text analysis
        text_analysis = comprehensive_text_analysis(text)
        
        # Merge results
        for key, value in text_analysis.items():
            if key != "error":
                prediction[key] = value
        
        # Save comprehensive result to history
        self._save_to_history(prediction["id"], prediction, enhanced=True, comprehensive=True)
        
        return prediction
    
    def _save_to_history(self, item_id: str, data: Dict[str, Any], 
                         enhanced: bool = False, comprehensive: bool = False) -> None:
        """Save analysis result to history"""
        history_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'history')
        os.makedirs(history_dir, exist_ok=True)
        
        try:
            # Create a filename with type indicator
            type_indicator = "comprehensive" if comprehensive else "enhanced" if enhanced else "basic"
            filename = f"{item_id}_{type_indicator}.json"
            filepath = os.path.join(history_dir, filename)
            
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving to history: {e}")
    
    def get_history(self, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Get analysis history
        
        Args:
            limit (int): Maximum number of items to return
            
        Returns:
            List[Dict[str, Any]]: Recent analysis results
        """
        history_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'history')
        
        if not os.path.exists(history_dir):
            return []
        
        try:
            history_files = [os.path.join(history_dir, f) for f in os.listdir(history_dir) 
                             if f.endswith('.json')]
            
            # Sort by modification time, newest first
            history_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
            
            # Limit number of results
            history_files = history_files[:limit]
            
            # Load history items
            history = []
            for file_path in history_files:
                try:
                    with open(file_path, 'r') as f:
                        item = json.load(f)
                        # Extract ID from filename
                        item_id = os.path.basename(file_path).split('_')[0]
                        history.append(item)
                except Exception as e:
                    print(f"Error loading history item {file_path}: {e}")
            
            return history
        except Exception as e:
            print(f"Error retrieving history: {e}")
            return []
    
    def get_history_item(self, item_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific history item by ID
        
        Args:
            item_id (str): The ID of the history item
            
        Returns:
            Optional[Dict[str, Any]]: The history item if found
        """
        history_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'history')
        
        if not os.path.exists(history_dir):
            return None
        
        try:
            # Look for any file starting with the item_id
            matching_files = [os.path.join(history_dir, f) for f in os.listdir(history_dir) 
                             if f.startswith(f"{item_id}_") and f.endswith('.json')]
            
            if not matching_files:
                return None
            
            # Prefer comprehensive > enhanced > basic
            for type_indicator in ["comprehensive", "enhanced", "basic"]:
                for file_path in matching_files:
                    if type_indicator in file_path:
                        with open(file_path, 'r') as f:
                            return json.load(f)
            
            # If no preferred type found, return the first match
            with open(matching_files[0], 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error retrieving history item {item_id}: {e}")
            return None
    
    def get_available_explanation_methods(self) -> List[str]:
        """
        Get list of available explanation methods
        
        Returns:
            List[str]: List of available explanation method names
        """
        if EXPLAINERS_AVAILABLE:
            return ["lime", "shap"]
        return []
    
    def generate_report(self, item_id: str = None, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Generate a detailed report from analysis data
        
        Args:
            item_id (str, optional): ID of history item to use
            data (Dict[str, Any], optional): Analysis data to use directly
            
        Returns:
            Dict[str, Any]: Detailed report
        """
        if not data and not item_id:
            return {"error": "Either item_id or data must be provided"}
        
        if not data:
            data = self.get_history_item(item_id)
            if not data:
                return {"error": f"History item not found: {item_id}"}
        
        # Generate a report ID if none exists
        report_id = data.get("id", str(uuid.uuid4()))
        
        # Create report structure
        report = {
            "id": report_id,
            "generated_at": datetime.now().isoformat(),
            "analysis_timestamp": data.get("timestamp", "unknown"),
            "summary": {
                "verdict": data.get("label", "Unknown"),
                "confidence": data.get("confidence", 0.0) * 100,
                "text_length": len(data.get("text", "")),
            },
            "details": {}
        }
        
        # Add language info if available
        language = data.get("language")
        if language:
            report["summary"]["language"] = language.get("language_name", "Unknown")
            report["details"]["language"] = language
        
        # Add readability if available
        readability = data.get("readability")
        if readability:
            report["summary"]["reading_level"] = readability.get("average_grade_level", 0.0)
            report["details"]["readability"] = readability
        
        # Add propaganda score if available
        propaganda = data.get("propaganda")
        if propaganda:
            report["summary"]["propaganda_score"] = propaganda.get("propaganda_score", 0.0)
            report["details"]["propaganda"] = propaganda
        
        # Add clickbait info if available
        clickbait = data.get("clickbait")
        if clickbait:
            report["summary"]["clickbait_score"] = clickbait.get("clickbait_score", 0.0) * 100
            report["details"]["clickbait"] = clickbait
        
        # Save report
        reports_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'reports')
        os.makedirs(reports_dir, exist_ok=True)
        
        try:
            report_path = os.path.join(reports_dir, f"report_{report_id}.json")
            with open(report_path, 'w') as f:
                json.dump(report, f, indent=2)
        except Exception as e:
            print(f"Error saving report: {e}")
        
        return report

# Create a global instance for reuse
detector = EnhancedFakeNewsDetector()

# Functions to be called by the API
def predict_fake_news(text: str, explain: bool = False, explanation_method: str = 'lime') -> Dict[str, Any]:
    """Wrapper function for basic prediction"""
    return detector.predict(text, explain, explanation_method)

def perform_enhanced_analysis(text: str) -> Dict[str, Any]:
    """Wrapper function for enhanced analysis"""
    return detector.enhanced_analysis(text)

def perform_comprehensive_analysis(text: str) -> Dict[str, Any]:
    """Wrapper function for comprehensive analysis"""
    return detector.comprehensive_analysis(text)

def get_analysis_history(limit: int = 20) -> List[Dict[str, Any]]:
    """Wrapper function for getting analysis history"""
    return detector.get_history(limit)

def get_analysis_item(item_id: str) -> Optional[Dict[str, Any]]:
    """Wrapper function for getting a specific analysis item"""
    return detector.get_history_item(item_id)

def get_explanation_methods() -> List[str]:
    """Wrapper function for getting available explanation methods"""
    return detector.get_available_explanation_methods()

def generate_analysis_report(item_id: str = None, data: Dict[str, Any] = None) -> Dict[str, Any]:
    """Wrapper function for generating a report"""
    return detector.generate_report(item_id, data)

# Example usage
if __name__ == "__main__":
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