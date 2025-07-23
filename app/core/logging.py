import logging
import logging.handlers
import os
from flask import Flask


def setup_logging(app: Flask):
    """Setup application logging"""
    log_level = getattr(logging, app.config['LOG_LEVEL'].upper())
    
    # Create logs directory if it doesn't exist
    log_dir = os.path.dirname(app.config['LOG_FILE'])
    os.makedirs(log_dir, exist_ok=True)
    
    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s %(levelname)s [%(name)s] %(message)s',
        handlers=[
            logging.handlers.RotatingFileHandler(
                app.config['LOG_FILE'],
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5
            ),
            logging.StreamHandler()
        ]
    )
    
    # Set specific logger levels
    logging.getLogger('werkzeug').setLevel(logging.WARNING)
    logging.getLogger('transformers').setLevel(logging.WARNING)
    logging.getLogger('torch').setLevel(logging.WARNING)

