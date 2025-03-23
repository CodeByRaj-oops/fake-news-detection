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

# Import fake news detection models
from improved_predict import ImprovedFakeNewsDetector
# Import enhanced detector with advanced text processing
from enhanced_predict import EnhancedFakeNewsDetector

# Define Pydantic models for request/response
class TextAnalysisRequest(BaseModel):
    """Schema for text analysis request"""
    text: str = Field(..., min_length=50, description="Text to analyze")
    detailed: bool = Field(False, description="Whether to include detailed analysis")
    save_report: bool = Field(False, description="Whether to save a report")
    explain: bool = Field(False, description="Whether to include model explanations")
    explanation_method: str = Field("lime", description="Method for explanations: 'lime', 'shap', or 'both'")
    num_features: int = Field(10, description="Number of features to include in explanations")

class EnhancedTextAnalysisRequest(BaseModel):
    """Schema for enhanced text analysis request"""
    text: str = Field(..., min_length=50, description="Text to analyze")
    detailed: bool = Field(False, description="Whether to include detailed analysis")
    comprehensive: bool = Field(False, description="Whether to perform comprehensive analysis with all features")
    save_report: bool = Field(False, description="Whether to save a report")
    explain: bool = Field(False, description="Whether to include model explanations")
    explanation_method: str = Field("lime", description="Method for explanations: 'lime', 'shap', or 'both'")
    num_features: int = Field(10, description="Number of features to include in explanations")
    detect_language: bool = Field(True, description="Whether to detect language of the text")

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
    language: Optional[Dict[str, Any]] = None
    comprehensive_analysis: Optional[Dict[str, Any]] = None

class HistoryItem(BaseModel):
    """Schema for history item"""
    id: str
    text: str
    prediction: str
    confidence: float
    timestamp: str
    credibility_score: Optional[float] = None
    report_id: Optional[str] = None
    language_code: Optional[str] = None

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
    language: Optional[Dict[str, Any]] = None

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

class LanguageDetectionRequest(BaseModel):
    """Schema for language detection request"""
    text: str = Field(..., min_length=20, description="Text to detect language")

class LanguageDetectionResponse(BaseModel):
    """Schema for language detection response"""
    language_code: str
    language_name: str
    confidence: float
    supported: bool

# Create FastAPI app
app = FastAPI(
    title="Fake News Detection API",
    description="API for detecting fake news using advanced ML models with detailed analysis and explanations",
    version="3.0.0"
)

# Setup CORS middleware to allow frontend to connect to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in development
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Add custom middleware for logging requests and errors
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests and responses"""
    request_id = f"{datetime.now().strftime('%Y%m%d%H%M%S')}-{id(request)}"
    logger.info(f"Request {request_id} started: {request.method} {request.url.path}")
    
    start_time = datetime.now()
    
    try:
        response = await call_next(request)
        process_time = (datetime.now() - start_time).total_seconds()
        logger.info(f"Request {request_id} completed: {response.status_code} in {process_time:.4f}s")
        return response
    except Exception as e:
        process_time = (datetime.now() - start_time).total_seconds()
        logger.error(f"Request {request_id} failed: {str(e)} in {process_time:.4f}s")
        return JSONResponse(
            status_code=500, 
            content={"detail": "Internal server error", "message": str(e)}
        )

# Initialize directories
REPORTS_DIR = os.path.join(script_dir, 'reports')
HISTORY_DIR = os.path.join(script_dir, 'history')
os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(HISTORY_DIR, exist_ok=True)

# Initialize detectors
# Standard detector
detector = ImprovedFakeNewsDetector()
# Enhanced detector with advanced text processing
enhanced_detector = EnhancedFakeNewsDetector()

@app.get("/", tags=["General"])
async def root():
    """API health check and info endpoint"""
    return {
        "message": "Fake News Detection API is running",
        "version": "3.0.0",
        "status": "active",
        "enhanced_features": True
    }

@app.post("/analyze", response_model=TextAnalysisResponse, tags=["Analysis"])
async def analyze_text(request: TextAnalysisRequest):
    """
    Analyze text for fake news indicators using the standard model
    
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

@app.post("/analyze/enhanced", response_model=TextAnalysisResponse, tags=["Enhanced Analysis"])
async def analyze_text_enhanced(request: EnhancedTextAnalysisRequest):
    """
    Analyze text using enhanced analysis with advanced text processing
    
    Args:
        request: Request object containing text and analysis options
        
    Returns:
        Enhanced analysis results with additional features
    """
    logger.info(f"Received enhanced analysis request - detailed: {request.detailed}, comprehensive: {request.comprehensive}")
    
    try:
        # Analyze text with enhanced detector
        result = enhanced_detector.predict(
            request.text, 
            detailed=request.detailed,
            comprehensive=request.comprehensive,
            explain=request.explain,
            explanation_method=request.explanation_method,
            num_features=request.num_features
        )
        
        if 'error' in result:
            raise HTTPException(status_code=400, detail=result['error'])
        
        # Save report if requested
        report_id = None
        if request.save_report and (request.detailed or request.comprehensive):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_id = f"enhanced_report_{timestamp}"
            report_path = enhanced_detector.save_report(request.text, result, f"{report_id}.json")
            logger.info(f"Enhanced report saved: {report_path}")
            result['report_id'] = report_id
        
        # Save to history
        history_id = f"history_enhanced_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
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
            
        if 'language' in result and result['language'].get('language_code'):
            history_item['language_code'] = result['language']['language_code']
        
        with open(os.path.join(HISTORY_DIR, f"{history_id}.json"), 'w') as f:
            json.dump(history_item, f, indent=2)
        
        logger.info(f"Enhanced history saved: {history_id}")
        result['history_id'] = history_id
        
        return result
    
    except Exception as e:
        logger.error(f"Error in enhanced analysis: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/detect-language", response_model=LanguageDetectionResponse, tags=["Language"])
