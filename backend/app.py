#!/usr/bin/env python3
"""
FastAPI backend for fake news detection with advanced analysis capabilities.
"""

import os
import sys
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from pathlib import Path

from fastapi import FastAPI, HTTPException, BackgroundTasks, Query, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
import uvicorn

# Add the backend directory to path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)

# Import detector
from improved_predict import ImprovedFakeNewsDetector

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize app
app = FastAPI(
    title="Fake News Detector API",
    description="API for detecting fake news with detailed analysis",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create report directory
REPORTS_DIR = os.path.join(script_dir, "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

# Create history directory to store request/response history
HISTORY_DIR = os.path.join(script_dir, "history")
os.makedirs(HISTORY_DIR, exist_ok=True)

# Initialize detector as a global variable
detector = ImprovedFakeNewsDetector()

# Pydantic models for request/response
class TextAnalysisRequest(BaseModel):
    text: str = Field(..., title="News text", description="The text to analyze for fake news detection", min_length=10)
    detailed: bool = Field(False, title="Detailed analysis", description="Whether to return detailed analysis")
    save_report: bool = Field(False, title="Save report", description="Whether to save a detailed report")

class CredibilityScore(BaseModel):
    score: float = Field(..., title="Credibility score", description="Credibility score (0-100)")
    description: str = Field(..., title="Description", description="Description of the credibility score")

class TextFeatures(BaseModel):
    word_count: int
    avg_word_length: float
    sentence_count: int
    avg_sentence_length: float
    exclamation_count: int
    question_count: int
    capitalized_ratio: float
    clickbait_score: int
    polarity: float
    subjectivity: float
    personal_pronouns: int
    punctuation_ratio: float

class WritingStyle(BaseModel):
    reading_ease: float
    avg_word_complexity: float
    hedging_phrases: int
    exaggeration_phrases: int

class WarningSignsAnalysis(BaseModel):
    misinformation_indicators: List[str]
    reliability_indicators: List[str]
    excessive_punctuation: bool
    excessive_capitalization: bool
    social_media_callout: bool
    source_credibility_issues: bool

class WordAnalysis(BaseModel):
    top_words: Dict[str, int]
    top_bigrams: Dict[str, int]
    emotional_language_count: int
    scientific_language_count: int

class DetailedAnalysis(BaseModel):
    text_features: TextFeatures
    writing_style: WritingStyle
    warning_signs: WarningSignsAnalysis
    word_analysis: WordAnalysis

class ReportMetadata(BaseModel):
    report_id: str
    timestamp: str
    filename: str
    
class TextAnalysisResponse(BaseModel):
    prediction: str = Field(..., title="Prediction", description="Prediction label (FAKE or REAL)")
    confidence: float = Field(..., title="Confidence", description="Confidence score (0-1)")
    credibility_score: Optional[float] = Field(None, title="Credibility score", description="Credibility score (0-100)")
    explanation: Optional[str] = Field(None, title="Explanation", description="Human-readable explanation of the prediction")
    detailed_analysis: Optional[DetailedAnalysis] = Field(None, title="Detailed analysis", description="Detailed analysis of the text")
    report: Optional[ReportMetadata] = Field(None, title="Report", description="Metadata of the saved report")
    timestamp: str = Field(..., title="Timestamp", description="Timestamp of the prediction")

class HistoryItem(BaseModel):
    id: str
    text_preview: str
    prediction: str
    confidence: float
    credibility_score: Optional[float]
    timestamp: str

class ErrorResponse(BaseModel):
    error: str

def save_history(request_data: Dict, response_data: Dict) -> str:
    """Save request/response history to a file and return the history ID."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    history_id = f"history_{timestamp}"
    
    # Create history record
    history_record = {
        "request": request_data,
        "response": response_data,
        "timestamp": datetime.now().isoformat()
    }
    
    # Save to file
    history_path = os.path.join(HISTORY_DIR, f"{history_id}.json")
    with open(history_path, 'w') as f:
        json.dump(history_record, f, indent=2)
    
    logger.info(f"History saved to {history_path}")
    return history_id

@app.get("/", response_class=JSONResponse)
async def root():
    """Root endpoint that returns API information."""
    return {
        "name": "Fake News Detector API",
        "version": "1.0.0",
        "description": "API for detecting fake news with detailed analysis",
        "endpoints": {
            "POST /analyze": "Analyze text for fake news",
            "GET /history": "Get analysis history",
            "GET /history/{history_id}": "Get specific analysis from history",
            "GET /reports": "Get list of saved reports",
            "GET /reports/{report_id}": "Get specific report"
        }
    }

@app.post("/analyze", response_model=TextAnalysisResponse, responses={400: {"model": ErrorResponse}})
async def analyze_text(
    request: Request,
    background_tasks: BackgroundTasks,
    analysis_request: TextAnalysisRequest
):
    """
    Analyze text for fake news detection.
    
    Returns prediction with confidence score and optional detailed analysis.
    """
    try:
        text = analysis_request.text
        detailed = analysis_request.detailed
        save_report = analysis_request.save_report
        
        # Check if text is too short
        if len(text.strip()) < 10:
            raise HTTPException(status_code=400, detail="Text is too short for analysis")
        
        # Perform prediction
        result = detector.predict(text, detailed=detailed)
        
        # Save report if requested
        report_metadata = None
        if save_report and detailed:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_filename = f"report_{timestamp}.json"
            report_path = detector.save_report(text, result, filename=report_filename)
            
            report_metadata = {
                "report_id": timestamp,
                "timestamp": datetime.now().isoformat(),
                "filename": report_filename
            }
        
        # Prepare response
        response_data = {
            "prediction": result.get("prediction", "Unknown"),
            "confidence": result.get("confidence", 0.0),
            "timestamp": datetime.now().isoformat()
        }
        
        # Add detailed analysis if available
        if detailed:
            response_data["credibility_score"] = result.get("credibility_score")
            response_data["explanation"] = result.get("explanation")
            response_data["detailed_analysis"] = result.get("detailed_analysis")
        
        # Add report metadata if available
        if report_metadata:
            response_data["report"] = report_metadata
        
        # Save request/response to history in background
        request_data = {
            "text": text,
            "detailed": detailed,
            "save_report": save_report
        }
        background_tasks.add_task(save_history, request_data, response_data)
        
        return response_data
        
    except Exception as e:
        logger.error(f"Error analyzing text: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error analyzing text: {str(e)}")

@app.get("/history", response_model=List[HistoryItem])
async def get_history(
    limit: int = Query(10, ge=1, le=100, description="Maximum number of history items to return"),
    offset: int = Query(0, ge=0, description="Offset for pagination")
):
    """Get analysis history with pagination."""
    try:
        # List all history files
        history_files = sorted(
            [f for f in os.listdir(HISTORY_DIR) if f.endswith('.json')],
            reverse=True
        )
        
        # Apply pagination
        paginated_files = history_files[offset:offset + limit]
        
        # Load history items
        history_items = []
        for filename in paginated_files:
            file_path = os.path.join(HISTORY_DIR, filename)
            try:
                with open(file_path, 'r') as f:
                    history_data = json.load(f)
                
                # Extract history ID from filename
                history_id = os.path.splitext(filename)[0]
                
                # Create preview (first 100 chars)
                text = history_data.get("request", {}).get("text", "")
                text_preview = text[:100] + "..." if len(text) > 100 else text
                
                # Get response data
                response = history_data.get("response", {})
                
                # Create history item
                history_item = {
                    "id": history_id,
                    "text_preview": text_preview,
                    "prediction": response.get("prediction", "Unknown"),
                    "confidence": response.get("confidence", 0.0),
                    "credibility_score": response.get("credibility_score"),
                    "timestamp": history_data.get("timestamp", "")
                }
                
                history_items.append(history_item)
                
            except Exception as e:
                logger.error(f"Error loading history file {filename}: {e}")
        
        return history_items
        
    except Exception as e:
        logger.error(f"Error getting history: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error getting history: {str(e)}")

@app.get("/history/{history_id}", response_model=Dict[str, Any])
async def get_history_item(
    history_id: str
):
    """Get specific analysis from history."""
    try:
        # Check if history file exists
        history_file = f"{history_id}.json"
        history_path = os.path.join(HISTORY_DIR, history_file)
        
        if not os.path.exists(history_path):
            raise HTTPException(status_code=404, detail=f"History item {history_id} not found")
        
        # Load history item
        with open(history_path, 'r') as f:
            history_data = json.load(f)
        
        return history_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting history item {history_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error getting history item: {str(e)}")

@app.get("/reports", response_model=List[ReportMetadata])
async def get_reports(
    limit: int = Query(10, ge=1, le=100, description="Maximum number of reports to return"),
    offset: int = Query(0, ge=0, description="Offset for pagination")
):
    """Get list of saved reports with pagination."""
    try:
        # List all report files
        report_files = sorted(
            [f for f in os.listdir(REPORTS_DIR) if f.endswith('.json')],
            reverse=True
        )
        
        # Apply pagination
        paginated_files = report_files[offset:offset + limit]
        
        # Create metadata for each report
        reports = []
        for filename in paginated_files:
            # Extract report ID from filename (remove "report_" prefix and ".json" suffix)
            report_id = filename.replace("report_", "").replace(".json", "")
            
            # Get file timestamp
            file_path = os.path.join(REPORTS_DIR, filename)
            file_timestamp = datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat()
            
            # Create report metadata
            report_metadata = {
                "report_id": report_id,
                "timestamp": file_timestamp,
                "filename": filename
            }
            
            reports.append(report_metadata)
        
        return reports
        
    except Exception as e:
        logger.error(f"Error getting reports: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error getting reports: {str(e)}")

@app.get("/reports/{report_id}", response_model=Dict[str, Any])
async def get_report(
    report_id: str
):
    """Get specific report by ID."""
    try:
        # Check if report file exists
        report_file = f"report_{report_id}.json"
        report_path = os.path.join(REPORTS_DIR, report_file)
        
        if not os.path.exists(report_path):
            raise HTTPException(status_code=404, detail=f"Report {report_id} not found")
        
        # Load report
        with open(report_path, 'r') as f:
            report_data = json.load(f)
        
        return report_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting report {report_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error getting report: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# Serve static files for the frontend
frontend_dir = os.path.join(os.path.dirname(script_dir), "frontend", "build")
if os.path.exists(frontend_dir):
    app.mount("/app", StaticFiles(directory=frontend_dir, html=True), name="frontend")

# Run the app
if __name__ == "__main__":
    try:
        # Try to load model to verify it's working
        if detector.model is None:
            logger.warning("Model not loaded, API will return default values")
        
        # Run the server
        port = int(os.environ.get("PORT", 8000))
        host = os.environ.get("HOST", "127.0.0.1")
        
        logger.info(f"Starting server on {host}:{port}")
        uvicorn.run("app:app", host=host, port=port, reload=True)
        
    except Exception as e:
        logger.error(f"Error starting server: {e}", exc_info=True) 