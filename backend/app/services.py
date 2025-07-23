import openai
import os
import asyncio
import logging
from typing import List
from fastapi import UploadFile
from .models import AnalysisResult

logger = logging.getLogger(__name__)

class MeetingAnalysisService:
    """Service class for meeting analysis operations"""
    
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
        
        self.allowed_types = [
            "audio/mpeg", "audio/mp4", "audio/wav", 
            "video/mp4", "audio/m4a", "audio/x-m4a"
        ]
        self.max_file_size = 25 * 1024 * 1024  # 25MB
    
    def is_configured(self) -> bool:
        """Check if OpenAI API key is configured"""
        return bool(self.openai_api_key)
    
    def validate_file(self, file: UploadFile) -> bool:
        """Validate uploaded file type and size"""
        if file.content_type not in self.allowed_types:
            logger.error(f"Invalid file type: {file.content_type}")
            return False
        
        if file.size and file.size > self.max_file_size:
            logger.error(f"File too large: {file.size} bytes")
            return False
        
        return True
    
    async def process_meeting(self, file_path: str) -> AnalysisResult:
        """Process meeting file and return analysis results"""
        # Step 1: Transcription
        transcription = await self.transcribe_audio(file_path)
        
        # Step 2: Parallel analysis
        summary_task = asyncio.create_task(self.generate_summary(transcription))
        action_items_task = asyncio.create_task(self.extract_action_items(transcription))
        decisions_task = asyncio.create_task(self.extract_decisions(transcription))
        
        summary, action_items, decision_points = await asyncio.gather(
            summary_task, action_items_task, decisions_task
        )
        
        return AnalysisResult(
            transcription=transcription,
            summary=summary,
            action_items=action_items,
            decision_points=decision_points
        )
    
    async def transcribe_audio(self, file_path: str) -> str:
        """Transcribe audio file using OpenAI Whisper"""
        try:
            logger.info("Starting transcription...")
            with open(file_path, "rb") as audio_file:
                transcript_response = openai.Audio.transcribe(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text"
                )
            
            logger.info(f"Transcription completed. Length: {len(transcript_response)} characters")
            return transcript_response
        
        except Exception as e:
            logger.error(f"Transcription error: {str(e)}")
            raise Exception(f"Failed to transcribe audio: {str(e)}")
    
    async def generate_summary(self, transcription: str) -> str:
        """Generate meeting summary using GPT"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at summarizing business meetings. Create a concise, well-structured summary that captures the key topics, discussions, and outcomes."
                    },
                    {
                        "role": "user",
                        "content": f"Please summarize this meeting transcript:\n\n{transcription}"
                    }
                ],
                max_tokens=500,
                temperature=0.3
            )
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            logger.error(f"Summary generation error: {str(e)}")
            return "Error generating summary"
    
    async def extract_action_items(self, transcription: str) -> List[str]:
        """Extract action items from transcription"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at identifying action items from meeting transcripts. Extract clear, actionable tasks that were assigned or discussed. Return only the action items, one per line, without numbering."
                    },
                    {
                        "role": "user",
                        "content": f"Extract action items from this meeting transcript:\n\n{transcription}"
                    }
                ],
                max_tokens=300,
                temperature=0.2
            )
            
            action_items = response.choices[0].message.content.strip().split('\n')
            return [item.strip('- ').strip() for item in action_items if item.strip()]
        
        except Exception as e:
            logger.error(f"Action items extraction error: {str(e)}")
            return ["Error extracting action items"]
    
    async def extract_decisions(self, transcription: str) -> List[str]:
        """Extract decision points from transcription"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at identifying decisions made during meetings. Extract clear decisions, conclusions, or resolutions that were reached. Return only the decisions, one per line, without numbering."
                    },
                    {
                        "role": "user",
                        "content": f"Extract decisions and key conclusions from this meeting transcript:\n\n{transcription}"
                    }
                ],
                max_tokens=300,
                temperature=0.2
            )
            
            decisions = response.choices[0].message.content.strip().split('\n')
            return [decision.strip('- ').strip() for decision in decisions if decision.strip()]
        
        except Exception as e:
            logger.error(f"Decision extraction error: {str(e)}")
            return ["Error extracting decisions"]