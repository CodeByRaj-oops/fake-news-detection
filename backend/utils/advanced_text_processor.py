#!/usr/bin/env python3
"""
Advanced text processing utilities with enhanced features for fake news detection.
This module extends the improved_text_processor with additional capabilities.
"""

import re
import string
import numpy as np
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.util import ngrams
from textblob import TextBlob
import langdetect
from langdetect import detect, DetectorFactory
import hashlib
import math

# Set seed for language detection to ensure consistent results
DetectorFactory.seed = 0

# Download necessary NLTK data
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
    nltk.data.find('corpora/wordnet')
    nltk.data.find('maxent_ne_chunker')
    nltk.data.find('words')
    nltk.data.find('averaged_perceptron_tagger')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('omw-1.4')
    nltk.download('maxent_ne_chunker')
    nltk.download('words')
    nltk.download('averaged_perceptron_tagger')

# Import existing utilities from improved text processor
from .improved_text_processor import (
    preprocess_text, 
    extract_features, 
    analyze_writing_style,
    get_ngram_frequencies,
    STOP_WORDS,
    CUSTOM_KEEP_WORDS,
    CLICKBAIT_PHRASES
)

def detect_language(text):
    """
    Detect the language of the input text.
    
    Args:
        text (str): Input text
    
    Returns:
        dict: Dictionary with language code, language name, and confidence
    """
    if not isinstance(text, str) or not text.strip():
        return {
            'language_code': 'unknown',
            'language_name': 'Unknown',
            'confidence': 0.0
        }
    
    try:
        # Attempt to detect language
        lang_code = detect(text)
        
        # Map language codes to names
        language_names = {
            'en': 'English',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'it': 'Italian',
            'pt': 'Portuguese',
            'ru': 'Russian',
            'ar': 'Arabic',
            'zh-cn': 'Chinese (Simplified)',
            'zh-tw': 'Chinese (Traditional)',
            'ja': 'Japanese',
            'ko': 'Korean',
            'hi': 'Hindi'
            # Add more as needed
        }
        
        lang_name = language_names.get(lang_code, f'Unknown ({lang_code})')
        
        # Note: langdetect doesn't provide confidence scores directly
        # We'd need to access internal probability distributions to get this
        return {
            'language_code': lang_code,
            'language_name': lang_name,
            'confidence': 0.95  # Placeholder for now
        }
    except langdetect.lang_detect_exception.LangDetectException:
        return {
            'language_code': 'unknown',
            'language_name': 'Unknown',
            'confidence': 0.0
        }

def extract_entities(text):
    """
    Extract named entities from text.
    
    Args:
        text (str): Input text
    
    Returns:
        dict: Dictionary with entity types and counts
    """
    if not isinstance(text, str) or not text.strip():
        return {
            'entities': {},
            'entity_count': 0
        }
    
    try:
        # Tokenize and tag parts of speech
        tokens = nltk.word_tokenize(text)
        pos_tags = nltk.pos_tag(tokens)
        
        # Extract named entities
        named_entities = nltk.ne_chunk(pos_tags)
        
        # Process the tree to extract entity types
        entity_counts = Counter()
        
        for chunk in named_entities:
            if hasattr(chunk, 'label'):
                entity_type = chunk.label()
                entity_text = ' '.join(c[0] for c in chunk)
                entity_counts[entity_type] += 1
        
        return {
            'entities': {k: v for k, v in entity_counts.items()},
            'entity_count': sum(entity_counts.values())
        }
    except Exception as e:
        print(f"Error extracting entities: {e}")
        return {
            'entities': {},
            'entity_count': 0
        }

