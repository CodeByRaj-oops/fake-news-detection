#!/usr/bin/env python3
"""
Script to download the Fake and Real News dataset from Kaggle.
Requires kaggle API credentials to be set up.
"""

import os
import zipfile
import logging
import subprocess
import sys
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(PROJECT_DIR, 'data')
os.makedirs(DATA_DIR, exist_ok=True)

# Kaggle dataset details
DATASET = "clmentbisaillon/fake-and-real-news-dataset"
DATASET_ZIP = "fake-and-real-news-dataset.zip"
DATASET_PATH = os.path.join(DATA_DIR, DATASET_ZIP)

def check_kaggle_api():
    """Check if kaggle API is installed and credentials are set up."""
    try:
        import kaggle
        return True
    except ImportError:
        logger.error("Kaggle API not found. Installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "kaggle"])
            import kaggle
            return True
        except Exception as e:
            logger.error(f"Failed to install Kaggle API: {e}")
            return False

def check_kaggle_credentials():
    """Check if Kaggle API credentials are configured."""
    kaggle_dir = os.path.join(os.path.expanduser("~"), ".kaggle")
    kaggle_json = os.path.join(kaggle_dir, "kaggle.json")
    
    if not os.path.exists(kaggle_json):
        logger.error(
            "Kaggle API credentials not found. Please set up your Kaggle API credentials:\n"
            "1. Go to your Kaggle account settings (https://www.kaggle.com/account)\n"
            "2. Click on 'Create New API Token' to download kaggle.json\n"
            "3. Place the downloaded file in ~/.kaggle/kaggle.json\n"
            "4. Run this script again"
        )
        return False
    
    return True

def download_dataset():
    """Download the dataset from Kaggle."""
    logger.info(f"Downloading dataset: {DATASET}")
    
    if os.path.exists(DATASET_PATH):
        logger.info(f"Dataset already downloaded at {DATASET_PATH}")
        return True
    
    try:
        from kaggle.api.kaggle_api_extended import KaggleApi
        api = KaggleApi()
        api.authenticate()
        
        # Download the dataset
        api.dataset_download_files(DATASET, path=DATA_DIR)
        logger.info(f"Dataset downloaded to {DATASET_PATH}")
        return True
    
    except Exception as e:
        logger.error(f"Failed to download dataset: {e}")
        
        # Provide manual download instructions
        logger.info(
            f"\nPlease download the dataset manually:\n"
            f"1. Go to https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset\n"
            f"2. Download the dataset\n"
            f"3. Extract the files to {DATA_DIR}\n"
            f"   - Ensure 'Fake.csv' and 'True.csv' are in the {DATA_DIR} directory"
        )
        return False

def extract_dataset():
    """Extract the downloaded dataset."""
    if not os.path.exists(DATASET_PATH):
        logger.error(f"Dataset zip file not found at {DATASET_PATH}")
        return False
    
    try:
        logger.info(f"Extracting {DATASET_PATH} to {DATA_DIR}")
        with zipfile.ZipFile(DATASET_PATH, 'r') as zip_ref:
            zip_ref.extractall(DATA_DIR)
        
        logger.info("Dataset extracted successfully")
        return True
    
    except Exception as e:
        logger.error(f"Failed to extract dataset: {e}")
        return False

def check_extracted_files():
    """Check if the expected files exist after extraction."""
    required_files = ["Fake.csv", "True.csv"]
    missing_files = [f for f in required_files if not os.path.exists(os.path.join(DATA_DIR, f))]
    
    if missing_files:
        logger.error(f"Missing required files after extraction: {', '.join(missing_files)}")
        return False
    
    logger.info("All required dataset files found")
    return True

def main():
    """Main function to download and extract the dataset."""
    logger.info("Starting dataset download process...")
    
    # Check if dataset files already exist
    if check_extracted_files():
        logger.info("Dataset already available. Skipping download.")
        return
    
    # Check Kaggle API and credentials
    if not check_kaggle_api() or not check_kaggle_credentials():
        logger.error("Cannot proceed with automatic download. Please follow the manual download instructions.")
        return
    
    # Download and extract dataset
    if download_dataset() and extract_dataset():
        if check_extracted_files():
            logger.info("Dataset download and extraction completed successfully!")
        else:
            logger.error("Dataset extraction completed but required files are missing.")
    else:
        logger.error("Failed to download or extract the dataset.")

if __name__ == "__main__":
    main() 