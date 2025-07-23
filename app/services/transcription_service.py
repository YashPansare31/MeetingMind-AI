import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from app.services.audio_processor import AudioProcessor
from app.services.nlp_service import NLPService
from app.services.file_service import FileService
from app.models.entities import MeetingAnalysis
from app.core.exceptions import MeetingAnalyticsException

logger = logging.getLogger(__name__)


class TranscriptionService:
    """Main service for meeting transcription and analysis"""
    
    def __init__(self, config):
        self.config = config
        self.audio_processor = AudioProcessor(config.WHISPER_MODEL_SIZE)
        self.nlp_service = NLPService()
        self.file_service = FileService(
            upload_folder=config.UPLOAD_FOLDER,
            max_file_size=config.MAX_FILE_SIZE,
            allowed_extensions=config.ALLOWED_EXTENSIONS
        )
    
    def process_audio_file(
        self,
        file_info: Dict[str, Any],
        model_size: Optional[str] = None,
        language: Optional[str] = None,
        extract_action_items: bool = True,
        custom_keywords: Optional[list] = None
    ) -> MeetingAnalysis:
        """Process audio file with transcription and analysis"""
        logger.info(f"Starting audio processing for file: {file_info['file_id']}")
        
        start_time = datetime.now()
        
        try:
            # Use custom model size if provided
            if model_size and model_size != self.audio_processor.model_size:
                self.audio_processor = AudioProcessor(model_size)
            
            # Transcribe audio
            transcription_result = self.audio_processor.transcribe_audio(
                file_info['file_path'],
                language=language
            )
            
            # Extract action items if requested
            action_items = []
            if extract_action_items:
                action_items = self.nlp_service.extract_action_items(
                    transcription_result['text'],
                    custom_keywords=custom_keywords
                )
            
            # Calculate processing time
            processing_time = (datetime.now() - start_time).total_seconds()
            
            # Create metadata
            metadata = {
                "file_id": file_info['file_id'],
                "original_filename": file_info['original_filename'],
                "processed_at": datetime.now().isoformat(),
                "processing_time_seconds": round(processing_time, 2),
                "model_used": model_size or self.audio_processor.model_size,
                "file_size_bytes": file_info['file_size'],
                "audio_duration_seconds": transcription_result.get('duration', 0)
            }
            
            # Create transcript data
            transcript = {
                "full_text": transcription_result['text'],
                "language": transcription_result['language'],
                "duration_seconds": transcription_result['duration'],
                "segments": transcription_result['segments'],
                "segment_count": len(transcription_result['segments'])
            }
            
            # Create summary
            summary = {
                "total_action_items": len(action_items),
                "high_priority_items": len([item for item in action_items if item.priority == 'high']),
                "medium_priority_items": len([item for item in action_items if item.priority == 'medium']),
                "low_priority_items": len([item for item in action_items if item.priority == 'low']),
                "items_with_assignees": len([item for item in action_items if item.assignees != ['unspecified']]),
                "items_with_deadlines": len([item for item in action_items if item.deadlines != ['not specified']]),
                "average_confidence": round(
                    sum([item.confidence for item in action_items]) / len(action_items), 2
                ) if action_items else 0.0
            }
            
            # Create meeting analysis result
            meeting_analysis = MeetingAnalysis(
                metadata=metadata,
                transcript=transcript,
                action_items=action_items,
                summary=summary
            )
            
            logger.info(f"Audio processing completed in {processing_time:.2f}s")
            return meeting_analysis
            
        except Exception as e:
            logger.error(f"Audio processing failed: {e}")
            raise MeetingAnalyticsException(f"Audio processing failed: {str(e)}")
        
        finally:
            # Clean up uploaded file
            self.file_service.delete_file(file_info['file_path'])
