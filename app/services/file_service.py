import os
import uuid
import logging
from typing import Optional, Dict, Any
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from app.core.exceptions import FileUploadError

logger = logging.getLogger(__name__)


class FileService:
    """Handles file upload, validation, and management"""
    
    def __init__(self, upload_folder: str, max_file_size: int, allowed_extensions: set):
        self.upload_folder = upload_folder
        self.max_file_size = max_file_size
        self.allowed_extensions = allowed_extensions
        
        # Create upload folder if it doesn't exist
        os.makedirs(upload_folder, exist_ok=True)
    
    def is_allowed_file(self, filename: str) -> bool:
        """Check if file extension is allowed"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.allowed_extensions
    
    def validate_file(self, file: FileStorage) -> Dict[str, Any]:
        """Validate uploaded file"""
        if not file:
            raise FileUploadError("No file provided")
        
        if file.filename == '':
            raise FileUploadError("No file selected")
        
        if not self.is_allowed_file(file.filename):
            raise FileUploadError(
                f"File type not allowed. Allowed types: {', '.join(self.allowed_extensions)}"
            )
        
        # Check file size (approximate check before saving)
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > self.max_file_size:
            raise FileUploadError(
                f"File size ({file_size} bytes) exceeds maximum allowed size ({self.max_file_size} bytes)"
            )
        
        return {
            "original_filename": file.filename,
            "file_size": file_size,
            "content_type": file.content_type
        }
    
    def save_file(self, file: FileStorage) -> Dict[str, Any]:
        """Save uploaded file and return file info"""
        logger.info(f"Saving uploaded file: {file.filename}")
        
        try:
            # Validate file
            file_info = self.validate_file(file)
            
            # Generate unique filename
            file_id = str(uuid.uuid4())
            original_filename = secure_filename(file.filename)
            file_extension = os.path.splitext(original_filename)[1]
            saved_filename = f"{file_id}{file_extension}"
            file_path = os.path.join(self.upload_folder, saved_filename)
            
            # Save file
            file.save(file_path)
            
            # Verify saved file
            if not os.path.exists(file_path):
                raise FileUploadError("Failed to save file")
            
            actual_file_size = os.path.getsize(file_path)
            
            result = {
                "file_id": file_id,
                "file_path": file_path,
                "saved_filename": saved_filename,
                "original_filename": original_filename,
                "file_size": actual_file_size,
                "content_type": file_info["content_type"]
            }
            
            logger.info(f"File saved successfully: {file_path}")
            return result
            
        except Exception as e:
            logger.error(f"File save failed: {e}")
            if isinstance(e, FileUploadError):
                raise
            else:
                raise FileUploadError(f"Failed to save file: {str(e)}")
    
    def delete_file(self, file_path: str) -> bool:
        """Delete file from storage"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"File deleted: {file_path}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to delete file {file_path}: {e}")
            return False
