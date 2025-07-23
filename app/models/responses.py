from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Service status")
    timestamp: datetime = Field(..., description="Response timestamp")
    version: str = Field(..., description="API version")
    
    class Config:
        schema_extra = {
            "example": {
                "status": "healthy",
                "timestamp": "2025-01-23T10:30:00Z",
                "version": "1.0.0"
            }
        }


class TranscriptionResponse(BaseModel):
    """Transcription response"""
    success: bool = Field(..., description="Processing success status")
    file_id: str = Field(..., description="Unique file identifier")
    transcript: Dict[str, Any] = Field(..., description="Transcription result")
    metadata: Dict[str, Any] = Field(..., description="Processing metadata")
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "file_id": "abc123",
                "transcript": {
                    "text": "Let's start the meeting...",
                    "language": "en",
                    "duration": 120.5
                },
                "metadata": {
                    "model_used": "base",
                    "processing_time": 15.2,
                    "file_size": 1024000
                }
            }
        }


class ActionItemResponse(BaseModel):
    """Action item response"""
    id: int = Field(..., description="Action item ID")
    task: str = Field(..., description="Task description")
    assignees: List[str] = Field(..., description="Assigned persons")
    deadlines: List[str] = Field(..., description="Detected deadlines")
    priority: str = Field(..., description="Priority level")
    confidence: float = Field(..., description="Extraction confidence")
    
    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "task": "John needs to follow up with the client by Friday",
                "assignees": ["John"],
                "deadlines": ["by Friday"],
                "priority": "medium",
                "confidence": 0.85
            }
        }


class AnalysisResponse(BaseModel):
    """Complete analysis response"""
    success: bool = Field(..., description="Processing success status")
    file_id: str = Field(..., description="Unique file identifier")
    metadata: Dict[str, Any] = Field(..., description="Processing metadata")
    transcript: Dict[str, Any] = Field(..., description="Transcription data")
    action_items: List[ActionItemResponse] = Field(..., description="Extracted action items")
    summary: Dict[str, Any] = Field(..., description="Analysis summary")
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "file_id": "abc123",
                "metadata": {
                    "processed_at": "2025-01-23T10:30:00Z",
                    "processing_time": 25.5,
                    "model_used": "base"
                },
                "transcript": {
                    "text": "Meeting transcript...",
                    "duration": 300.0
                },
                "action_items": [
                    {
                        "id": 1,
                        "task": "Follow up with client",
                        "assignees": ["John"],
                        "deadlines": ["Friday"],
                        "priority": "high",
                        "confidence": 0.9
                    }
                ],
                "summary": {
                    "total_action_items": 5,
                    "high_priority_items": 1,
                    "items_with_assignees": 3
                }
            }
        }


class ErrorResponse(BaseModel):
    """Error response"""
    success: bool = Field(default=False, description="Processing success status")
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(default=None, description="Additional error details")
    
    class Config:
        schema_extra = {
            "example": {
                "success": False,
                "error": "FileUploadError",
                "message": "File size exceeds maximum limit",
                "details": {
                    "max_size": "100MB",
                    "uploaded_size": "150MB"
                }
            }
        }