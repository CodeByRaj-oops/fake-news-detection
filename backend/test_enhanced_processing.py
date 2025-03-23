#!/usr/bin/env python3
"""
Test script to demonstrate the enhanced text processing features.
"""

import os
import sys
import json
from pprint import pprint

# Add parent directory to path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)

# Import text processing utilities
from utils.advanced_text_processor import (
    detect_language,
    extract_entities,
    calculate_readability_metrics,
    calculate_text_uniqueness,
    detect_propaganda_techniques,
    comprehensive_text_analysis
)

# Import enhanced detector
from enhanced_predict import EnhancedFakeNewsDetector

def print_separator(title):
    """Print a separator with title."""
    print("\n" + "=" * 80)
    print(f" {title} ".center(80, "="))
    print("=" * 80 + "\n")

def print_json(data):
    """Print data as formatted JSON."""
    print(json.dumps(data, indent=2))

def test_language_detection():
    """Test language detection feature."""
    print_separator("LANGUAGE DETECTION")
    
    samples = {
        "english": "This is a sample text in English language for testing purposes.",
        "spanish": "Este es un texto de muestra en español para propósitos de prueba.",
        "french": "Ceci est un exemple de texte en français à des fins de test.",
        "german": "Dies ist ein Beispieltext in deutscher Sprache für Testzwecke.",
        "mixed": "This is English. Pero aquí hay algo de español. Et aussi du français."
    }
    
    for lang, text in samples.items():
        print(f"Sample ({lang}):")
        print(f"  \"{text}\"")
        result = detect_language(text)
        print(f"  Detected: {result['language_name']} ({result['language_code']}) with confidence {result['confidence']}")
        print()

def test_entity_extraction():
    """Test entity extraction feature."""
    print_separator("ENTITY EXTRACTION")
    
    text = """
    The President of the United States, Joe Biden, visited Berlin, Germany last week 
    where he met with Chancellor Olaf Scholz. The meeting was held at the Federal Chancellery 
    on January 15, 2023. Representatives from Apple Inc. and Microsoft Corporation were also present.
    The Federal Reserve announced a 0.25% interest rate increase, causing the S&P 500 to drop by 2%.
    """
    
    print(f"Sample text:\n{text}\n")
    result = extract_entities(text)
    print("Extracted entities:")
    for entity_type, count in result['entities'].items():
        print(f"  {entity_type}: {count}")
    print(f"\nTotal entity count: {result['entity_count']}")

def test_readability_metrics():
    """Test readability metrics feature."""
    print_separator("READABILITY METRICS")
    
    samples = {
        "simple": "The cat sat on the mat. The dog ran in the park. We had fun today.",
        "medium": "The analysis of various textual features can reveal patterns associated with fake news. Research indicates that sensationalist language often correlates with lower credibility.",
        "complex": "The epistemological implications of post-truth discourse necessitate a rigorous analytical framework for discerning verisimilitude in contemporary media narratives, particularly vis-à-vis the proliferation of algorithmically disseminated disinformation."
    }
    
    for complexity, text in samples.items():
        print(f"Sample ({complexity}):")
        print(f"  \"{text}\"")
        result = calculate_readability_metrics(text)
        print(f"  Flesch Reading Ease: {result['flesch_reading_ease']} (higher = easier to read)")
        print(f"  Flesch-Kincaid Grade Level: {result['flesch_kincaid_grade']}")
        print(f"  Average Grade Level: {result['average_grade_level']}")
        print()

def test_propaganda_detection():
    """Test propaganda detection feature."""
    print_separator("PROPAGANDA TECHNIQUE DETECTION")
    
    text = """
    SHOCKING NEWS! The radical left doesn't want you to know this INCREDIBLE truth.
    Scientists found that ordinary citizens are being misled by the mainstream media.
    Everyone is waking up to this conspiracy now. The government is hiding critical information.
    It's either you stand with us or against us. This is the greatest threat our nation has 
    ever faced! According to experts, we must act now before it's too late.
    """
    
    print(f"Sample text:\n{text}\n")
    result = detect_propaganda_techniques(text)
    print(f"Propaganda score: {result['propaganda_score']}%\n")
    print("Detected techniques:")
    for technique, count in result['techniques'].items():
        print(f"  {technique}: {count}")

def test_comprehensive_analysis():
    """Test comprehensive analysis feature."""
    print_separator("COMPREHENSIVE ANALYSIS")
    
    text = """
    BREAKING: Scientists discover SHOCKING link between vaccines and autism!
    The government doesn't want YOU to know this INCREDIBLE truth.
    According to anonymous sources close to the investigation, this conspiracy has been
    going on for YEARS! According to Dr. Smith from the Institute of Medical Research,
    "The evidence is clear." The CDC and WHO have not responded to our requests for comment.
    Share this with everyone you know before they take it down!!!
    """
    
    print(f"Sample text:\n{text}\n")
    result = comprehensive_text_analysis(text)
    
    # Print selected key insights
    print(f"Language: {result['language']['language_name']}")
    print(f"Lexical diversity: {result['uniqueness']['lexical_diversity']}")
    print(f"Readability (Flesch): {result['readability']['flesch_reading_ease']} (Grade level: {result['readability']['flesch_kincaid_grade']})")
    print(f"Propaganda score: {result['propaganda']['propaganda_score']}%")
    
    # Print entities
    if result['entities']['entity_count'] > 0:
        print("\nEntities:")
        for entity_type, count in result['entities']['entities'].items():
            print(f"  {entity_type}: {count}")
    
    # Print writing style
    print("\nWriting style:")
    for key, value in result['writing_style'].items():
        print(f"  {key}: {value}")

def test_enhanced_detector():
    """Test the enhanced detector."""
    print_separator("ENHANCED FAKE NEWS DETECTOR")
    
    detector = EnhancedFakeNewsDetector()
    
    text = """
    SHOCKING DISCOVERY: Scientists find definitive link between vaccines and autism!
    The government has been HIDING this information from the public for YEARS!
    According to anonymous sources, this conspiracy goes all the way to the top.
    Share this with everyone you know before it gets taken down!!!
    """
    
    print(f"Sample text:\n{text}\n")
    
    # Get prediction with comprehensive analysis
    result = detector.predict(text, comprehensive=True)
    
    # Print prediction and confidence
    print(f"Prediction: {result['prediction']}")
    print(f"Confidence: {result['confidence']:.4f}")
    if 'credibility_score' in result:
        print(f"Credibility score: {result['credibility_score']}/100")
    
    # Print language info
    if 'language' in result:
        print(f"Language: {result['language']['language_name']}")

def main():
    """Run all tests."""
    print("\nTESTING ENHANCED TEXT PROCESSING FEATURES\n")
    
    # Run individual feature tests
    test_language_detection()
    test_entity_extraction()
    test_readability_metrics()
    test_propaganda_detection()
    test_comprehensive_analysis()
    test_enhanced_detector()
    
    print("\nAll tests completed successfully!\n")

if __name__ == "__main__":
    main() 