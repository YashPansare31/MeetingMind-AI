from flask import Blueprint, jsonify
from datetime import datetime
from app.models.responses import HealthResponse

health_bp = Blueprint('health', __name__)


@health_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    response = HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        version="1.0.0"
    )
    return jsonify(response.dict()), 200


@health_bp.route('/health/models', methods=['GET'])
def models_health():
    """Check if ML models are loaded and healthy"""
    try:
        from app.services.audio_processor import AudioProcessor
        from app.services.nlp_service import NLPService
        
        # Quick model check
        audio_processor = AudioProcessor("tiny")  # Use smallest model for health check
        nlp_service = NLPService()
        
        # Test if models can be accessed
        model_status = {
            "whisper_model": "loaded" if audio_processor._model else "not_loaded",
            "ner_model": "loaded" if nlp_service._ner_pipeline else "not_loaded"
        }
        
        return jsonify({
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "models": model_status
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }), 500
