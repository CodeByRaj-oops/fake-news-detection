import re
import string
from typing import List, Dict, Any, Optional

# Stop words list
STOP_WORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", 
    "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being", 
    "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't", 
    "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during", 
    "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have", 
    "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", 
    "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", 
    "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", 
    "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", 
    "off", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", 
    "out", "over", "own", "same", "shan't", "she", "she'd", "she'll", "she's", "should", 
    "shouldn't", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", 
    "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", 
    "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up", 
    "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't", 
    "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", 
    "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd", 
    "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves"
}

def preprocess_text(text: str, remove_stopwords: bool = True, remove_punctuation: bool = True, 
                    lowercase: bool = True, remove_extra_spaces: bool = True, 
                    remove_urls: bool = True, remove_numbers: bool = False) -> str:
    """
    Enhanced text preprocessing function with multiple options
    
    Args:
        text (str): Input text to be processed
        remove_stopwords (bool): Whether to remove stopwords
        remove_punctuation (bool): Whether to remove punctuation
        lowercase (bool): Whether to convert text to lowercase
        remove_extra_spaces (bool): Whether to remove extra whitespace
        remove_urls (bool): Whether to remove URLs
        remove_numbers (bool): Whether to remove numeric values
        
    Returns:
        str: Processed text
    """
    if not text:
        return ""
    
    # Standardize text (handle different types of quotes, dashes, etc.)
    text = text.strip()
    text = re.sub(r'["""]', '"', text)  # Standardize quotes
    text = re.sub(r'[''']', "'", text)  # Standardize apostrophes
    text = re.sub(r'[–—−]', "-", text)  # Standardize dashes
    
    # Remove URLs if requested
    if remove_urls:
        text = re.sub(r'https?://\S+|www\.\S+', '', text)
        
    # Convert to lowercase if requested
    if lowercase:
        text = text.lower()
    
    # Remove numbers if requested
    if remove_numbers:
        text = re.sub(r'\d+', '', text)
    
    # Remove punctuation if requested
    if remove_punctuation:
        translator = str.maketrans('', '', string.punctuation)
        text = text.translate(translator)
    
    # Tokenize
    words = text.split()
    
    # Remove stopwords if requested
    if remove_stopwords:
        words = [word for word in words if word not in STOP_WORDS]
    
    # Rejoin words
    text = ' '.join(words)
    
    # Remove extra whitespace if requested
    if remove_extra_spaces:
        text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def analyze_text_features(text: str) -> Dict[str, Any]:
    """
    Analyze text and extract its features
    
    Args:
        text (str): Input text
        
    Returns:
        Dict[str, Any]: Dictionary with text features
    """
    # Basic text stats
    char_count = len(text)
    word_count = len(text.split())
    sentence_count = len(re.split(r'[.!?]+', text))
    
    # Preprocessed version
    processed = preprocess_text(text)
    processed_word_count = len(processed.split())
    
    # Calculate features
    avg_word_length = sum(len(word) for word in text.split()) / max(1, word_count)
    avg_sentence_length = word_count / max(1, sentence_count)
    
    # Count specific features
    exclamation_count = text.count('!')
    question_count = text.count('?')
    capital_letters = sum(1 for c in text if c.isupper())
    
    return {
        "character_count": char_count,
        "word_count": word_count,
        "sentence_count": sentence_count,
        "processed_word_count": processed_word_count,
        "avg_word_length": avg_word_length,
        "avg_sentence_length": avg_sentence_length,
        "exclamation_count": exclamation_count,
        "question_count": question_count,
        "capital_letters": capital_letters,
        "uppercase_ratio": capital_letters / max(1, char_count)
    }

def tokenize_text(text: str, min_token_length: int = 2) -> List[str]:
    """
    Tokenize text into words
    
    Args:
        text (str): Input text
        min_token_length (int): Minimum length of tokens to keep
        
    Returns:
        List[str]: List of tokens
    """
    # Preprocess text
    processed = preprocess_text(text)
    
    # Tokenize
    tokens = processed.split()
    
    # Filter by length
    tokens = [token for token in tokens if len(token) >= min_token_length]
    
    return tokens

def calculate_text_similarity(text1: str, text2: str) -> float:
    """
    Calculate similarity between two texts using Jaccard similarity
    
    Args:
        text1 (str): First text
        text2 (str): Second text
        
    Returns:
        float: Similarity score between 0 and 1
    """
    # Tokenize both texts
    tokens1 = set(tokenize_text(text1))
    tokens2 = set(tokenize_text(text2))
    
    # Calculate Jaccard similarity
    intersection = len(tokens1.intersection(tokens2))
    union = len(tokens1.union(tokens2))
    
    # Return similarity score
    return intersection / max(1, union)

def detect_clickbait(text: str) -> Dict[str, Any]:
    """
    Detect if text has clickbait characteristics
    
    Args:
        text (str): Input text
        
    Returns:
        Dict[str, Any]: Dictionary with clickbait indicators
    """
    # Common clickbait phrases
    clickbait_phrases = [
        "you won't believe", "shocking", "amazing", "incredible", "mind blowing",
        "you'll never guess", "unbelievable", "jaw-dropping", "secret", "insane",
        "revealed", "top 10", "what happens next", "this is why", "will shock you"
    ]
    
    # Convert text to lowercase for checking
    lower_text = text.lower()
    
    # Check for clickbait phrases
    phrase_matches = [phrase for phrase in clickbait_phrases if phrase in lower_text]
    
    # Check for ALL CAPS words
    words = text.split()
    all_caps_words = [word for word in words if len(word) > 2 and word.isupper()]
    
    # Check for excessive punctuation
    excessive_punctuation = bool(re.search(r'[!?]{2,}', text))
    
    # Calculate clickbait score
    clickbait_score = (
        (len(phrase_matches) * 0.2) + 
        (len(all_caps_words) / max(1, len(words)) * 0.4) + 
        (excessive_punctuation * 0.4)
    )
    
    return {
        "clickbait_score": min(1.0, clickbait_score),
        "clickbait_phrases": phrase_matches,
        "all_caps_count": len(all_caps_words),
        "excessive_punctuation": excessive_punctuation,
        "is_likely_clickbait": clickbait_score > 0.3
    } 