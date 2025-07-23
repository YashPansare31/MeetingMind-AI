from pydantic import BaseModel
from typing import List, Optional

class AnalysisResult(BaseModel):
    """Response model for meeting analysis"""
    transcription: str
    summary: str
    action_items: List[str]
    decision_points: List[str]
    processing_time: Optional[float] = None

class HealthCheck(BaseModel):
    """Health check response model"""
    status: str
    openai_configured: bool

class ErrorResponse(BaseModel):
    """Error response model"""
    detail: str
    status_code: int