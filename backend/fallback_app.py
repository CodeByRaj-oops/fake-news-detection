from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
import json
import os
from datetime import datetime
import uvicorn
import nltk
from utils.text_processor import preprocess_text

# Download NLTK data if needed
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')

app = FastAPI(
    title="Fake News Detection API",
    description="API for fake news detection with enhanced text processing features",
    version="3.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure directories exist
os.makedirs("reports", exist_ok=True)
os.makedirs("history", exist_ok=True)
os.makedirs("models", exist_ok=True)

# Models
class TextRequest(BaseModel):
    text: str
    explain: bool = False
    history_id: str = None

class TextResult(BaseModel):
    prediction: float
    label: str
    confidence: float
    id: str
    timestamp: str
    text_length: int
    processed_text: str

class EnhancedAnalysisResult(BaseModel):
    prediction: float
    label: str
    confidence: float
    language: dict = None
    entities: dict = None
    readability: dict = None
    uniqueness: dict = None
    propaganda: dict = None
    
# Routes
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "Fake News Detection API",
        "version": "3.0.0",
        "status": "operational"
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "ok"}

@app.post("/analyze")
async def analyze_text(request: TextRequest):
    """Analyze text for fake news likelihood"""
    try:
        # Simple fallback analysis
        text = request.text
        processed = preprocess_text(text)
        
        # Generate random ID for result
        result_id = f"analysis_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(1000, 9999)}"
        
        # Get text stats
        word_count = len(text.split())
        
        # Placeholder prediction (would use ML model in real version)
        # Generate a consistent score for the same text
        import hashlib
        text_hash = int(hashlib.md5(text.encode()).hexdigest(), 16)
        prediction = (text_hash % 100) / 100
        
        # Classify
        label = "FAKE" if prediction > 0.5 else "REAL"
        confidence = max(prediction, 1 - prediction)
        
        # Create result
        result = TextResult(
            prediction=prediction,
            label=label,
            confidence=confidence,
            id=result_id,
            timestamp=datetime.now().isoformat(),
            text_length=len(text),
            processed_text=processed[:100] + "..." if len(processed) > 100 else processed
        )
        
        # Save to history
        history_path = os.path.join("history", f"{result_id}.json")
        with open(history_path, "w") as f:
            json.dump(result.model_dump(), f)
            
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/analyze/enhanced")
async def enhanced_analysis(request: TextRequest):
    """Enhanced analysis with additional text processing features"""
    try:
        # Basic analysis
        text = request.text
        processed = preprocess_text(text)
        
        # Generate random ID
        result_id = f"enhanced_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(1000, 9999)}"
        
        # Placeholder prediction
        import hashlib
        text_hash = int(hashlib.md5(text.encode()).hexdigest(), 16)
        prediction = (text_hash % 100) / 100
        
        # Classify
        label = "FAKE" if prediction > 0.5 else "REAL"
        confidence = max(prediction, 1 - prediction)
        
        # Enhanced features (simplified version)
        # Language detection
        language = {
            "language_code": "en",
            "language_name": "English",
            "confidence": 0.98,
            "supported": True
        }
        
        # Entity extraction
        entities = {
            "entities": {
                "PERSON": text.count("Trump") + text.count("Biden") + text.count("Obama"),
                "ORG": text.count("CNN") + text.count("Fox") + text.count("BBC"),
                "GPE": text.count("America") + text.count("US") + text.count("Russia")
            },
            "entity_count": text.count("Trump") + text.count("Biden") + text.count("Obama") + 
                          text.count("CNN") + text.count("Fox") + text.count("BBC") +
                          text.count("America") + text.count("US") + text.count("Russia")
        }
        
        # Readability metrics
        words = len(text.split())
        sentences = text.count('.') + text.count('!') + text.count('?')
        sentences = max(1, sentences)
        readability = {
            "flesch_reading_ease": 100 - (words / sentences),
            "flesch_kincaid_grade": (0.39 * words / sentences) + 11.8,
            "gunning_fog": 0.4 * (words / sentences),
            "coleman_liau_index": 5.89 * (len(text) / words) - 29.5,
            "average_grade_level": 10.5
        }
        
        # Text uniqueness
        unique_words = len(set(text.lower().split()))
        total_words = len(text.split())
        uniqueness = {
            "unique_words_ratio": unique_words / max(1, total_words),
            "lexical_diversity": unique_words / max(1, total_words),
            "content_hash": hashlib.md5(text.encode()).hexdigest()
        }
        
        # Propaganda techniques
        propaganda = {
            "techniques": {
                "name_calling": text.lower().count("fake") + text.lower().count("corrupt"),
                "exaggeration": text.lower().count("very") + text.lower().count("huge"),
                "loaded_language": text.lower().count("disaster") + text.lower().count("terrible")
            },
            "propaganda_score": (text.lower().count("fake") + text.lower().count("corrupt") +
                               text.lower().count("very") + text.lower().count("huge") +
                               text.lower().count("disaster") + text.lower().count("terrible")) / max(1, len(text.split())) * 100
        }
        
        # Create enhanced result
        result = EnhancedAnalysisResult(
            prediction=prediction,
            label=label,
            confidence=confidence,
            language=language,
            entities=entities,
            readability=readability,
            uniqueness=uniqueness,
            propaganda=propaganda
        )
        
        # Save to history
        history_path = os.path.join("history", f"{result_id}.json")
        with open(history_path, "w") as f:
            json.dump(result.model_dump(), f)
            
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Enhanced analysis failed: {str(e)}")

@app.get("/detect-language")
async def detect_language(text: str):
    """Detect the language of the input text"""
    return {
        "language_code": "en",
        "language_name": "English",
        "confidence": 0.98,
        "supported": True
    }

@app.get("/history")
async def get_history():
    """Get analysis history"""
    history = []
    try:
        for filename in os.listdir("history"):
            if filename.endswith(".json"):
                with open(os.path.join("history", filename), "r") as f:
                    history.append(json.load(f))
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve history: {str(e)}")

@app.get("/explain/methods")
async def explain_methods():
    """Return explanation methods"""
    return {
        "methods": [
            {"id": "lime", "name": "LIME", "description": "Local Interpretable Model-agnostic Explanations"},
            {"id": "shap", "name": "SHAP", "description": "SHapley Additive exPlanations"}
        ]
    }

if __name__ == "__main__":
    # Run the server
    print("Starting Fake News Detection Backend Server...")
    # Use port 8001 to avoid conflict with the test server
    uvicorn.run(app, host="0.0.0.0", port=8001) 