#!/usr/bin/env python3
"""
FastAPI backend for fake news detection system with improved models and detailed explanations.
"""

import os
import sys
import re
import json
import logging
import shutil
from datetime import datetime
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Request, Body, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add parent directory to path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)

# Import fake news detection model
from improved_predict import ImprovedFakeNewsDetector

# Define Pydantic models for request/response
class TextAnalysisRequest(BaseModel):
    """Schema for text analysis request"""
    text: str = Field(..., min_length=50, description="Text to analyze")
    detailed: bool = Field(False, description="Whether to include detailed analysis")
    save_report: bool = Field(False, description="Whether to save a report")
    explain: bool = Field(False, description="Whether to include model explanations")
    explanation_method: str = Field("lime", description="Method for explanations: 'lime', 'shap', or 'both'")
    num_features: int = Field(10, description="Number of features to include in explanations")

class TextAnalysisResponse(BaseModel):
    """Schema for text analysis response"""
    prediction: str
    confidence: float
    timestamp: str
    detailed_analysis: Optional[Dict[str, Any]] = None
    explanation: Optional[str] = None
    credibility_score: Optional[float] = None
    report_id: Optional[str] = None
    history_id: Optional[str] = None
    model_explanations: Optional[Dict[str, Any]] = None

class HistoryItem(BaseModel):
    """Schema for history item"""
    id: str
    text: str
    prediction: str
    confidence: float
    timestamp: str
    credibility_score: Optional[float] = None
    report_id: Optional[str] = None

class ReportItem(BaseModel):
    """Schema for report item"""
    id: str
    text: str
    prediction: str
    confidence: float
    timestamp: str
    detailed_analysis: Optional[Dict[str, Any]] = None
    explanation: Optional[str] = None
    credibility_score: Optional[float] = None
    model_explanations: Optional[Dict[str, Any]] = None

class HistoryListResponse(BaseModel):
    """Schema for history list response"""
    items: List[HistoryItem]
    total: int

class ReportListResponse(BaseModel):
    """Schema for report list response"""
    items: List[ReportItem]
    total: int

class ExplanationRequest(BaseModel):
    """Schema for explanation request"""
    text: str = Field(..., min_length=50, description="Text to explain")
    method: str = Field("lime", description="Explanation method: 'lime', 'shap', or 'both'")
    num_features: int = Field(10, description="Number of features to include")

class ExplanationResponse(BaseModel):
    """Schema for explanation response"""
    method: str
    explanations: Dict[str, Any]
    highlighted_text: Optional[str] = None
    error: Optional[str] = None

# Create FastAPI app
app = FastAPI(
    title="Fake News Detection API",
    description="API for detecting fake news using advanced ML models with detailed analysis and explanations",
    version="2.0.0"
)

# Add CORS middleware with explicit frontend URLs
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:3002", 
                  "http://localhost:3003", "http://localhost:3004", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "Accept", "Origin", "X-Requested-With"],
)

# Initialize directories
REPORTS_DIR = os.path.join(script_dir, 'reports')
HISTORY_DIR = os.path.join(script_dir, 'history')
os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(HISTORY_DIR, exist_ok=True)

# Initialize detector
detector = ImprovedFakeNewsDetector()

@app.get("/", tags=["General"])
async def root():
    """API health check and info endpoint"""
    return {
        "message": "Fake News Detection API is running",
        "version": "2.0.0",
        "status": "active"
    }

@app.post("/analyze", response_model=TextAnalysisResponse, tags=["Analysis"])
async def analyze_text(request: TextAnalysisRequest):
    """
    Analyze text for fake news indicators
    
    Args:
        request: Request object containing text and options
        
    Returns:
        Analysis results
    """
    logger.info(f"Received analysis request - detailed: {request.detailed}, save_report: {request.save_report}")
    
    try:
        # Analyze text
        result = detector.predict(
            request.text, 
            detailed=request.detailed,
            explain=request.explain,
            explanation_method=request.explanation_method,
            num_features=request.num_features
        )
        
        if 'error' in result:
            raise HTTPException(status_code=400, detail=result['error'])
        
        # Save report if requested
        report_id = None
        if request.save_report and request.detailed:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_id = f"report_{timestamp}"
            report_path = detector.save_report(request.text, result, f"{report_id}.json")
            logger.info(f"Report saved: {report_path}")
            result['report_id'] = report_id
        
        # Save to history
        history_id = f"history_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        history_item = {
            'id': history_id,
            'text': request.text,
            'prediction': result['prediction'],
            'confidence': result['confidence'],
            'timestamp': result['timestamp'],
            'report_id': report_id
        }
        
        if 'credibility_score' in result:
            history_item['credibility_score'] = result['credibility_score']
        
        with open(os.path.join(HISTORY_DIR, f"{history_id}.json"), 'w') as f:
            json.dump(history_item, f, indent=2)
        
        logger.info(f"History saved: {history_id}")
        result['history_id'] = history_id
        
        return result
    
    except Exception as e:
        logger.error(f"Error analyzing text: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history", response_model=HistoryListResponse, tags=["History"])
async def get_history():
    """
    Get list of analysis history
    
    Returns:
        List of history items
    """
    try:
        history_files = os.listdir(HISTORY_DIR)
        history_items = []
        
        for filename in sorted(history_files, reverse=True):
            if filename.endswith(".json"):
                with open(os.path.join(HISTORY_DIR, filename), 'r') as f:
                    item = json.load(f)
                    history_items.append(item)
        
        return {
            "items": history_items,
            "total": len(history_items)
        }
    
    except Exception as e:
        logger.error(f"Error retrieving history: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history/{history_id}", tags=["History"])