async def detect_language(request: LanguageDetectionRequest):
    """
    Detect the language of the provided text
    
    Args:
        request: Request object containing text to analyze
        
    Returns:
        Language detection results
    """
    from utils.advanced_text_processor import detect_language as detect_lang
    
    try:
        # Detect language
        result = detect_lang(request.text)
        
        # Add flag to indicate if language is supported by our models
        is_supported = result['language_code'] == 'en'
        
        return {
            'language_code': result['language_code'],
            'language_name': result['language_name'],
            'confidence': result['confidence'],
            'supported': is_supported
        }
    
    except Exception as e:
        logger.error(f"Error detecting language: {e}", exc_info=True)
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
        history_path = os.path.join(HISTORY_DIR, f"{history_id}.json")
        
        if not os.path.exists(history_path):
            raise HTTPException(status_code=404, detail="History item not found")
            
        with open(history_path, 'r') as f:
            history_item = json.load(f)
            
        return history_item
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving history item: {e}", exc_info=True)
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
                    
                    # Extract report ID from filename
                    report_id = filename.replace(".json", "")
                    
                    # Extract prediction data
                    prediction = report_data.get('prediction', {})
                    
                    # Create report item
                    item = {
                        'id': report_id,
                        'text': report_data.get('original_text', ""),
                        'prediction': prediction.get('prediction', "Unknown"),
                        'confidence': prediction.get('confidence', 0.0),
                        'timestamp': prediction.get('timestamp', datetime.now().isoformat()),
                        'credibility_score': prediction.get('credibility_score')
                    }
                    
                    if 'detailed_analysis' in prediction:
                        item['detailed_analysis'] = prediction['detailed_analysis']
                        
                    if 'explanation' in prediction:
                        item['explanation'] = prediction['explanation']
                        
                    if 'model_explanations' in prediction:
                        item['model_explanations'] = prediction['model_explanations']
                        
                    if 'language' in prediction:
                        item['language'] = prediction['language']
                    
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
        report_path = os.path.join(REPORTS_DIR, f"{report_id}.json")
        
        if not os.path.exists(report_path):
            raise HTTPException(status_code=404, detail="Report not found")
            
        with open(report_path, 'r') as f:
            report = json.load(f)
            
        return report
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving report: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/history/{history_id}", tags=["History"])
async def delete_history_item(history_id: str):
    """
    Delete a history item
    
    Args:
        history_id: ID of the history item to delete
        
    Returns:
        Deletion status
    """
    try:
        history_path = os.path.join(HISTORY_DIR, f"{history_id}.json")
        
        if not os.path.exists(history_path):
            raise HTTPException(status_code=404, detail="History item not found")
            
        os.remove(history_path)
        
        return {"status": "success", "message": f"History item {history_id} deleted"}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting history item: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/reports/{report_id}", tags=["Reports"])
async def delete_report(report_id: str):
    """
    Delete a report
    
    Args:
        report_id: ID of the report to delete
        
    Returns:
        Deletion status
    """
    try:
        report_path = os.path.join(REPORTS_DIR, f"{report_id}.json")
        
        if not os.path.exists(report_path):
            raise HTTPException(status_code=404, detail="Report not found")
            
        os.remove(report_path)
        
        return {"status": "success", "message": f"Report {report_id} deleted"}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting report: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/explain", response_model=ExplanationResponse, tags=["Explanations"])
async def get_explanation(request: ExplanationRequest):
    """
    Get model explanation for text
    
    Args:
        request: Request object containing text and explanation options
        
    Returns:
        Model explanation
    """
    try:
        if EXPLAINERS_AVAILABLE:
            # Use enhanced model for explanation
            result = enhanced_detector.predict(
                request.text, 
                explain=True,
                explanation_method=request.method,
                num_features=request.num_features
            )
            
            if 'model_explanations' in result:
                explanation = result['model_explanations']
                return {
                    "method": request.method,
                    "explanations": explanation,
                    "highlighted_text": explanation.get("highlighted_text")
                }
            else:
                return {
                    "method": request.method,
                    "explanations": {},
                    "error": "Failed to generate explanation"
                }
        else:
            return {
                "method": request.method,
                "explanations": {},
                "error": "Explanation modules not available"
            }
    
    except Exception as e:
        logger.error(f"Error generating explanation: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

# Add comprehensive text analysis endpoint
@app.post("/analyze/comprehensive", tags=["Enhanced Analysis"])
async def comprehensive_analysis(request: TextAnalysisRequest):
    """
    Perform comprehensive text analysis with all available features
    
    Args:
        request: Request object containing text to analyze
        
    Returns:
        Comprehensive analysis results
    """
    try:
        # Import the comprehensive analysis function directly
        from utils.advanced_text_processor import comprehensive_text_analysis
        
        # Perform comprehensive analysis
        analysis_result = comprehensive_text_analysis(request.text)
        
        if 'error' in analysis_result:
            raise HTTPException(status_code=400, detail=analysis_result['error'])
            
        return analysis_result
    
    except Exception as e:
        logger.error(f"Error in comprehensive analysis: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
