import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration class"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    FLASK_ENV = os.environ.get('FLASK_ENV') or 'development'
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Server configuration
    HOST = os.environ.get('HOST') or '0.0.0.0'
    PORT = int(os.environ.get('PORT') or 5000)
    
    # Audio processing configuration
    WHISPER_MODEL_SIZE = os.environ.get('WHISPER_MODEL_SIZE') or 'base'
    MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB in bytes
    ALLOWED_EXTENSIONS = {'mp3', 'wav', 'm4a', 'ogg', 'flac'}
    
    # Storage configuration
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or 'uploads'
    OUTPUT_FOLDER = os.environ.get('OUTPUT_FOLDER') or 'outputs'
    
    # Logging configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'INFO'
    LOG_FILE = os.environ.get('LOG_FILE') or 'logs/app.log'


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable must be set in production")


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    UPLOAD_FOLDER = 'test_uploads'
    OUTPUT_FOLDER = 'test_outputs'