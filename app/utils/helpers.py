import os
import uuid
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from werkzeug.utils import secure_filename

logger = logging.getLogger(__name__)


def generate_file_id() -> str:
    """Generate unique file identifier"""
    return str(uuid.uuid4())


def create_secure_filename(original_filename: str, file_id: str) -> str:
    """Create secure filename with unique identifier"""
    secure_name = secure_filename(original_filename)
    file_extension = os.path.splitext(secure_name)[1]
    return f"{file_id}{file_extension}"


def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f}{size_names[i]}"


def format_duration(seconds: float) -> str:
    """Format duration in human readable format"""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        remaining_seconds = seconds % 60
        return f"{minutes}m {remaining_seconds:.1f}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        remaining_seconds = seconds % 60
        return f"{hours}h {minutes}m {remaining_seconds:.1f}s"


def safe_delete_file(file_path: str) -> bool:
    """Safely delete a file"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"File deleted: {file_path}")
            return True
        return False
    except Exception as e:
        logger.error(f"Failed to delete file {file_path}: {e}")
        return False


def create_response_metadata(
    file_id: str,
    original_filename: str,
    processing_start_time: datetime,
    model_used: str,
    file_size: int,
    duration: Optional[float] = None
) -> Dict[str, Any]:
    """Create standardized response metadata"""
    processing_time = (datetime.now() - processing_start_time).total_seconds()
    
    metadata = {
        "file_id": file_id,
        "original_filename": original_filename,
        "processed_at": datetime.now().isoformat(),
        "processing_time_seconds": round(processing_time, 2),
        "model_used": model_used,
        "file_size_bytes": file_size
    }
    
    if duration is not None:
        metadata["audio_duration_seconds"] = duration
    
    return metadata
