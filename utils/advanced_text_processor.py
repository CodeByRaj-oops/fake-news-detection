import re
import string
from typing import Dict, Any, List, Tuple, Optional
import math

# Import the improved text processor
from utils.text_processor import preprocess_text, analyze_text_features, detect_clickbait

# Language detection patterns (simplified version)
LANGUAGE_PATTERNS = {
    'en': {
        'common_words': ['the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'it'],
        'unique_chars': set(),
        'common_ngrams': ['th', 'he', 'in', 'er', 'an', 're', 'on', 'at', 'en', 'nd']
    },
    'es': {
        'common_words': ['el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'ser', 'se'],
        'unique_chars': {'ñ', 'á', 'é', 'í', 'ó', 'ú', '¿', '¡'},
        'common_ngrams': ['de', 'en', 'la', 'el', 'qu', 'es', 'ar', 'ue', 'os', 'as']
    },
    'fr': {
        'common_words': ['le', 'la', 'de', 'et', 'à', 'en', 'un', 'être', 'avoir', 'que'],
        'unique_chars': {'ç', 'é', 'â', 'ê', 'î', 'ô', 'û', 'ë', 'ï', 'ü'},
        'common_ngrams': ['le', 'de', 'es', 'en', 'on', 'nt', 'qu', 're', 'an', 'la']
    },
    'de': {
        'common_words': ['der', 'die', 'das', 'und', 'zu', 'in', 'den', 'ist', 'von', 'nicht'],
        'unique_chars': {'ä', 'ö', 'ü', 'ß'},
        'common_ngrams': ['en', 'er', 'ch', 'de', 'ei', 'in', 'te', 'nd', 'ie', 'ge']
    }
}

# Language names
LANGUAGE_NAMES = {
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German'
}

def detect_language(text: str) -> Dict[str, Any]:
    """
    Detect the language of the input text
    
    Args:
        text (str): Input text
        
    Returns:
        Dict[str, Any]: Dictionary with detected language and confidence
    """
    if not text or len(text) < 10:
        return {
            "language_code": "un",
            "language_name": "Unknown",
            "confidence": 0.0
        }
    
    # Normalize text
    normalized_text = text.lower()
    
    # Calculate scores for each language
    scores = {}
    
    for lang_code, patterns in LANGUAGE_PATTERNS.items():
        # Initialize score
        scores[lang_code] = 0.0
        
        # Check common words
        words = re.findall(r'\b\w+\b', normalized_text)
        common_word_count = sum(1 for word in words if word in patterns['common_words'])
        scores[lang_code] += common_word_count * 10
        
        # Check unique characters
        unique_char_count = sum(1 for char in normalized_text if char in patterns['unique_chars'])
        scores[lang_code] += unique_char_count * 5
        
        # Check common n-grams
        ngram_count = 0
        for ngram in patterns['common_ngrams']:
            ngram_count += normalized_text.count(ngram)
        scores[lang_code] += ngram_count
    
    # Determine the most likely language
    if not scores:
        return {
            "language_code": "un",
            "language_name": "Unknown",
            "confidence": 0.0
        }
    
    # Get the language with the highest score
    most_likely_lang = max(scores, key=scores.get)
    total_score = sum(scores.values())
    
    if total_score == 0:
        confidence = 0.0
    else:
        confidence = scores[most_likely_lang] / total_score
    
    return {
        "language_code": most_likely_lang,
        "language_name": LANGUAGE_NAMES.get(most_likely_lang, "Unknown"),
        "confidence": min(1.0, confidence)
    }

def extract_entities(text: str) -> Dict[str, Any]:
    """
    Extract entities from text (simplified version without NER)
    
    Args:
        text (str): Input text
        
    Returns:
        Dict[str, Any]: Dictionary with entity counts
    """
    # This is a simplified version without proper NER
    # A real implementation would use a proper NER library
    
    # Initialize entity types
    entities = {
        "PERSON": 0,
        "ORGANIZATION": 0,
        "LOCATION": 0,
        "DATE": 0,
        "MONEY": 0
    }
    
    # Some very basic pattern matching (extremely simplified)
    
    # Persons - words with capital letters not at start of sentences
    sentences = re.split(r'[.!?]+', text)
    for sentence in sentences:
        words = sentence.strip().split()
        if len(words) > 1:  # Skip the first word which is often capitalized
            for word in words[1:]:
                if re.match(r'^[A-Z][a-z]+$', word) and len(word) > 1:
                    entities["PERSON"] += 1
    
    # Organizations - acronyms
    orgs = re.findall(r'\b[A-Z]{2,}\b', text)
    entities["ORGANIZATION"] = len(orgs)
    
    # Locations - simplified rule-based detection
    location_indicators = ["in", "at", "near", "from"]
    for indicator in location_indicators:
        pattern = r'\b' + indicator + r' ([A-Z][a-z]+)\b'
        locations = re.findall(pattern, text)
        entities["LOCATION"] += len(locations)
    
    # Dates - simplified pattern matching
    date_patterns = [
        r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',  # 01/01/2020
        r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}(st|nd|rd|th)?,?\s+\d{4}\b'  # January 1st, 2020
    ]
    
    for pattern in date_patterns:
        dates = re.findall(pattern, text, re.IGNORECASE)
        entities["DATE"] += len(dates)
    
    # Money - simplified pattern matching
    money_patterns = [
        r'\$\d+([,.]\d+)?',  # $100 or $100.00
        r'\d+ dollars'  # 100 dollars
    ]
    
    for pattern in money_patterns:
        money = re.findall(pattern, text, re.IGNORECASE)
        entities["MONEY"] += len(money)
    
    return {
        "entities": entities,
        "total_entities": sum(entities.values())
    }

def calculate_readability_metrics(text: str) -> Dict[str, float]:
    """
    Calculate readability metrics for the text
    
    Args:
        text (str): Input text
        
    Returns:
        Dict[str, float]: Dictionary with readability metrics
    """
    if not text:
        return {
            "flesch_reading_ease": 0.0,
            "flesch_kincaid_grade": 0.0,
            "smog_index": 0.0,
            "coleman_liau_index": 0.0,
            "automated_readability_index": 0.0,
            "average_grade_level": 0.0
        }
    
    # Count sentences, words, and syllables
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    sentence_count = len(sentences)
    
    words = re.findall(r'\b\w+\b', text.lower())
    word_count = len(words)
    
    if sentence_count == 0 or word_count == 0:
        return {
            "flesch_reading_ease": 0.0,
            "flesch_kincaid_grade": 0.0,
            "smog_index": 0.0,
            "coleman_liau_index": 0.0,
            "automated_readability_index": 0.0,
            "average_grade_level": 0.0
        }
    
    # Count syllables (simplified)
    def count_syllables(word: str) -> int:
        word = word.lower()
        # Count vowel groups
        count = len(re.findall(r'[aeiouy]+', word))
        # Adjust for common patterns
        if word.endswith('e'):
            count -= 1
        if word.endswith('le') and len(word) > 2 and word[-3] not in 'aeiouy':
            count += 1
        # Ensure at least one syllable per word
        return max(1, count)
    
    syllable_count = sum(count_syllables(word) for word in words)
    complex_words = sum(1 for word in words if count_syllables(word) >= 3)
    
    # Calculate Flesch Reading Ease
    # Higher score = easier to read (90-100: Very easy, 0-30: Very difficult)
    flesch_reading_ease = 206.835 - (1.015 * (word_count / sentence_count)) - (84.6 * (syllable_count / word_count))
    flesch_reading_ease = max(0, min(100, flesch_reading_ease))
    
    # Calculate Flesch-Kincaid Grade Level
    # Result approximates US grade level needed to comprehend
    flesch_kincaid_grade = 0.39 * (word_count / sentence_count) + 11.8 * (syllable_count / word_count) - 15.59
    flesch_kincaid_grade = max(0, flesch_kincaid_grade)
    
    # Calculate SMOG Index
    # Result approximates years of education needed to understand
    smog_index = 1.043 * math.sqrt((complex_words * (30 / sentence_count)) + 3.1291)
    smog_index = max(0, smog_index)
    
    # Calculate Coleman-Liau Index
    # Also approximates US grade level
    avg_letters_per_100_words = ((sum(len(word) for word in words) / word_count) * 100)
    avg_sentences_per_100_words = (sentence_count / word_count) * 100
    coleman_liau_index = 0.0588 * avg_letters_per_100_words - 0.296 * avg_sentences_per_100_words - 15.8
    coleman_liau_index = max(0, coleman_liau_index)
    
    # Calculate Automated Readability Index
    # Also approximates US grade level
    char_count = sum(len(word) for word in words)
    automated_readability_index = 4.71 * (char_count / word_count) + 0.5 * (word_count / sentence_count) - 21.43
    automated_readability_index = max(0, automated_readability_index)
    
    # Calculate average grade level
    average_grade_level = (flesch_kincaid_grade + smog_index + coleman_liau_index + automated_readability_index) / 4
    
    return {
        "flesch_reading_ease": flesch_reading_ease,
        "flesch_kincaid_grade": flesch_kincaid_grade,
        "smog_index": smog_index,
        "coleman_liau_index": coleman_liau_index,
        "automated_readability_index": automated_readability_index,
        "average_grade_level": average_grade_level
    }

def analyze_text_uniqueness(text: str) -> Dict[str, Any]:
    """
    Analyze text for uniqueness features
    
    Args:
        text (str): Input text
        
    Returns:
        Dict[str, Any]: Dictionary with uniqueness metrics
    """
    # Preprocess text
    processed = preprocess_text(text, lowercase=True, remove_stopwords=True)
    
    # Split into words
    words = processed.split()
    total_words = len(words)
    
    if total_words == 0:
        return {
            "lexical_diversity": 0.0,
            "content_density": 0.0,
            "uniqueness_score": 0.0
        }
    
    # Calculate lexical diversity (type-token ratio)
    unique_words = set(words)
    lexical_diversity = len(unique_words) / total_words
    
    # Calculate content density
    # Content words typically include nouns, verbs, adjectives, and adverbs
    # This is a simplified approximation using word length as a proxy
    content_words = [word for word in words if len(word) > 3]
    content_density = len(content_words) / max(1, total_words)
    
    # Calculate overall uniqueness score
    uniqueness_score = (lexical_diversity * 0.6) + (content_density * 0.4)
    
    return {
        "lexical_diversity": lexical_diversity,
        "content_density": content_density,
        "uniqueness_score": uniqueness_score,
        "unique_word_count": len(unique_words),
        "total_words": total_words
    }

def detect_propaganda_techniques(text: str) -> Dict[str, Any]:
    """
    Detect potential propaganda techniques in text
    
    Args:
        text (str): Input text
        
    Returns:
        Dict[str, Any]: Dictionary with propaganda techniques scores
    """
    text_lower = text.lower()
    
    # Initialize propaganda techniques
    techniques = {
        "name_calling": 0,
        "glittering_generality": 0,
        "transfer": 0,
        "testimonial": 0,
        "plain_folks": 0,
        "bandwagon": 0,
        "fear": 0,
        "loaded_language": 0
    }
    
    # Name calling - derogatory terms
    name_calling_terms = [
        "fake", "phony", "corrupt", "radical", "traitor", "conspiracy", 
        "disgrace", "stupid", "idiot", "dumb", "failure", "dangerous"
    ]
    
    for term in name_calling_terms:
        count = len(re.findall(r'\b' + term + r'\b', text_lower))
        techniques["name_calling"] += count
    
    # Glittering generality - positive emotional terms
    glittering_terms = [
        "freedom", "patriot", "justice", "truth", "love", "peace", 
        "hope", "change", "progress", "unity", "best", "greatest"
    ]
    
    for term in glittering_terms:
        count = len(re.findall(r'\b' + term + r'\b', text_lower))
        techniques["glittering_generality"] += count
    
    # Transfer - associating with symbols/institutions
    transfer_terms = [
        "flag", "nation", "country", "constitution", "founding fathers", 
        "god", "bible", "faith", "science", "expert", "studies"
    ]
    
    for term in transfer_terms:
        count = len(re.findall(r'\b' + term + r'\b', text_lower))
        techniques["transfer"] += count
    
    # Testimonial - quotes or endorsements
    testimonial_patterns = [
        r'"[^"]*"',  # Text in quotes
        r'according to',  # Attribution
        r'said that'  # Reported speech
    ]
    
    for pattern in testimonial_patterns:
        count = len(re.findall(pattern, text_lower))
        techniques["testimonial"] += count
    
    # Plain folks - ordinary people language
    plain_folks_terms = [
        "ordinary", "common", "everyday", "working class", "average joe",
        "regular people", "folks", "community", "neighbor", "family values"
    ]
    
    for term in plain_folks_terms:
        count = len(re.findall(r'\b' + term + r'\b', text_lower))
        techniques["plain_folks"] += count
    
    # Bandwagon - everyone is doing it
    bandwagon_patterns = [
        r'\beveryone\b', r'\bpeople are\b', r'\bmost people\b',
        r'\bmany\b', r'\bcrowd\b', r'\bmajority\b', r'\btrend\b'
    ]
    
    for pattern in bandwagon_patterns:
        count = len(re.findall(pattern, text_lower))
        techniques["bandwagon"] += count
    
    # Fear - creating anxiety
    fear_terms = [
        "threat", "danger", "crisis", "fear", "urgent", "emergency",
        "catastrophe", "disaster", "collapse", "invasion", "attack"
    ]
    
    for term in fear_terms:
        count = len(re.findall(r'\b' + term + r'\b', text_lower))
        techniques["fear"] += count
    
    # Loaded language - emotional words
    loaded_terms = [
        "shocking", "outrageous", "explosive", "bombshell", "devastating",
        "dramatic", "terrifying", "horrific", "astonishing", "unbelievable"
    ]
    
    for term in loaded_terms:
        count = len(re.findall(r'\b' + term + r'\b', text_lower))
        techniques["loaded_language"] += count
    
    # Calculate overall propaganda score
    total_count = sum(techniques.values())
    word_count = len(text_lower.split())
    
    if word_count == 0:
        propaganda_score = 0
    else:
        # Normalized score from 0-100
        propaganda_score = min(100, (total_count / word_count) * 100)
    
    return {
        "techniques": techniques,
        "total_techniques": total_count,
        "propaganda_score": propaganda_score
    }

def comprehensive_text_analysis(text: str) -> Dict[str, Any]:
    """
    Perform comprehensive analysis of text including all enhanced features
    
    Args:
        text (str): Input text
        
    Returns:
        Dict[str, Any]: Dictionary with all analysis results
    """
    if not text:
        return {
            "error": "Empty text provided"
        }
    
    try:
        result = {}
        
        # Basic text features
        result["text_features"] = analyze_text_features(text)
        
        # Clickbait detection
        result["clickbait"] = detect_clickbait(text)
        
        # Language detection
        result["language"] = detect_language(text)
        
        # Entity extraction
        result["entities"] = extract_entities(text)
        
        # Readability metrics
        result["readability"] = calculate_readability_metrics(text)
        
        # Text uniqueness
        result["uniqueness"] = analyze_text_uniqueness(text)
        
        # Propaganda techniques
        result["propaganda"] = detect_propaganda_techniques(text)
        
        # Add processed text
        result["processed_text"] = preprocess_text(text)
        
        return result
    except Exception as e:
        return {
            "error": f"Analysis failed: {str(e)}"
        } 