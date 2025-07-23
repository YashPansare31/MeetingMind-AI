import pytest
import tempfile
import os
from app.services.audio_processor import AudioProcessor
from app.core.exceptions import AudioProcessingError


@pytest.fixture
def audio_processor():
    """Create audio processor instance"""
    return AudioProcessor("tiny")  # Use smallest model for testing


def test_validate_audio_file_not_found(audio_processor):
    """Test validation with non-existent file"""
    with pytest.raises(AudioProcessingError):
        audio_processor.validate_audio_file("nonexistent.mp3")


def test_validate_audio_file_exists(audio_processor):
    """Test validation with existing file"""
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
        temp_file.write(b"fake audio content")
        temp_file_path = temp_file.name
    
    try:
        result = audio_processor.validate_audio_file(temp_file_path)
        
        assert result['file_path'] == temp_file_path
        assert result['file_size'] > 0
        assert result['file_extension'] == '.mp3'
    finally:
        os.unlink(temp_file_path)
