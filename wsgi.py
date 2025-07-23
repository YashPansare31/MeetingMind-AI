"""
Production WSGI entry point
Usage with gunicorn: gunicorn wsgi:application
"""
from app import create_app
from app.core.config import ProductionConfig

application = create_app(ProductionConfig)

if __name__ == "__main__":
    application.run()
