from flask import Flask
from flask_cors import CORS
from app.core.config import Config
from app.core.logging import setup_logging
from app.api.middleware.error_handlers import register_error_handlers
import os


def create_app(config_class=Config):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Setup logging
    setup_logging(app)
    
    # Initialize extensions
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:3000", "http://127.0.0.1:3000"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Create required directories
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    
    # Register blueprints
    from app.api.routes.health import health_bp
    from app.api.routes.transcription import transcription_bp
    from app.api.routes.analysis import analysis_bp
    
    app.register_blueprint(health_bp, url_prefix='/api')
    app.register_blueprint(transcription_bp, url_prefix='/api')
    app.register_blueprint(analysis_bp, url_prefix='/api')
    
    # Register error handlers
    register_error_handlers(app)
    
    return app