def calculate_readability_metrics(text):
    """
    Calculate readability metrics for the text.
    
    Args:
        text (str): Input text
    
    Returns:
        dict: Dictionary with readability metrics
    """
    if not isinstance(text, str) or not text.strip():
        return {
            'flesch_reading_ease': 0,
            'flesch_kincaid_grade': 0,
            'gunning_fog': 0,
            'smog_index': 0,
            'coleman_liau_index': 0,
            'automated_readability_index': 0,
            'average_grade_level': 0
        }
    
    # Tokenize text
    sentences = sent_tokenize(text)
    words = word_tokenize(text)
    
    # Filter out non-words
    words = [word for word in words if any(c.isalpha() for c in word)]
    
    # Count numbers
    num_sentences = len(sentences)
    num_words = len(words)
    
    if num_sentences == 0 or num_words == 0:
        return {
            'flesch_reading_ease': 0,
            'flesch_kincaid_grade': 0,
            'gunning_fog': 0,
            'smog_index': 0,
            'coleman_liau_index': 0,
            'automated_readability_index': 0,
            'average_grade_level': 0
        }
    
    # Count syllables (simple approximation)
    def count_syllables(word):
        word = word.lower()
        if len(word) <= 3:
            return 1
            
        # Remove e from the end
        if word.endswith('e'):
            word = word[:-1]
            
        # Count vowel groups
        vowels = 'aeiouy'
        count = 0
        in_vowel_group = False
        
        for char in word:
            if char in vowels:
                if not in_vowel_group:
                    count += 1
                    in_vowel_group = True
            else:
                in_vowel_group = False
                
        # Ensure at least one syllable
        return max(1, count)
    
    # Count total syllables
    total_syllables = sum(count_syllables(word) for word in words)
    
    # Count complex words (words with 3+ syllables)
    complex_words = [word for word in words if count_syllables(word) >= 3]
    complex_word_count = len(complex_words)
    
    # Calculate character count
    character_count = sum(len(word) for word in words)
    
    # 1. Flesch Reading Ease
    flesch_reading_ease = 206.835 - 1.015 * (num_words / num_sentences) - 84.6 * (total_syllables / num_words)
    
    # 2. Flesch-Kincaid Grade Level
    flesch_kincaid_grade = 0.39 * (num_words / num_sentences) + 11.8 * (total_syllables / num_words) - 15.59
    
    # 3. Gunning Fog Index
    gunning_fog = 0.4 * ((num_words / num_sentences) + 100 * (complex_word_count / num_words))
    
    # 4. SMOG Index (simplified formula)
    smog_index = 1.043 * math.sqrt(complex_word_count * (30 / num_sentences)) + 3.1291
    
    # 5. Coleman-Liau Index
    L = (character_count / num_words) * 100  # Average number of characters per 100 words
    S = (num_sentences / num_words) * 100  # Average number of sentences per 100 words
    coleman_liau_index = 0.0588 * L - 0.296 * S - 15.8
    
    # 6. Automated Readability Index
    automated_readability_index = 4.71 * (character_count / num_words) + 0.5 * (num_words / num_sentences) - 21.43
    
    # 7. Average Grade Level
    grade_levels = [
        flesch_kincaid_grade,
        gunning_fog,
        smog_index,
        coleman_liau_index, 
        automated_readability_index
    ]
    average_grade_level = sum(grade_levels) / len(grade_levels)
    
    return {
        'flesch_reading_ease': round(flesch_reading_ease, 2),
        'flesch_kincaid_grade': round(flesch_kincaid_grade, 2),
        'gunning_fog': round(gunning_fog, 2),
        'smog_index': round(smog_index, 2),
        'coleman_liau_index': round(coleman_liau_index, 2),
        'automated_readability_index': round(automated_readability_index, 2),
        'average_grade_level': round(average_grade_level, 2)
    }

def calculate_text_uniqueness(text):
    """
    Calculate metrics related to text uniqueness and originality.
    
    Args:
        text (str): Input text
    
    Returns:
        dict: Dictionary with uniqueness metrics
    """
    if not isinstance(text, str) or not text.strip():
        return {
            'unique_words_ratio': 0,
            'lexical_diversity': 0,
            'content_hash': "",
        }
        
    # Tokenize and clean
    words = word_tokenize(text.lower())
    words = [word for word in words if word.isalpha()]
    
    if not words:
        return {
            'unique_words_ratio': 0,
            'lexical_diversity': 0,
            'content_hash': hashlib.md5(text.encode()).hexdigest(),
        }
    
    # Count words and unique words
    word_count = len(words)
    unique_words = set(words)
    unique_word_count = len(unique_words)
    
    # Calculate lexical diversity (type-token ratio)
    lexical_diversity = unique_word_count / word_count if word_count > 0 else 0
    
    # Calculate unique words ratio
    unique_words_ratio = unique_word_count / word_count if word_count > 0 else 0
    
    # Generate content hash (useful for duplicate detection)
    content_hash = hashlib.md5(text.encode()).hexdigest()
    
    return {
        'unique_words_ratio': round(unique_words_ratio, 4),
        'lexical_diversity': round(lexical_diversity, 4),
        'content_hash': content_hash,
    }

