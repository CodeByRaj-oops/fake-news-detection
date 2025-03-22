#!/usr/bin/env python3
"""
Explanation utilities for fake news detection using LIME and SHAP.
"""

import os
import sys
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.pipeline import Pipeline
import joblib
from typing import Dict, List, Tuple, Union, Callable, Any, Optional

# Import LIME and SHAP
try:
    import lime
    import lime.lime_text
    import shap
    from lime.lime_text import LimeTextExplainer
except ImportError:
    raise ImportError(
        "Please install LIME and SHAP packages with: pip install lime shap"
    )

# Add parent directory to path to allow imports
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
sys.path.append(parent_dir)

# Import text processing utilities
from utils.improved_text_processor import preprocess_text


class ModelExplainer:
    """Wrapper class to provide explanations for fake news detection models."""

    def __init__(self, model, class_names=None):
        """
        Initialize the explainer with a trained model.
        
        Args:
            model: Trained scikit-learn pipeline or model
            class_names: List of class names (e.g., ["REAL", "FAKE"])
        """
        self.model = model
        
        # Determine if the model is a pipeline
        self.is_pipeline = isinstance(self.model, Pipeline)
        
        # Try to extract the classifier and vectorizer from pipeline
        if self.is_pipeline:
            self.vectorizer = None
            self.classifier = None
            
            # Find TF-IDF vectorizer in pipeline
            for name, transformer in self.model.named_steps.items():
                if "tfidf" in name.lower() or hasattr(transformer, 'transform'):
                    self.vectorizer = transformer
                if hasattr(transformer, 'predict_proba'):
                    self.classifier = transformer
        
        # Set class names
        if class_names is None:
            if hasattr(self.model, 'classes_'):
                self.class_names = self.model.classes_
            else:
                # Default to binary classification
                self.class_names = ["REAL", "FAKE"]
        else:
            self.class_names = class_names
    
    def _preprocess_text(self, text):
        """Preprocess text consistently with the model's training."""
        return preprocess_text(text)
    
    def explain_with_lime(self, text, num_features=10, num_samples=3000):
        """
        Generate explanations using LIME for the model's prediction on a text sample.
        
        Args:
            text (str): The text to explain
            num_features (int): Number of features to include in the explanation
            num_samples (int): Number of samples to use for perturbation
            
        Returns:
            dict: LIME explanation results including top features
        """
        # Preprocess text
        processed_text = self._preprocess_text(text)
        
        # Create a pipeline prediction function for LIME
        def pipeline_predict_proba(texts):
            return self.model.predict_proba([self._preprocess_text(t) for t in texts])
        
        # Initialize LIME explainer
        explainer = LimeTextExplainer(
            class_names=self.class_names,
            split_expression=r'\s+',  # Split by whitespace
            bow=True,  # Use bag-of-words representation
            random_state=42
        )
        
        # Generate explanation
        explanation = explainer.explain_instance(
            text,  # Use original text
            pipeline_predict_proba,  # Use our prediction function
            num_features=num_features,
            num_samples=num_samples
        )
        
        # Get prediction class and probability
        prediction_proba = self.model.predict_proba([processed_text])[0]
        prediction_idx = np.argmax(prediction_proba)
        predicted_class = self.class_names[prediction_idx]
        
        # Get explanations for the predicted class
        top_features = explanation.as_list(label=prediction_idx)
        
        # Return explanation data
        explanation_data = {
            "method": "LIME",
            "predicted_class": predicted_class,
            "predicted_probability": float(prediction_proba[prediction_idx]),
            "explained_class": predicted_class,
            "top_features": [
                {"word": feature[0], "importance": feature[1]} 
                for feature in top_features
            ],
            "positive_words": [
                feature[0] for feature in top_features if feature[1] > 0
            ],
            "negative_words": [
                feature[0] for feature in top_features if feature[1] < 0
            ]
        }
        
        # Create HTML explanation for visualization
        explanation_data["explanation_html"] = explanation.as_html()
        
        return explanation_data
    
    def explain_with_shap(self, text, num_features=10, background_samples=None):
        """
        Generate explanations using SHAP for the model's prediction on a text sample.
        
        Args:
            text (str): The text to explain
            num_features (int): Number of features to include in the explanation
            background_samples (list): List of background samples for SHAP
            
        Returns:
            dict: SHAP explanation results including top features
        """
        # Preprocess text
        processed_text = self._preprocess_text(text)
        
        if self.is_pipeline and self.vectorizer and self.classifier:
            # Transform text using the vectorizer
            vectorized_text = self.vectorizer.transform([processed_text])
            
            # Choose the right SHAP explainer based on the model type
            classifier_type = type(self.classifier).__name__.lower()
            
            # Initialize SHAP explainer based on classifier type
            if "tree" in classifier_type or "forest" in classifier_type or "boost" in classifier_type:
                # For tree-based models (Random Forest, Gradient Boosting, etc.)
                explainer = shap.TreeExplainer(self.classifier)
                shap_values = explainer.shap_values(vectorized_text)
                
                # If classifier returns a list of shap values (one per class),
                # take the values for the predicted class
                prediction_idx = np.argmax(self.classifier.predict_proba(vectorized_text))
                if isinstance(shap_values, list):
                    shap_values = shap_values[prediction_idx]
                
            else:
                # For other models (Logistic Regression, SVM, etc.)
                # We need background samples for KernelExplainer
                if background_samples is None:
                    # Create simple background dataset
                    background_samples = vectorized_text
                
                explainer = shap.KernelExplainer(
                    self.classifier.predict_proba, background_samples
                )
                shap_values = explainer.shap_values(vectorized_text, nsamples=100)
                
                # For binary classification, take the values for the predicted class
                prediction_idx = np.argmax(self.classifier.predict_proba(vectorized_text))
                if isinstance(shap_values, list):
                    shap_values = shap_values[prediction_idx]
            
            # Get feature names if available
            if hasattr(self.vectorizer, 'get_feature_names_out'):
                feature_names = self.vectorizer.get_feature_names_out()
            elif hasattr(self.vectorizer, 'get_feature_names'):
                feature_names = self.vectorizer.get_feature_names()
            else:
                feature_names = [f"feature_{i}" for i in range(vectorized_text.shape[1])]
            
            # Convert sparse matrix to dense if needed
            if hasattr(vectorized_text, "toarray"):
                dense_text = vectorized_text.toarray()[0]
            else:
                dense_text = vectorized_text[0]
            
            # Only keep features that actually appear in the text (non-zero)
            non_zero_indices = np.where(dense_text != 0)[0]
            values = [(feature_names[i], float(shap_values[0, i])) for i in non_zero_indices]
            
            # Sort by absolute SHAP value
            sorted_values = sorted(values, key=lambda x: abs(x[1]), reverse=True)
            top_features = sorted_values[:num_features]
            
            # Get prediction
            prediction_proba = self.classifier.predict_proba(vectorized_text)[0]
            predicted_class = self.class_names[prediction_idx]
            
            # Return explanation data
            explanation_data = {
                "method": "SHAP",
                "predicted_class": predicted_class,
                "predicted_probability": float(prediction_proba[prediction_idx]),
                "explained_class": predicted_class,
                "top_features": [
                    {"word": feature[0], "importance": feature[1]} 
                    for feature in top_features
                ],
                "positive_words": [
                    feature[0] for feature in top_features if feature[1] > 0
                ],
                "negative_words": [
                    feature[0] for feature in top_features if feature[1] < 0
                ]
            }
            
            return explanation_data
        else:
            # If not a pipeline or components not found, use a simpler approach
            return self.explain_with_lime(text, num_features, num_samples=100)
    
    def get_highlighted_text(self, text, explanation_data, mode="html"):
        """
        Generate highlighted text to visualize important words.
        
        Args:
            text (str): Original text
            explanation_data (dict): Explanation data from LIME or SHAP
            mode (str): Output format ('html' or 'console')
            
        Returns:
            str: Text with highlighting for important words
        """
        # Get positive and negative words
        positive_words = explanation_data.get("positive_words", [])
        negative_words = explanation_data.get("negative_words", [])
        
        # Prepare regular expressions for highlighting
        # Convert words to regex patterns that match whole words only
        pos_patterns = [re.compile(r'\b{}\b'.format(re.escape(word))) for word in positive_words]
        neg_patterns = [re.compile(r'\b{}\b'.format(re.escape(word))) for word in negative_words]
        
        highlighted_text = text
        
        if mode == "html":
            # For HTML output, use span tags with colors
            for pattern in pos_patterns:
                highlighted_text = pattern.sub(r'<span style="background-color: #c6ecc6; font-weight: bold;">\g<0></span>', highlighted_text)
            
            for pattern in neg_patterns:
                highlighted_text = pattern.sub(r'<span style="background-color: #ffcccb; font-weight: bold;">\g<0></span>', highlighted_text)
            
            # Wrap in a div with some basic styling
            highlighted_text = f'<div style="font-family: Arial, sans-serif; line-height: 1.6; padding: 10px;">{highlighted_text}</div>'
        
        elif mode == "console":
            # For console output, use ANSI escape codes for colors
            for pattern in pos_patterns:
                highlighted_text = pattern.sub(r'\033[42m\g<0>\033[0m', highlighted_text)
            
            for pattern in neg_patterns:
                highlighted_text = pattern.sub(r'\033[41m\g<0>\033[0m', highlighted_text)
        
        return highlighted_text
    
    def explain_prediction(self, text, method="both", num_features=10):
        """
        Explain a prediction using specified methods.
        
        Args:
            text (str): The text to explain
            method (str): Explanation method - 'lime', 'shap', or 'both'
            num_features (int): Number of features to include in explanations
            
        Returns:
            dict: Explanation results
        """
        result = {
            "text": text,
            "prediction": None,
            "confidence": None,
            "explanations": {}
        }
        
        # Get prediction
        processed_text = self._preprocess_text(text)
        prediction_proba = self.model.predict_proba([processed_text])[0]
        prediction_idx = np.argmax(prediction_proba)
        result["prediction"] = self.class_names[prediction_idx]
        result["confidence"] = float(prediction_proba[prediction_idx])
        
        # Generate explanations
        if method.lower() in ["lime", "both"]:
            result["explanations"]["lime"] = self.explain_with_lime(
                text, num_features=num_features
            )
        
        if method.lower() in ["shap", "both"]:
            result["explanations"]["shap"] = self.explain_with_shap(
                text, num_features=num_features
            )
        
        # Add highlighted text visualization
        if "lime" in result["explanations"]:
            result["highlighted_text_html"] = self.get_highlighted_text(
                text, result["explanations"]["lime"], mode="html"
            )
        elif "shap" in result["explanations"]:
            result["highlighted_text_html"] = self.get_highlighted_text(
                text, result["explanations"]["shap"], mode="html"
            )
        
        return result


