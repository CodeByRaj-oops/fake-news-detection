from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import random
import os
import json
from datetime import datetime

# Create FastAPI app
app = FastAPI(
    title="Fake News Detection API (Fallback)",
    description="Simplified API for testing the frontend connection",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configure CORS
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
    processed_text: Optional[str] = None
    text_length: Optional[int] = None

class ExplainRequest(BaseModel):
    text: str
    method: str = "lime"

# Root endpoint
@app.get("/")
async def root():
    return {
        "service": "Fake News Detection API (Fallback)",
        "version": "1.0.0", 
        "status": "ok",
        "endpoints": ["/analyze", "/analyze/enhanced", "/health", "/history", "/explain", "/explain/methods", "/detect-language"]
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

# Analyze endpoint - generates mock predictions
@app.post("/analyze", response_model=TextResult)
async def analyze_text(request: TextRequest):
    # Mock processing
    text = request.text
    
    # Generate a random prediction for testing
    prediction = random.random()
    label = "FAKE" if prediction > 0.5 else "REAL"
    confidence = max(0.5, prediction) if label == "FAKE" else max(0.5, 1 - prediction)
    
    # Generate a unique ID
    item_id = f"test-{datetime.now().strftime('%Y%m%d%H%M%S')}-{random.randint(1000, 9999)}"
    
    # Process the text (simple simulation)
    processed_text = text.lower()[:100] + "..." if len(text) > 100 else text.lower()
    
    # Prepare result
    result = {
        "prediction": prediction,
        "label": label,
        "confidence": confidence,
        "id": item_id,
        "timestamp": datetime.now().isoformat(),
        "processed_text": processed_text,
        "text_length": len(text)
    }
    
    # Save to history
    history_path = os.path.join("history", f"{item_id}.json")
    with open(history_path, "w") as f:
        json.dump({
            "request": {"text": text},
            "result": result
        }, f)
    
    return result

# Enhanced analysis endpoint - mock implementation
@app.post("/analyze/enhanced")
async def enhanced_analysis(request: TextRequest):
    # Mock processing
    text = request.text
    
    # Generate a random prediction
    prediction = random.random()
    label = "FAKE" if prediction > 0.5 else "REAL"
    confidence = max(0.5, prediction) if label == "FAKE" else max(0.5, 1 - prediction)
    
    # Generate a unique ID
    item_id = f"test-{datetime.now().strftime('%Y%m%d%H%M%S')}-{random.randint(1000, 9999)}"
    
    # Process the text (simple simulation)
    processed_text = text.lower()[:100] + "..." if len(text) > 100 else text.lower()
    
    # Save to history
    result = {
        "prediction": prediction,
        "label": label,
        "confidence": confidence,
        "id": item_id,
        "timestamp": datetime.now().isoformat(),
        "processed_text": processed_text,
        "text_length": len(text),
        "language": {
            "language_code": "en",
            "language_name": "English",
            "confidence": 0.98,
            "supported": True
        },
        "entities": {
            "entities": {
                "PERSON": 2,
                "ORG": 3,
                "GPE": 1
            },
            "entity_count": 6
        },
        "readability": {
            "flesch_reading_ease": 65.2,
            "flesch_kincaid_grade": 8.7,
            "smog_index": 9.2,
            "gunning_fog": 10.1,
            "coleman_liau_index": 9.8,
            "average_grade_level": 9.3
        },
        "uniqueness": {
            "lexical_diversity": 0.76,
            "unique_words_ratio": 0.68,
            "content_hash": "abcdef1234567890"
        },
        "propaganda": {
            "techniques": {
                "name_calling": 1,
                "exaggeration": 2,
                "loaded_language": 1
            },
            "propaganda_score": 45.0
        }
    }
    
    # Save to history
    history_path = os.path.join("history", f"{item_id}.json")
    with open(history_path, "w") as f:
        json.dump({
            "request": {"text": text},
            "result": result
        }, f)
    
    return result

# Get history endpoint
@app.get("/history")
async def get_history():
    """Get analysis history"""
    history = []
    try:
        for filename in os.listdir("history"):
            if filename.endswith(".json"):
                with open(os.path.join("history", filename), "r") as f:
                    data = json.load(f)
                    history.append(data.get("result", {}))
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve history: {str(e)}")

# Get specific history item
@app.get("/history/{item_id}")
async def get_history_item(item_id: str):
    """Get specific history item"""
    try:
        file_path = os.path.join("history", f"{item_id}.json")
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                data = json.load(f)
                return data.get("result", {})
        else:
            raise HTTPException(status_code=404, detail=f"History item {item_id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve history item: {str(e)}")

# Explain methods endpoint
@app.get("/explain/methods")
async def explain_methods():
    """Return explanation methods"""
    return {
        "methods": [
            {"id": "lime", "name": "LIME", "description": "Local Interpretable Model-agnostic Explanations"},
            {"id": "shap", "name": "SHAP", "description": "SHapley Additive exPlanations"}
        ]
    }

# Explain endpoint
@app.post("/explain")
async def explain_prediction(request: ExplainRequest):
    """Mock implementation of explanation endpoint"""
    return {
        "method": request.method,
        "text": request.text,
        "explanation": {
            "features": [
                {"word": "fake", "importance": 0.42, "direction": "positive"},
                {"word": "claim", "importance": 0.38, "direction": "positive"},
                {"word": "source", "importance": 0.35, "direction": "negative"},
                {"word": "according", "importance": 0.29, "direction": "negative"},
                {"word": "experts", "importance": 0.27, "direction": "negative"}
            ],
            "summary": "The words 'fake' and 'claim' contributed most to the prediction."
        }
    }

# Language detection endpoint
@app.get("/detect-language")
async def detect_language(text: str):
    """Detect the language of the input text"""
    return {
        "language_code": "en",
        "language_name": "English",
        "confidence": 0.98,
        "supported": True
    }

# Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 