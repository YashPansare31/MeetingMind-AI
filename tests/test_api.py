import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import os
import sys

# Add the backend directory to the path
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(current_dir, '..', 'backend')
sys.path.insert(0, backend_dir)

from app.main import app

client = TestClient(app)

def test_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "Meeting Analysis API V1" in response.json()["message"]

def test_health_check_without_openai():
    """Test health check without OpenAI key"""
    with patch.dict(os.environ, {}, clear=True):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["openai_configured"] == False

def test_health_check_with_openai():
    """Test health check with OpenAI key"""
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        # Import and recreate the service after setting the env var
        from app.services import MeetingAnalysisService
        test_service = MeetingAnalysisService()
        
        with patch('app.main.analysis_service', test_service):
            response = client.get("/health")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
            assert data["openai_configured"] == True

def test_analyze_endpoint_invalid_file():
    """Test analyze endpoint with invalid file type"""
    response = client.post(
        "/analyze",
        files={"file": ("test.txt", b"test content", "text/plain")}
    )
    assert response.status_code == 400
    assert "Invalid file type" in response.json()["detail"]

@patch('app.services.openai')
def test_analyze_endpoint_valid_file(mock_openai):
    """Test analyze endpoint with valid audio file"""
    # Mock OpenAI responses
    mock_transcript = MagicMock()
    mock_transcript.return_value = "This is a test meeting transcript."
    mock_openai.Audio.transcribe = mock_transcript
    
    mock_chat_response = MagicMock()
    mock_chat_response.choices = [MagicMock()]
    mock_chat_response.choices[0].message.content = "Test response"
    mock_openai.ChatCompletion.create.return_value = mock_chat_response
    
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        response = client.post(
            "/analyze",
            files={"file": ("test.mp3", b"fake audio data", "audio/mpeg")}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "transcription" in data
        assert "summary" in data
        assert "action_items" in data
        assert "decision_points" in data
        assert "processing_time" in data

if __name__ == "__main__":
    pytest.main([__file__])