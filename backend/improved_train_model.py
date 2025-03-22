#!/usr/bin/env python3
"""
Improved script to train a fake news detection model with advanced techniques.
"""

import os
import pandas as pd
import numpy as np
import joblib
import logging
import time
import nltk
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_curve, auc
from sklearn.base import BaseEstimator, TransformerMixin

# Import our improved text processor
from utils.improved_text_processor import preprocess_text, extract_features

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

# Create a figures directory for plots
FIGURES_DIR = os.path.join(SCRIPT_DIR, 'figures')
os.makedirs(FIGURES_DIR, exist_ok=True)

# Custom transformer for extracting text features
class TextFeaturesExtractor(BaseEstimator, TransformerMixin):
    def fit(self, x, y=None):
        return self
    
    def transform(self, texts):
        features_list = [extract_features(text) for text in texts]
        return pd.DataFrame(features_list)

def load_data():
    """
    Load and combine the Fake and Real news datasets with improved error handling.
    
    Returns:
        pd.DataFrame: Combined dataframe with 'text' and 'label' columns
    """
    logger.info("Loading datasets...")
    
    # Check for expected files
    fake_path = os.path.join(DATA_DIR, 'Fake.csv')
    true_path = os.path.join(DATA_DIR, 'True.csv')
    
    if not os.path.exists(fake_path) or not os.path.exists(true_path):
        logger.warning(f"Dataset files not found at expected paths: {fake_path}, {true_path}")
        logger.info("Creating mock data for testing purposes...")
        
        # Create mock data for testing
        return create_mock_data()
    
    try:
        # Load datasets
        fake_df = pd.read_csv(fake_path)
        true_df = pd.read_csv(true_path)
        
        # Add labels
        fake_df['label'] = 'FAKE'
        true_df['label'] = 'REAL'
        
        # Combine datasets
        df = pd.concat([fake_df, true_df], ignore_index=True)
        
        # Create text column if needed
        if 'text' not in df.columns:
            logger.info("'text' column not found, creating from available columns")
            if all(col in df.columns for col in ['title', 'text']):
                df['text'] = df['title'] + ' ' + df['text']
            else:
                text_cols = [col for col in df.columns if df[col].dtype == 'object' and col != 'label']
                if text_cols:
                    df['text'] = df[text_cols[0]]
                else:
                    raise ValueError("No text columns found in dataset")
        
        # Keep only needed columns and remove any rows with missing values
        df = df[['text', 'label']].dropna()
        
        logger.info(f"Loaded {len(df)} articles ({len(fake_df)} fake, {len(true_df)} real)")
        
        # Shuffle the data
        df = df.sample(frac=1, random_state=42).reset_index(drop=True)
        
        # Print a few examples
        logger.info("Sample data:")
        for i, row in df.head(3).iterrows():
            logger.info(f"[{row['label']}] {row['text'][:100]}...")
        
        return df
    
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        logger.info("Creating mock data for testing purposes...")
        return create_mock_data()

def create_mock_data():
    """Create mock data for testing when actual dataset is not available."""
    logger.info("Creating mock dataset with synthetic examples")
    
    # Create synthetic examples of fake and real news
    fake_examples = [
        "BREAKING: Scientist discovers that vaccines cause autism! Government hiding the truth!",
        "You won't believe what this celebrity did! Shocking revelation changes everything!",
        "SECRET NASA images reveal alien structures on Mars! Cover-up exposed!",
        "CONFIRMED: Politician caught in massive fraud scheme worth billions!",
        "Doctors don't want you to know this one simple trick to cure all diseases!"
    ]
    
    real_examples = [
        "New study shows correlation between exercise and improved mental health.",
        "City council approves budget for infrastructure improvements starting next month.",
        "Scientists publish findings on climate change effects in peer-reviewed journal.",
        "Stock market shows modest gains following Federal Reserve announcement.",
        "Local community organizes food drive to support families affected by recent storm."
    ]
    
    # Create dataframe
    data = {
        'text': fake_examples + real_examples,
        'label': ['FAKE'] * len(fake_examples) + ['REAL'] * len(real_examples)
    }
    
    df = pd.DataFrame(data)
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)  # Shuffle
    
    logger.info(f"Created mock dataset with {len(df)} examples")
    return df

def process_data(df):
    """
    Preprocess the text data with improved method.
    
    Args:
        df (pd.DataFrame): Input dataframe with 'text' column
        
    Returns:
        pd.DataFrame: Dataframe with processed text
    """
    logger.info("Preprocessing text data...")
    
    start_time = time.time()
    
    # Apply improved preprocessing to the text
    df['processed_text'] = df['text'].apply(lambda x: preprocess_text(x, 
                                                                      handle_negation=True, 
                                                                      remove_stopwords=True, 
                                                                      lemmatize=True))
    
    elapsed_time = time.time() - start_time
    logger.info(f"Preprocessing completed in {elapsed_time:.2f} seconds")
    
    # Show a before/after example
    sample_idx = 0
    logger.info(f"Preprocessing example:")
    logger.info(f"Original: {df.iloc[sample_idx]['text'][:100]}...")
    logger.info(f"Processed: {df.iloc[sample_idx]['processed_text'][:100]}...")
    
    return df

