import pytest
import tempfile
import os
from app import create_app
from app.core.config import TestingConfig


@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app(TestingConfig)
    
    # Create temporary directories for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        app.config['UPLOAD_FOLDER'] = os.path.join(temp_dir, 'uploads')
        app.config['OUTPUT_FOLDER'] = os.path.join(temp_dir, 'outputs')
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)
        
        yield app


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


@pytest.fixture
def sample_text():
    """Sample meeting text for testing"""
    return """
    Good morning everyone, let's start our weekly team meeting.
    First item - John, you need to follow up with the Miller account by this Friday.
    Sarah, can you please prepare the quarterly budget report and send it to finance by next Tuesday?
    We have an urgent issue with the server - Mike, you should investigate this immediately and report back by end of day.
    Action item for everyone: review the new policy document before our meeting next week.
    Lisa will schedule a follow-up with the client and send calendar invites by tomorrow.
    High priority - we must deliver the project proposal to the client by Monday.
    That concludes our meeting, thank you all.
    """