def detect_propaganda_techniques(text):
    """
    Detect common propaganda techniques in text.
    
    Args:
        text (str): Input text
    
    Returns:
        dict: Dictionary with propaganda techniques and scores
    """
    if not isinstance(text, str) or not text.strip():
        return {
            'techniques': {},
            'propaganda_score': 0
        }
    
    text_lower = text.lower()
    
    # Define propaganda techniques and their associated phrases/patterns
    propaganda_techniques = {
        'name_calling': [
            'radical', 'terrorist', 'thug', 'communist', 'socialist', 'fascist', 
            'snowflake', 'libtard', 'sheep', 'nazi', 'extremist', 'cult'
        ],
        'glittering_generalities': [
            'freedom', 'patriotic', 'family values', 'fairness', 'democracy', 
            'rights', 'truth', 'justice', 'love', 'peace'
        ],
        'transfer': [
            'experts say', 'scientists found', 'according to research', 
            'studies show', 'doctors recommend'
        ],
        'testimonial': [
            'endorsed by', 'supported by', 'according to', 'as stated by',
            'as mentioned by', 'as shown by'
        ],
        'plain_folks': [
            'common sense', 'regular people', 'ordinary citizens', 'everyday',
            'working class', 'main street', 'real americans'
        ],
        'card_stacking': [
            'what they don\'t want you to know', 'what they\'re hiding', 
            'the truth about', 'what they won\'t tell you', 'the real truth'
        ],
        'bandwagon': [
            'everyone is', 'people are saying', 'trending', 'going viral', 
            'popular opinion', 'the consensus is', 'everybody knows'
        ],
        'fear': [
            'warning', 'danger', 'threat', 'terror', 'alarming', 'frightening',
            'scary', 'beware', 'urgent', 'crisis', 'emergency', 'panic'
        ],
        'black_and_white_fallacy': [
            'either', 'or', 'versus', 'against', 'with us or against us',
            'only choice', 'no alternative', 'black and white'
        ],
        'exaggeration': [
            'best ever', 'worst ever', 'greatest', 'perfect', 'absolutely',
            'completely', 'totally', 'undoubtedly', 'incredible'
        ]
    }
    
    # Count technique occurrences
    technique_counts = {}
    for technique, phrases in propaganda_techniques.items():
        count = 0
        for phrase in phrases:
            count += len(re.findall(r'\b' + re.escape(phrase) + r'\b', text_lower))
        if count > 0:
            technique_counts[technique] = count
    
    # Calculate overall propaganda score (normalized by text length)
    total_count = sum(technique_counts.values())
    word_count = len(word_tokenize(text))
    propaganda_score = (total_count / (word_count + 1)) * 100  # +1 to avoid division by zero
    
    return {
        'techniques': technique_counts,
        'propaganda_score': round(min(propaganda_score, 100), 2)  # Cap at 100%
    }

def comprehensive_text_analysis(text):
    """
    Perform comprehensive analysis of text for fake news detection.
    Combines all analysis features into a single function.
    
    Args:
        text (str): Input text
    
    Returns:
        dict: Comprehensive analysis results
    """
    if not isinstance(text, str) or not text.strip():
        return {
            'error': 'Invalid or empty text'
        }
    
    # Process text
    processed_text = preprocess_text(text)
    
    # Language detection
    language_info = detect_language(text)
    
    # Basic feature extraction (from improved_text_processor)
    basic_features = extract_features(text)
    
    # Writing style analysis (from improved_text_processor)
    style_analysis = analyze_writing_style(text)
    
    # Entity extraction
    entity_info = extract_entities(text)
    
    # Readability metrics
    readability = calculate_readability_metrics(text)
    
    # Text uniqueness
    uniqueness = calculate_text_uniqueness(text)
    
    # Propaganda techniques
    propaganda = detect_propaganda_techniques(text)
    
    # Combine all results
    return {
        'processed_text': processed_text,
        'language': language_info,
        'basic_features': basic_features,
        'writing_style': style_analysis,
        'entities': entity_info,
        'readability': readability,
        'uniqueness': uniqueness,
        'propaganda': propaganda
    }

# Example usage
if __name__ == "__main__":
    sample_text = """
    SHOCKING NEWS! Scientists discover that vaccines cause autism!
    The government doesn't want YOU to know this INCREDIBLE truth.
    According to sources close to the investigation, this conspiracy has been
    going on for YEARS! Share this with everyone you know!!!
    """

    result = comprehensive_text_analysis(sample_text)
    import json
    print(json.dumps(result, indent=2)) 