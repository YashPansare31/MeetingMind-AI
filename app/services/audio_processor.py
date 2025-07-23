import os
import whisper
import logging
from typing import Dict, Any, Optional
from app.core.exceptions import AudioProcessingError, TranscriptionError

logger = logging.getLogger(__name__)


class AudioProcessor:
    """Handles audio file processing and transcription"""
    
    def __init__(self, model_size: str = "base"):
        self.model_size = model_size
        self._model = None
        
    @property
    def model(self):
        """Lazy load Whisper model"""
        if self._model is None:
            logger.info(f"Loading Whisper {self.model_size} model...")
            try:
                self._model = whisper.load_model(self.model_size)
                logger.info("Whisper model loaded successfully")
            except Exception as e:
                logger.error(f"Failed to load Whisper model: {e}")
                raise AudioProcessingError(f"Failed to load Whisper model: {str(e)}")
        return self._model
    
    def validate_audio_file(self, file_path: str) -> Dict[str, Any]:
        """Validate audio file exists and get basic info"""
        if not os.path.exists(file_path):
            raise AudioProcessingError(f"Audio file not found: {file_path}")
        
        file_size = os.path.getsize(file_path)
        file_extension = os.path.splitext(file_path)[1].lower()
        
        return {
            "file_path": file_path,
            "file_size": file_size,
            "file_extension": file_extension
        }
    
    def transcribe_audio(self, file_path: str, language: Optional[str] = None) -> Dict[str, Any]:
        """Transcribe audio file using Whisper"""
        logger.info(f"Starting transcription for: {file_path}")
        
        try:
            # Validate file
            file_info = self.validate_audio_file(file_path)
            
            # Transcribe
            result = self.model.transcribe(
                file_path,
                language=language,
                verbose=False
            )
            
            # Process segments
            processed_segments = []
            if 'segments' in result:
                for i, segment in enumerate(result['segments']):
                    processed_segments.append({
                        'id': i + 1,
                        'start': segment.get('start', 0),
                        'end': segment.get('end', 0),
                        'text': segment.get('text', '').strip()
                    })
            
            transcription_result = {
                'text': result.get('text', '').strip(),
                'language': result.get('language', 'unknown'),
                'duration': result.get('duration', 0),
                'segments': processed_segments,
                'file_info': file_info
            }
            
            logger.info(f"Transcription completed. Duration: {transcription_result['duration']:.1f}s")
            return transcription_result
            
        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            raise TranscriptionError(f"Transcription failed: {str(e)}")
