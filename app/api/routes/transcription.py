from flask import Blueprint, request, jsonify, current_app
from werkzeug.datastructures import FileStorage
import logging
from app.services.transcription_service import TranscriptionService
from app.models.responses import TranscriptionResponse, ErrorResponse
from app.core.exceptions import MeetingAnalyticsException

logger = logging.getLogger(__name__)
transcription_bp = Blueprint('transcription', __name__)


@transcription_bp.route('/transcribe', methods=['POST'])
def transcribe_audio():
    """Transcribe audio file endpoint"""
    try:
        # Check if file is in request
        if 'audio_file' not in request.files:
            return jsonify(ErrorResponse(
                error="FileUploadError",
                message="No audio file provided"
            ).dict()), 400
        
        file = request.files['audio_file']
        
        # Get optional parameters
        model_size = request.form.get('model_size', 'base')
        language = request.form.get('language', None)
        
        # Validate parameters
        valid_model_sizes = ['tiny', 'base', 'small', 'medium', 'large']
        if model_size not in valid_model_sizes:
            return jsonify(ErrorResponse(
                error="ValidationError",
                message=f"Invalid model size. Must be one of: {valid_model_sizes}"
            ).dict()), 400
        
        # Initialize transcription service
        transcription_service = TranscriptionService(current_app.config)
        
        # Save uploaded file
        file_info = transcription_service.file_service.save_file(file)
        
        logger.info(f"Processing transcription request for file: {file_info['file_id']}")
        
        # Process audio (transcription only, no action items)
        meeting_analysis = transcription_service.process_audio_file(
            file_info=file_info,
            model_size=model_size,
            language=language,
            extract_action_items=False
        )
        
        # Create response
        response = TranscriptionResponse(
            success=True,
            file_id=meeting_analysis.metadata['file_id'],
            transcript={
                "text": meeting_analysis.transcript['full_text'],
                "language": meeting_analysis.transcript['language'],
                "duration": meeting_analysis.transcript['duration_seconds'],
                "segments": meeting_analysis.transcript['segments']
            },
            metadata={
                "model_used": meeting_analysis.metadata['model_used'],
                "processing_time": meeting_analysis.metadata['processing_time_seconds'],
                "file_size": meeting_analysis.metadata['file_size_bytes'],
                "original_filename": meeting_analysis.metadata['original_filename']
            }
        )
        
        logger.info(f"Transcription completed for file: {file_info['file_id']}")
        return jsonify(response.dict()), 200
        
    except MeetingAnalyticsException as e:
        logger.error(f"Transcription failed: {e}")
        return jsonify(ErrorResponse(
            error=e.__class__.__name__,
            message=e.message
        ).dict()), e.status_code
        
    except Exception as e:
        logger.error(f"Unexpected error in transcription: {e}")
        return jsonify(ErrorResponse(
            error="InternalServerError",
            message="An unexpected error occurred during transcription"
        ).dict()), 500