# Helper functions for using the explainer
def explain_with_lime(model, text, num_features=10, class_names=None):
    """
    Wrapper function to explain a text sample using LIME.
    
    Args:
        model: Trained model (pipeline or classifier)
        text (str): Text to explain
        num_features (int): Number of features in explanation
        class_names (list): Class names
    
    Returns:
        dict: LIME explanation
    """
    explainer = ModelExplainer(model, class_names=class_names)
    return explainer.explain_with_lime(text, num_features=num_features)


def explain_with_shap(model, text, num_features=10, class_names=None):
    """
    Wrapper function to explain a text sample using SHAP.
    
    Args:
        model: Trained model (pipeline or classifier)
        text (str): Text to explain
        num_features (int): Number of features in explanation
        class_names (list): Class names
    
    Returns:
        dict: SHAP explanation
    """
    explainer = ModelExplainer(model, class_names=class_names)
    return explainer.explain_with_shap(text, num_features=num_features)


def get_combined_explanation(model, text, num_features=10, class_names=None):
    """
    Get explanations from both LIME and SHAP and combine insights.
    
    Args:
        model: Trained model (pipeline or classifier)
        text (str): Text to explain
        num_features (int): Number of features in explanation
        class_names (list): Class names
    
    Returns:
        dict: Combined explanation
    """
    explainer = ModelExplainer(model, class_names=class_names)
    return explainer.explain_prediction(text, method="both", num_features=num_features)


# Example usage
if __name__ == "__main__":
    import os
    from improved_predict import ImprovedFakeNewsDetector
    
    # Initialize the detector
    detector = ImprovedFakeNewsDetector()
    
    # Sample texts
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
    
    # Create explainer
    explainer = ModelExplainer(detector.model, class_names=["REAL", "FAKE"])
    
    # Get explanations
    fake_explanation = explainer.explain_prediction(fake_news_example, method="both")
    real_explanation = explainer.explain_prediction(real_news_example, method="both")
    
    # Print results
    print("\nFake News Explanation:")
    print(f"Prediction: {fake_explanation['prediction']} (Confidence: {fake_explanation['confidence']:.2%})")
    print("\nTop LIME Features:")
    for feature in fake_explanation["explanations"]["lime"]["top_features"][:5]:
        print(f"- {feature['word']}: {feature['importance']:.4f}")
    
    print("\nReal News Explanation:")
    print(f"Prediction: {real_explanation['prediction']} (Confidence: {real_explanation['confidence']:.2%})")
    print("\nTop LIME Features:")
    for feature in real_explanation["explanations"]["lime"]["top_features"][:5]:
        print(f"- {feature['word']}: {feature['importance']:.4f}") 