async def get_history_item(history_id: str):
    """
    Get a specific history item
    
    Args:
        history_id: ID of the history item
        
    Returns:
        History item details
    """
    try:
        file_path = os.path.join(HISTORY_DIR, f"{history_id}.json")
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail=f"History item {history_id} not found")
        
        with open(file_path, 'r') as f:
            item = json.load(f)
        
        return item
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving history item: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/history/{history_id}", tags=["History"])
async def delete_history_item(history_id: str):
    """
    Delete a specific history item
    
    Args:
        history_id: ID of the history item
        
    Returns:
        Confirmation message
    """
    try:
        file_path = os.path.join(HISTORY_DIR, f"{history_id}.json")
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail=f"History item {history_id} not found")
        
        os.remove(file_path)
        logger.info(f"Deleted history item: {history_id}")
        
        return {"message": f"History item {history_id} deleted successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting history item: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/reports", response_model=ReportListResponse, tags=["Reports"])
async def get_reports():
    """
    Get list of saved reports
    
    Returns:
        List of report items
    """
    try:
        report_files = os.listdir(REPORTS_DIR)
        report_items = []
        
        for filename in sorted(report_files, reverse=True):
            if filename.endswith(".json"):
                with open(os.path.join(REPORTS_DIR, filename), 'r') as f:
                    report_data = json.load(f)
                    
                    # Extract ID from filename
                    report_id = filename.replace(".json", "")
                    
                    # Create summary item
                    item = {
                        "id": report_id,
                        "text": report_data.get("original_text", ""),
                        "prediction": report_data["prediction"].get("prediction", ""),
                        "confidence": report_data["prediction"].get("confidence", 0.0),
                        "timestamp": report_data["prediction"].get("timestamp", ""),
                        "credibility_score": report_data["prediction"].get("credibility_score")
                    }
                    
                    report_items.append(item)
        
        return {
            "items": report_items,
            "total": len(report_items)
        }
    
    except Exception as e:
        logger.error(f"Error retrieving reports: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/reports/{report_id}", tags=["Reports"])
async def get_report(report_id: str):
    """
    Get a specific report
    
    Args:
        report_id: ID of the report
        
    Returns:
        Report details
    """
    try:
        file_path = os.path.join(REPORTS_DIR, f"{report_id}.json")
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail=f"Report {report_id} not found")
        
        with open(file_path, 'r') as f:
            report = json.load(f)
        
        # Add report ID to response
        if "prediction" in report:
            report["prediction"]["id"] = report_id
        
        return report
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving report: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/reports/{report_id}", tags=["Reports"])
async def delete_report(report_id: str):
    """
    Delete a specific report
    
    Args:
        report_id: ID of the report
        
    Returns:
        Confirmation message
    """
    try:
        file_path = os.path.join(REPORTS_DIR, f"{report_id}.json")
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail=f"Report {report_id} not found")
        
        os.remove(file_path)
        logger.info(f"Deleted report: {report_id}")
        
        return {"message": f"Report {report_id} deleted successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting report: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/explain", response_model=ExplanationResponse, tags=["Explanations"])
async def explain_text(request: ExplanationRequest):
    """
    Generate explanations for text classification using LIME or SHAP
    
    Args:
        request: Request object containing text and explanation options
        
    Returns:
        Explanation results
    """
    logger.info(f"Received explanation request - method: {request.method}")
    
    try:
        if request.method.lower() == "lime":
            result = detector.explain_prediction_with_lime(
                request.text, 
                num_features=request.num_features
            )
            if "error" in result:
                raise HTTPException(status_code=400, detail=result["error"])
            
            highlighted_text = detector.explainer.get_highlighted_text(request.text, result)
            return {
                "method": "LIME",
                "explanations": result,
                "highlighted_text": highlighted_text
            }
            
        elif request.method.lower() == "shap":
            result = detector.explain_prediction_with_shap(
                request.text, 
                num_features=request.num_features
            )
            if "error" in result:
                raise HTTPException(status_code=400, detail=result["error"])
            
            highlighted_text = detector.explainer.get_highlighted_text(request.text, result)
            return {
                "method": "SHAP",
                "explanations": result,
                "highlighted_text": highlighted_text
            }
            
        elif request.method.lower() == "both":
            result = detector.get_combined_explanation(
                request.text, 
                num_features=request.num_features
            )
            if "error" in result:
                raise HTTPException(status_code=400, detail=result["error"])
            
            return {
                "method": "LIME+SHAP",
                "explanations": result["explanations"],
                "highlighted_text": result.get("highlighted_text_html")
            }
            
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported explanation method: {request.method}")
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating explanation: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/explain/methods", tags=["Explanations"])
async def get_explanation_methods():
    """
    Get available explanation methods
    
    Returns:
        List of available explanation methods
    """
    methods = [
        {
            "id": "lime",
            "name": "LIME",
            "description": "Local Interpretable Model-agnostic Explanations"
        },
        {
            "id": "shap",
            "name": "SHAP",
            "description": "SHapley Additive exPlanations"
        },
        {
            "id": "both",
            "name": "LIME + SHAP",
            "description": "Combined explanations using both LIME and SHAP"
        }
    ]
    
    return {"methods": methods}

@app.get("/health", tags=["General"])
async def health_check():
    """API health check endpoint"""
    return {
        "status": "ok",
        "service": "fake-news-detection-backend",
        "version": "2.0.0",
        "timestamp": datetime.now().isoformat()
    }

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