def evaluate_model(model, X_test, y_test, feature_names=None, class_names=None):
    """
    Evaluate the model and generate visualizations.
    
    Args:
        model: Trained model
        X_test: Test features
        y_test: Test labels
        feature_names: Names of features (for feature importance)
        class_names: Names of classes
        
    Returns:
        dict: Dictionary of evaluation metrics
    """
    # Make predictions
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else None
    
    # Classification metrics
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, output_dict=True)
    cm = confusion_matrix(y_test, y_pred)
    
    logger.info(f"Model Accuracy: {accuracy:.4f}")
    logger.info("Classification Report:")
    logger.info(classification_report(y_test, y_pred))
    
    # Plot confusion matrix
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=class_names, 
                yticklabels=class_names)
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title('Confusion Matrix')
    plt.savefig(os.path.join(FIGURES_DIR, 'confusion_matrix.png'))
    
    # Plot ROC curve if probability estimates are available
    if y_prob is not None:
        fpr, tpr, _ = roc_curve(y_test == class_names[1], y_prob)
        roc_auc = auc(fpr, tpr)
        
        plt.figure(figsize=(8, 6))
        plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver Operating Characteristic')
        plt.legend(loc="lower right")
        plt.savefig(os.path.join(FIGURES_DIR, 'roc_curve.png'))
    
    # Feature importance for tree-based models
    if hasattr(model, 'feature_importances_') and feature_names:
        n_features = min(20, len(feature_names))  # Show top 20 features
        indices = np.argsort(model.feature_importances_)[-n_features:]
        
        plt.figure(figsize=(10, 8))
        plt.title('Feature Importances')
        plt.barh(range(n_features), model.feature_importances_[indices], align='center')
        plt.yticks(range(n_features), [feature_names[i] for i in indices])
        plt.xlabel('Relative Importance')
        plt.savefig(os.path.join(FIGURES_DIR, 'feature_importance.png'))
    
    return {
        'accuracy': accuracy,
        'report': report,
        'confusion_matrix': cm
    }

def train_model(df):
    """
    Train an improved fake news detection model with feature engineering and model selection.
    
    Args:
        df (pd.DataFrame): Dataframe with 'processed_text' and 'label' columns
        
    Returns:
        tuple: (trained model, vectorizer, feature names)
    """
    logger.info("Training improved model...")
    
    # Split data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        df['processed_text'], 
        df['label'], 
        test_size=0.2, 
        random_state=42,
        stratify=df['label']  # Ensure balanced classes in both splits
    )
    
    # Extract raw text for feature extraction
    train_raw_text = df.loc[X_train.index, 'text'].values
    test_raw_text = df.loc[X_test.index, 'text'].values
    
    logger.info(f"Training set size: {len(X_train)}, Test set size: {len(X_test)}")
    logger.info(f"Class distribution in training set: {pd.Series(y_train).value_counts().to_dict()}")
    
    # Create a pipeline with TF-IDF vectorizer and additional text features
    pipeline = Pipeline([
        ('features', FeatureUnion([
            ('tfidf', Pipeline([
                ('vectorizer', TfidfVectorizer(
                    max_features=5000,
                    min_df=5,
                    max_df=0.7,
                    ngram_range=(1, 2)
                ))
            ])),
            ('text_features', Pipeline([
                ('extractor', TextFeaturesExtractor()),
                ('scaler', StandardScaler())
            ]))
        ])),
        ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
    ])
    
    # Define parameter grid for GridSearchCV
    param_grid = {
        'features__tfidf__vectorizer__max_features': [3000, 5000],
        'features__tfidf__vectorizer__ngram_range': [(1, 1), (1, 2)],
        'classifier__n_estimators': [50, 100],
        'classifier__max_depth': [None, 20]
    }
    
    # Use GridSearchCV for parameter tuning
    logger.info("Performing grid search for hyperparameter tuning...")
    grid_search = GridSearchCV(
        pipeline,
        param_grid=param_grid,
        cv=3,
        n_jobs=-1,
        verbose=1,
        scoring='f1'
    )
    
    # Fit the grid search on combined raw texts and extracted features
    grid_search.fit(X_train, y_train)
    
    logger.info(f"Best parameters: {grid_search.best_params_}")
    logger.info(f"Best cross-validation score: {grid_search.best_score_:.4f}")
    
    # Get the best model
    best_model = grid_search.best_estimator_
    
    # Extract feature names if possible for visualization
    try:
        tfidf_step = best_model.named_steps['features'].transformer_list[0][1]
        vectorizer = tfidf_step.named_steps['vectorizer']
        feature_names = vectorizer.get_feature_names_out()
    except:
        logger.warning("Couldn't extract feature names for visualization")
        feature_names = None
    
    # Evaluate the model
    logger.info("Evaluating model on test set...")
    class_names = ['FAKE', 'REAL']
    evaluation = evaluate_model(best_model, X_test, y_test, feature_names, class_names)
    
    # Save the best model
    model_path = os.path.join(MODELS_DIR, 'improved_fake_news_model.pkl')
    joblib.dump(best_model, model_path)
    logger.info(f"Best model saved to {model_path}")
    
    return best_model, evaluation

def main():
    """Main function to execute the improved training pipeline."""
    try:
        # Ensure NLTK data is downloaded
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('wordnet')
        nltk.download('omw-1.4')
        
        # Create mock data
        logger.info("Starting the improved model training pipeline...")
        
        # Load data
        df = load_data()
        if df.empty:
            logger.error("Empty dataset returned. Cannot proceed with training.")
            return
        
        # Process data
        processed_df = process_data(df)
        
        # Train and evaluate model
        model, evaluation = train_model(processed_df)
        
        logger.info("Improved training pipeline completed successfully!")
        logger.info(f"Final model accuracy: {evaluation['accuracy']:.4f}")
        
    except Exception as e:
        logger.error(f"Error in training pipeline: {e}", exc_info=True)

if __name__ == "__main__":
    main() 