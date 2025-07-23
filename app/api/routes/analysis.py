from flask import Blueprint, request, jsonify, current_app
import logging
from app.services.transcription_service import TranscriptionService
from app.models.responses import AnalysisResponse, ActionItemResponse, ErrorResponse
from app.core.exceptions import MeetingAnalyticsException

logger = logging.getLogger(__name__)
analysis_bp = Blueprint('analysis', __name__)


@analysis_bp.route('/analyze', methods=['POST'])
def analyze_meeting():
    """Complete meeting analysis endpoint (transcription + action items)"""
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
        extract_action_items = request.form.get('extract_action_items', 'true').lower() == 'true'
        
        # Parse custom keywords if provided
        custom_keywords = None
        if 'custom_keywords' in request.form:
            custom_keywords = [kw.strip() for kw in request.form['custom_keywords'].split(',') if kw.strip()]
        
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
        
        logger.info(f"Processing analysis request for file: {file_info['file_id']}")
        
        # Process audio with full analysis
        meeting_analysis = transcription_service.process_audio_file(
            file_info=file_info,
            model_size=model_size,
            language=language,
            extract_action_items=extract_action_items,
            custom_keywords=custom_keywords
        )
        
        # Convert action items to response format
        action_items_response = []
        for item in meeting_analysis.action_items:
            action_items_response.append(ActionItemResponse(
                id=item.id,
                task=item.task,
                assignees=item.assignees,
                deadlines=item.deadlines,
                priority=item.priority,
                confidence=item.confidence
            ))
        
        # Create response
        response = AnalysisResponse(
            success=True,
            file_id=meeting_analysis.metadata['file_id'],
            metadata={
                "processed_at": meeting_analysis.metadata['processed_at'],
                "processing_time": meeting_analysis.metadata['processing_time_seconds'],
                "model_used": meeting_analysis.metadata['model_used'],
                "original_filename": meeting_analysis.metadata['original_filename'],
                "file_size": meeting_analysis.metadata['file_size_bytes']
            },
            transcript={
                "text": meeting_analysis.transcript['full_text'],
                "language": meeting_analysis.transcript['language'],
                "duration": meeting_analysis.transcript['duration_seconds'],
                "segment_count": meeting_analysis.transcript['segment_count']
            },
            action_items=action_items_response,
            summary=meeting_analysis.summary
        )
        
        logger.info(f"Analysis completed for file: {file_info['file_id']}")
        return jsonify(response.dict()), 200
        
    except MeetingAnalyticsException as e:
        logger.error(f"Analysis failed: {e}")
        return jsonify(ErrorResponse(
            error=e.__class__.__name__,
            message=e.message
        ).dict()), e.status_code
        
    except Exception as e:
        logger.error(f"Unexpected error in analysis: {e}")
        return jsonify(ErrorResponse(
            error="InternalServerError",
            message="An unexpected error occurred during analysis"
        ).dict()), 500


@analysis_bp.route('/analyze/text', methods=['POST'])
def analyze_text():
    """Analyze text directly (no audio transcription)"""
    try:
        # Get JSON data
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify(ErrorResponse(
                error="ValidationError",
                message="Text field is required"
            ).dict()), 400
        
        text = data['text']
        custom_keywords = data.get('custom_keywords', None)
        
        if not text.strip():
            return jsonify(ErrorResponse(
                error="ValidationError",
                message="Text cannot be empty"
            ).dict()), 400
        
        # Initialize NLP service
        from app.services.nlp_service import NLPService
        nlp_service = NLPService()
        
        logger.info("Processing text analysis request")
        
        # Extract action items
        action_items = nlp_service.extract_action_items(text, custom_keywords)
        
        # Convert to response format
        action_items_response = []
        for item in action_items:
            action_items_response.append(ActionItemResponse(
                id=item.id,
                task=item.task,
                assignees=item.assignees,
                deadlines=item.deadlines,
                priority=item.priority,
                confidence=item.confidence
            ))
        
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
        
        response = {
            "success": True,
            "text_length": len(text),
            "action_items": [item.dict() for item in action_items_response],
            "summary": summary
        }
        
        logger.info("Text analysis completed")
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Text analysis failed: {e}")
        return jsonify(ErrorResponse(
            error="InternalServerError",
            message="An unexpected error occurred during text analysis"
        ).dict()), 500

