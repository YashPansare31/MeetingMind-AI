import functools
import logging
import time
from typing import Callable, Any
from flask import request, jsonify
from app.models.responses import ErrorResponse

logger = logging.getLogger(__name__)


def log_api_call(func: Callable) -> Callable:
    """Decorator to log API calls"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        
        logger.info(f"API call: {request.method} {request.path}")
        
        try:
            result = func(*args, **kwargs)
            processing_time = time.time() - start_time
            logger.info(f"API call completed in {processing_time:.2f}s")
            return result
        except Exception as e:
            processing_time = time.time() - start_time
            logger.error(f"API call failed after {processing_time:.2f}s: {e}")
            raise
    
    return wrapper


def validate_json_request(required_fields: list = None):
    """Decorator to validate JSON request data"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not request.is_json:
                return jsonify(ErrorResponse(
                    error="ValidationError",
                    message="Request must be JSON"
                ).dict()), 400
            
            data = request.get_json()
            if not data:
                return jsonify(ErrorResponse(
                    error="ValidationError",
                    message="Request body cannot be empty"
                ).dict()), 400
            
            if required_fields:
                missing_fields = [field for field in required_fields if field not in data]
                if missing_fields:
                    return jsonify(ErrorResponse(
                        error="ValidationError",
                        message=f"Missing required fields: {', '.join(missing_fields)}"
                    ).dict()), 400
            
            return func(*args, **kwargs)
        return wrapper
    return decorator


def handle_file_cleanup(file_path_key: str = 'file_path'):
    """Decorator to ensure file cleanup after processing"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            file_path = None
            try:
                result = func(*args, **kwargs)
                # Try to get file path from result if it's a dict
                if isinstance(result, dict) and file_path_key in result:
                    file_path = result[file_path_key]
                return result
            except Exception as e:
                logger.error(f"Function {func.__name__} failed: {e}")
                raise
            finally:
                if file_path and os.path.exists(file_path):
                    safe_delete_file(file_path)
        return wrapper
    return decorator