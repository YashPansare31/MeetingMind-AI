import os
from typing import Optional, List
from werkzeug.datastructures import FileStorage
from app.core.exceptions import ValidationError


def validate_file_upload(file: FileStorage, allowed_extensions: set, max_size: int) -> None:
    """Validate uploaded file"""
    if not file:
        raise ValidationError("No file provided")
    
    if file.filename == '':
        raise ValidationError("No file selected")
    
    # Check file extension
    if not ('.' in file.filename and 
            file.filename.rsplit('.', 1)[1].lower() in allowed_extensions):
        raise ValidationError(f"File type not allowed. Allowed types: {', '.join(allowed_extensions)}")
    
    # Check file size
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    
    if file_size > max_size:
        raise ValidationError(f"File size exceeds maximum limit of {max_size} bytes")


def validate_whisper_model_size(model_size: str) -> None:
    """Validate Whisper model size parameter"""
    valid_sizes = ['tiny', 'base', 'small', 'medium', 'large']
    if model_size not in valid_sizes:
        raise ValidationError(f"Invalid model size. Must be one of: {valid_sizes}")


def validate_custom_keywords(keywords: Optional[List[str]]) -> Optional[List[str]]:
    """Validate and clean custom keywords"""
    if not keywords:
        return None
    
    cleaned_keywords = []
    for keyword in keywords:
        if isinstance(keyword, str) and keyword.strip():
            cleaned_keywords.append(keyword.strip().lower())
    
    return cleaned_keywords if cleaned_keywords else None

