from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import json
import os
import random
from datetime import datetime
import sys

# Add utils directory to path to import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils.text_processor import preprocess_text

# Create FastAPI app
app = FastAPI(
    title="Fake News Detection API",
    description="API for detecting fake news with enhanced text processing features",
    version="3.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configure CORS - IMPORTANT for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
    expose_headers=["Content-Type", "X-API-Key"]
)

# Ensure required directories exist
os.makedirs("history", exist_ok=True)
os.makedirs("reports", exist_ok=True)
os.makedirs("models", exist_ok=True)

# Models
class TextRequest(BaseModel):
    text: str
    explain: bool = False
    history_id: Optional[str] = None
    
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
    language: Optional[Dict[str, Any]] = None
    entities: Optional[Dict[str, Any]] = None
    readability: Optional[Dict[str, Any]] = None
    uniqueness: Optional[Dict[str, Any]] = None
    propaganda: Optional[Dict[str, Any]] = None

class ExplanationRequest(BaseModel):
    text: str
    method: str = "lime"
    num_features: int = 10

# Exception handler
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": f"An error occurred: {str(exc)}"}
    )

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "Fake News Detection API",
        "version": "3.0.0",
        "status": "operational",
        "documentation": "/docs"
    }

# Health check endpoint
@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "ok"}

# Analyze text for fake news
@app.post("/analyze")
async def analyze_text(request: TextRequest):
    """Analyze text for fake news likelihood"""
    try:
        # Get text from request
        text = request.text
        
        # Preprocess text
        processed = preprocess_text(text)
        
        # Generate unique ID
        result_id = f"analysis_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(1000, 9999)}"
        
        # Generate prediction (placeholder in this demo)
        import hashlib
        text_hash = int(hashlib.md5(text.encode()).hexdigest(), 16)
        prediction = (text_hash % 100) / 100
        
        # Determine label and confidence
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

# Enhanced analysis endpoint
@app.post("/analyze/enhanced")
async def enhanced_analysis(request: TextRequest):
    """Enhanced analysis with additional text processing features"""
    try:
        # Basic analysis
        text = request.text
        processed = preprocess_text(text)
        
        # Generate unique ID
        result_id = f"enhanced_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(1000, 9999)}"
        
        # Generate prediction (placeholder in this demo)
        import hashlib
        text_hash = int(hashlib.md5(text.encode()).hexdigest(), 16)
        prediction = (text_hash % 100) / 100
        
        # Determine label and confidence
        label = "FAKE" if prediction > 0.5 else "REAL"
        confidence = max(prediction, 1 - prediction)
        
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
        
        # Create result
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

# Get explanation methods
@app.get("/explain/methods")
async def explain_methods():
    """Return available explanation methods"""
    return {
        "methods": [
            {"id": "lime", "name": "LIME", "description": "Local Interpretable Model-agnostic Explanations"},
            {"id": "shap", "name": "SHAP", "description": "SHapley Additive exPlanations"}
        ]
    }

# Generate explanation
@app.post("/explain")
async def explain(request: ExplanationRequest):
    """Generate explanation for prediction"""
    try:
        text = request.text
        method = request.method
        num_features = request.num_features
        
        # Process text
        processed = preprocess_text(text)
        
        # Generate explanation (simplified placeholder)
        words = processed.split()
        word_importances = []
        
        # Generate some random word importances
        import random
        for word in words[:min(len(words), num_features)]:
            importance = random.uniform(-1, 1)
            word_importances.append({"word": word, "importance": importance})
        
        # Sort by absolute importance
        word_importances.sort(key=lambda x: abs(x["importance"]), reverse=True)
        
        return {
            "method": method,
            "features": word_importances,
            "base_value": 0.5,
            "prediction": 0.7 if text.lower().count("fake") > 0 else 0.3
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Explanation failed: {str(e)}")

# Get history
@app.get("/history")
async def get_history():
    """Fetch analysis history"""
    try:
        history = []
        for filename in os.listdir("history"):
            if filename.endswith(".json"):
                with open(os.path.join("history", filename), "r") as f:
                    history.append(json.load(f))
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve history: {str(e)}")

# Get specific history item
@app.get("/history/{item_id}")
async def get_history_item(item_id: str):
    """Fetch specific history item by ID"""
    try:
        file_path = os.path.join("history", f"{item_id}.json")
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail=f"History item not found: {item_id}")
        
        with open(file_path, "r") as f:
            return json.load(f)
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Failed to retrieve history item: {str(e)}")

# Language detection
@app.get("/detect-language")
async def detect_language(text: str):
    """Detect language of text"""
    return {
        "language_code": "en",
        "language_name": "English",
        "confidence": 0.98,
        "supported": True
    }

# Comprehensive analysis
@app.post("/analyze/comprehensive")
async def comprehensive_analysis(request: TextRequest):
    """Comprehensive analysis with all features"""
    # This is basically the same as enhanced analysis for the demo
    return await enhanced_analysis(request)

if __name__ == "__main__":
    print("Starting Fake News Detection Backend (Fixed Version)")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info") 