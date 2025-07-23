"""
Development server entry point
Usage: python run.py
"""
from app import create_app
from app.core.config import DevelopmentConfig

if __name__ == '__main__':
    app = create_app(DevelopmentConfig)
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )