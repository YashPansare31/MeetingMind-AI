from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import tempfile
import asyncio
import logging
from .models import AnalysisResult, HealthCheck
from .services import MeetingAnalysisService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Meeting Analysis API V1", 
    version="1.0.0",
    description="AI-powered meeting transcription and analysis"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize service
analysis_service = MeetingAnalysisService()

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Meeting Analysis API V1", "docs": "/docs"}

@app.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check endpoint"""
    return HealthCheck(
        status="healthy",
        openai_configured=analysis_service.is_configured()
    )

@app.post("/analyze", response_model=AnalysisResult)
async def analyze_meeting(file: UploadFile = File(...)):
    """
    Analyze meeting audio/video file
    Accepts: MP3, MP4, WAV, M4A files
    Returns: Transcription, summary, action items, and decision points
    """
    start_time = asyncio.get_event_loop().time()
    
    # Validate file
    if not analysis_service.validate_file(file):
        raise HTTPException(status_code=400, detail="Invalid file type or size")
    
    temp_file_path = None
    try:
        # Save uploaded file temporarily
        temp_file_path = await save_temp_file(file)
        
        # Process the file
        result = await analysis_service.process_meeting(temp_file_path)
        
        processing_time = asyncio.get_event_loop().time() - start_time
        result.processing_time = round(processing_time, 2)
        
        return result
        
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")
    
    finally:
        # Clean up temp file
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

async def save_temp_file(file: UploadFile) -> str:
    """Save uploaded file to temporary location"""
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file.filename.split('.')[-1]}") as temp_file:
        content = await file.read()
        temp_file.write(content)
        return temp_file.name