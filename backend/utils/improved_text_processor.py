#!/usr/bin/env python3
"""
Advanced text preprocessing and feature extraction for fake news detection.
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

# Download necessary NLTK data
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('omw-1.4')

# Load stopwords
STOP_WORDS = set(stopwords.words('english'))

# Add custom fake news related keywords that should never be removed
CUSTOM_KEEP_WORDS = {
    'not', 'no', 'never', 'none', 'nobody', 'nothing', 'nowhere',
    'fake', 'hoax', 'lie', 'conspiracy', 'truth', 'false', 'real',
    'allegedly', 'reportedly', 'supposedly', 'claim', 'source'
}

# Remove these words from stopwords
STOP_WORDS = STOP_WORDS - CUSTOM_KEEP_WORDS

# Clickbait and sensationalist phrases often found in fake news
CLICKBAIT_PHRASES = [
    'you won\'t believe', 'shocking', 'mind blowing', 'amazing', 
    'unbelievable', 'incredible', 'won\'t believe your eyes',
    'shocking truth', 'what happens next', 'secret', 'reveal',
    'exclusive', 'the truth about', 'they don\'t want you to know',
    'conspiracy'
]

# URL regex pattern
URL_PATTERN = re.compile(r'https?://\S+|www\.\S+')

# Email regex pattern
EMAIL_PATTERN = re.compile(r'\S+@\S+')

def preprocess_text(text, handle_negation=True, remove_stopwords=True, lemmatize=True):
    """
    Preprocess text with advanced techniques.
    
    Args:
        text (str): Input text
        handle_negation (bool): Whether to handle negation (e.g., "not good" -> "not_good")
        remove_stopwords (bool): Whether to remove stopwords
        lemmatize (bool): Whether to lemmatize tokens
        
    Returns:
        str: Preprocessed text
    """
    if not isinstance(text, str) or not text.strip():
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove URLs
    text = URL_PATTERN.sub(' url ', text)
    
    # Remove emails
    text = EMAIL_PATTERN.sub(' email ', text)
    
    # Remove HTML tags
    text = re.sub(r'<.*?>', ' ', text)
    
    # Replace numbers with token
    text = re.sub(r'\d+', ' number ', text)
    
    # Tokenize
    tokens = word_tokenize(text)
    
    # Lemmatize if requested
    if lemmatize:
        lemmatizer = WordNetLemmatizer()
        tokens = [lemmatizer.lemmatize(token) for token in tokens]
    
    # Handle negation if requested (convert "not good" to "not_good")
    if handle_negation:
        tokens = handle_text_negation(tokens)
    
    # Remove stopwords if requested
    if remove_stopwords:
        tokens = [token for token in tokens if token not in STOP_WORDS]
    
    # Remove punctuation
    tokens = [token for token in tokens if token not in string.punctuation]
    
    # Rejoin tokens
    processed_text = ' '.join(tokens)
    
    return processed_text

def handle_text_negation(tokens):
    """
    Handle negation in text by joining negation words with the following words.
    Example: "not good" -> "not_good"
    
    Args:
        tokens (list): List of tokens
        
    Returns:
        list: List of tokens with negation handled
    """
    negation_tokens = ['not', 'no', 'never', 'none', 'neither', 'nor', 'nothing']
    negation_scope = 3  # Words to consider after negation term
    
    new_tokens = []
    negation_active = False
    negation_count = 0
    
    for token in tokens:
        if token in negation_tokens:
            negation_active = True
            negation_count = 0
            new_tokens.append(token)
        elif negation_active and negation_count < negation_scope:
            # Join with underscore to preserve negation context
            new_tokens.append(f"not_{token}")
            negation_count += 1
            
            # End negation at punctuation
            if token in '.,:;!?':
                negation_active = False
        else:
            new_tokens.append(token)
            
            # End negation at punctuation
            if token in '.,:;!?' and negation_active:
                negation_active = False
    
    return new_tokens

def extract_features(text):
    """
    Extract linguistic and stylistic features from text for fake news detection.
    
    Args:
        text (str): Input raw text
        
    Returns:
        dict: Dictionary of extracted features
    """
    if not isinstance(text, str) or not text.strip():
        return {
            'word_count': 0,
            'avg_word_length': 0,
            'sentence_count': 0,
            'avg_sentence_length': 0,
            'exclamation_count': 0,
            'question_count': 0,
            'capitalized_ratio': 0,
            'clickbait_score': 0,
            'polarity': 0,
            'subjectivity': 0,
            'personal_pronouns': 0,
            'punctuation_ratio': 0
        }
    
    # Ensure text is lowercase
    text_lower = text.lower()
    
    # Word count
    words = word_tokenize(text_lower)
    word_count = len(words)
    
    # Average word length
    if word_count > 0:
        avg_word_length = sum(len(word) for word in words) / word_count
    else:
        avg_word_length = 0
    
    # Sentence count
    sentences = sent_tokenize(text)
    sentence_count = len(sentences)
    
    # Average sentence length (in words)
    if sentence_count > 0:
        avg_sentence_length = word_count / sentence_count
    else:
        avg_sentence_length = 0
    
    # Count of exclamation marks
    exclamation_count = text.count('!')
    
    # Count of question marks
    question_count = text.count('?')
    
    # Ratio of capitalized words (potential sensationalism)
    if word_count > 0:
        capitalized_words = sum(1 for word in text.split() if word.isupper() and len(word) > 1)
        capitalized_ratio = capitalized_words / word_count
    else:
        capitalized_ratio = 0
    
    # Clickbait phrases detection
    clickbait_score = 0
    for phrase in CLICKBAIT_PHRASES:
        if phrase in text_lower:
            clickbait_score += 1
    
    # Sentiment analysis (polarity and subjectivity)
    blob = TextBlob(text_lower)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    
    # Personal pronouns (often used in fake news to create connection)
    personal_pronouns = sum(1 for word in words if word.lower() in 
                            {'i', 'me', 'my', 'mine', 'myself', 
                             'we', 'us', 'our', 'ours', 'ourselves',
                             'you', 'your', 'yours', 'yourself', 'yourselves'})
    
    # Punctuation ratio (over-punctuation is common in fake news)
    if word_count > 0:
        punctuation_count = sum(1 for char in text if char in string.punctuation)
        punctuation_ratio = punctuation_count / word_count
    else:
        punctuation_ratio = 0
    
    return {
        'word_count': word_count,
        'avg_word_length': avg_word_length,
        'sentence_count': sentence_count,
        'avg_sentence_length': avg_sentence_length,
        'exclamation_count': exclamation_count,
        'question_count': question_count,
        'capitalized_ratio': capitalized_ratio,
        'clickbait_score': clickbait_score,
        'polarity': polarity,
        'subjectivity': subjectivity,
        'personal_pronouns': personal_pronouns,
        'punctuation_ratio': punctuation_ratio
    }

def get_ngram_frequencies(text, n=2):
    """
    Get n-gram frequencies from text.
    
    Args:
        text (str): Input text
        n (int): n-gram size
        
    Returns:
        dict: Dictionary with n-gram frequencies
    """
    if not isinstance(text, str) or not text.strip():
        return {}
    
    # Tokenize
    tokens = word_tokenize(text.lower())
    
    # Generate n-grams
    n_grams = list(ngrams(tokens, n))
    
    # Count n-grams
    n_gram_freq = Counter(n_grams)
    
    # Convert to dictionary with joined strings as keys
    return {' '.join(gram): count for gram, count in n_gram_freq.items()}

def analyze_writing_style(text):
    """
    Analyze writing style indicators that may help identify fake news.
    
    Args:
        text (str): Input text
        
    Returns:
        dict: Dictionary with writing style metrics
    """
    if not isinstance(text, str) or not text.strip():
        return {
            'reading_ease': 0,
            'avg_word_complexity': 0,
            'hedging_phrases': 0,
            'exaggeration_phrases': 0
        }
    
    # Tokenize
    words = word_tokenize(text.lower())
    sentences = sent_tokenize(text)
    
    # Calculate basic metrics
    word_count = len(words)
    sentence_count = len(sentences)
    
    # Syllable count estimation (simplified)
    def count_syllables(word):
        vowels = 'aeiouy'
        count = 0
        if word and word[0] in vowels:
            count += 1
        for i in range(1, len(word)):
            if word[i] in vowels and word[i-1] not in vowels:
                count += 1
        if word.endswith('e'):
            count -= 1
        if count == 0:
            count = 1
        return count
    
    syllable_count = sum(count_syllables(word) for word in words if word.isalpha())
    
    # Calculate Flesch Reading Ease score (simplified)
    if sentence_count > 0 and word_count > 0:
        reading_ease = 206.835 - 1.015 * (word_count / sentence_count) - 84.6 * (syllable_count / word_count)
    else:
        reading_ease = 0
    
    # Average word complexity (by syllable count)
    if word_count > 0:
        avg_word_complexity = syllable_count / word_count
    else:
        avg_word_complexity = 0
    
    # Hedging phrases (common in questionable content)
    hedging_phrases = ['may', 'might', 'could', 'allegedly', 'reportedly', 'some people say',
                      'sources say', 'it is claimed', 'it is believed', 'possibly', 'perhaps']
    
    hedging_count = 0
    for phrase in hedging_phrases:
        hedging_count += sum(1 for match in re.finditer(r'\b' + phrase + r'\b', text.lower()))
    
    # Exaggeration phrases
    exaggeration_phrases = ['all', 'none', 'every', 'always', 'never', 'everyone', 'nobody',
                           'definitely', 'absolutely', 'undoubtedly', 'completely']
    
    exaggeration_count = 0
    for phrase in exaggeration_phrases:
        exaggeration_count += sum(1 for match in re.finditer(r'\b' + phrase + r'\b', text.lower()))
    
    return {
        'reading_ease': reading_ease,
        'avg_word_complexity': avg_word_complexity,
        'hedging_phrases': hedging_count,
        'exaggeration_phrases': exaggeration_count
    }

# Example usage
if __name__ == "__main__":
    sample_text = """
    SHOCKING NEWS! Scientists discover that vaccines cause autism! 
    The government doesn't want YOU to know this INCREDIBLE truth. 
    According to sources close to the investigation, this conspiracy has been 
    going on for YEARS! Share this with everyone you know!!!
    """
    
    processed = preprocess_text(sample_text)
    print("Processed text:", processed)
    
    features = extract_features(sample_text)
    print("\nExtracted features:", features)
    
    writing_style = analyze_writing_style(sample_text)
    print("\nWriting style analysis:", writing_style) 