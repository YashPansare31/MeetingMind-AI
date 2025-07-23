from flask import jsonify
import logging
from app.models.responses import ErrorResponse
from app.core.exceptions import MeetingAnalyticsException

logger = logging.getLogger(__name__)


def register_error_handlers(app):
    """Register global error handlers"""
    
    @app.errorhandler(MeetingAnalyticsException)
    def handle_meeting_analytics_exception(e):
        """Handle custom application exceptions"""
        logger.error(f"Application error: {e}")
        return jsonify(ErrorResponse(
            error=e.__class__.__name__,
            message=e.message
        ).dict()), e.status_code
    
    @app.errorhandler(400)
    def handle_bad_request(e):
        """Handle bad request errors"""
        return jsonify(ErrorResponse(
            error="BadRequest",
            message="Invalid request format or parameters"
        ).dict()), 400
    
    @app.errorhandler(404)
    def handle_not_found(e):
        """Handle not found errors"""
        return jsonify(ErrorResponse(
            error="NotFound",
            message="The requested resource was not found"
        ).dict()), 404
    
    @app.errorhandler(405)
    def handle_method_not_allowed(e):
        """Handle method not allowed errors"""
        return jsonify(ErrorResponse(
            error="MethodNotAllowed",
            message="The method is not allowed for the requested URL"
        ).dict()), 405
    
    @app.errorhandler(413)
    def handle_payload_too_large(e):
        """Handle file too large errors"""
        return jsonify(ErrorResponse(
            error="PayloadTooLarge",
            message="The uploaded file is too large"
        ).dict()), 413
    
    @app.errorhandler(500)
    def handle_internal_server_error(e):
        """Handle internal server errors"""
        logger.error(f"Internal server error: {e}")
        return jsonify(ErrorResponse(
            error="InternalServerError",
            message="An unexpected error occurred"
        ).dict()), 500