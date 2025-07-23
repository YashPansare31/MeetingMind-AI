from pydantic import BaseModel, Field, validator
from typing import Optional, List
from werkzeug.datastructures import FileStorage


class TranscriptionRequest(BaseModel):
    """Request model for transcription endpoint"""
    model_size: Optional[str] = Field(default="base", description="Whisper model size")
    language: Optional[str] = Field(default=None, description="Audio language (auto-detect if None)")
    
    @validator('model_size')
    def validate_model_size(cls, v):
        valid_sizes = ['tiny', 'base', 'small', 'medium', 'large']
        if v not in valid_sizes:
            raise ValueError(f'Model size must be one of: {valid_sizes}')
        return v

    class Config:
        schema_extra = {
            "example": {
                "model_size": "base",
                "language": "en"
            }
        }


class AnalysisRequest(BaseModel):
    """Request model for analysis endpoint"""
    extract_action_items: bool = Field(default=True, description="Extract action items")
    extract_sentiment: bool = Field(default=False, description="Extract sentiment")
    custom_keywords: Optional[List[str]] = Field(default=None, description="Custom action keywords")
    
    class Config:
        schema_extra = {
            "example": {
                "extract_action_items": True,
                "extract_sentiment": False,
                "custom_keywords": ["follow up", "deadline", "urgent"]
            }
        }

