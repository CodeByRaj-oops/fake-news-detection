#!/usr/bin/env python3
"""
Script to train a fake news detection model using the Kaggle Fake and Real News dataset.
"""

import os
import pandas as pd
import numpy as np
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import logging
import time
import nltk

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), 'data')
MODELS_DIR = os.path.join(SCRIPT_DIR, 'models')
os.makedirs(MODELS_DIR, exist_ok=True)

# Import text processing function
from utils.text_processor import preprocess_text

def load_data():
    """
    Load and combine the Fake and Real news datasets.
    
    Returns:
        pd.DataFrame: Combined dataframe with 'text' and 'label' columns
    """
    logger.info("Loading datasets...")
    
    # Check for expected files
    fake_path = os.path.join(DATA_DIR, 'Fake.csv')
    true_path = os.path.join(DATA_DIR, 'True.csv')
    
    if not os.path.exists(fake_path) or not os.path.exists(true_path):
        raise FileNotFoundError(
            f"Dataset files not found. Please download from Kaggle and place in {DATA_DIR}."
            "Expected files: Fake.csv, True.csv"
        )
    
    # Load datasets
    fake_df = pd.read_csv(fake_path)
    true_df = pd.read_csv(true_path)
    
    # Add labels
    fake_df['label'] = 'FAKE'
    true_df['label'] = 'REAL'
    
    # Combine datasets
    df = pd.concat([fake_df, true_df], ignore_index=True)
    
    # Check if expected columns exist
    if 'text' not in df.columns:
        # If 'text' doesn't exist, try to create it from title and content
        if 'title' in df.columns and 'text' in df.columns:
            df['text'] = df['title'] + ' ' + df['text']
        else:
            # Use whatever text columns are available
            text_cols = [col for col in df.columns if df[col].dtype == 'object' and col != 'label']
            df['text'] = df[text_cols[0]] if text_cols else ''
    
    # Keep only needed columns
    df = df[['text', 'label']]
    
    logger.info(f"Loaded {len(df)} articles ({len(fake_df)} fake, {len(true_df)} real)")
    
    return df

def process_data(df):
    """
    Preprocess the text data.
    
    Args:
        df (pd.DataFrame): Input dataframe with 'text' column
        
    Returns:
        pd.DataFrame: Dataframe with processed text
    """
    logger.info("Preprocessing text data...")
    
    start_time = time.time()
    
    # Apply preprocessing to the text
    df['processed_text'] = df['text'].apply(preprocess_text)
    
    elapsed_time = time.time() - start_time
    logger.info(f"Preprocessing completed in {elapsed_time:.2f} seconds")
    
    return df

def train_model(df):
    """
    Train a fake news detection model.
    
    Args:
        df (pd.DataFrame): Dataframe with 'processed_text' and 'label' columns
        
    Returns:
        tuple: (trained model, vectorizer)
    """
    logger.info("Training model...")
    
    # Split data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        df['processed_text'], 
        df['label'], 
        test_size=0.2, 
        random_state=42
    )
    
    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer(max_features=10000)
    X_train_vectorized = vectorizer.fit_transform(X_train)
    X_test_vectorized = vectorizer.transform(X_test)
    
    # Train logistic regression model
    logger.info("Training Logistic Regression model...")
    model = LogisticRegression(max_iter=1000, n_jobs=-1)
    model.fit(X_train_vectorized, y_train)
    
    # Evaluate model
    y_pred = model.predict(X_test_vectorized)
    accuracy = accuracy_score(y_test, y_pred)
    
    logger.info(f"Model Accuracy: {accuracy:.4f}")
    logger.info("Classification Report:")
    logger.info(classification_report(y_test, y_pred))
    
    # Save model and vectorizer
    joblib.dump(model, os.path.join(MODELS_DIR, 'fake_news_model.pkl'))
    joblib.dump(vectorizer, os.path.join(MODELS_DIR, 'vectorizer.pkl'))
    
    logger.info(f"Model and vectorizer saved to {MODELS_DIR}")
    
    return model, vectorizer

def main():
    """Main function to execute the training pipeline."""
    try:
        # Ensure NLTK data is downloaded
        nltk.download('punkt')
        nltk.download('stopwords')
        
        # Load and process data
        df = load_data()
        processed_df = process_data(df)
        
        # Train and save model
        model, vectorizer = train_model(processed_df)
        
        logger.info("Training pipeline completed successfully!")
        
    except Exception as e:
        logger.error(f"Error in training pipeline: {e}")
        raise

if __name__ == "__main__":
    main() 