class MeetingAnalyticsException(Exception):
    """Base exception for the application"""
    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class AudioProcessingError(MeetingAnalyticsException):
    """Raised when audio processing fails"""
    def __init__(self, message: str = "Audio processing failed"):
        super().__init__(message, 422)


class TranscriptionError(MeetingAnalyticsException):
    """Raised when transcription fails"""
    def __init__(self, message: str = "Transcription failed"):
        super().__init__(message, 422)


class NLPProcessingError(MeetingAnalyticsException):
    """Raised when NLP processing fails"""
    def __init__(self, message: str = "NLP processing failed"):
        super().__init__(message, 422)


class FileUploadError(MeetingAnalyticsException):
    """Raised when file upload fails"""
    def __init__(self, message: str = "File upload failed"):
        super().__init__(message, 400)


class ValidationError(MeetingAnalyticsException):
    """Raised when request validation fails"""
    def __init__(self, message: str = "Validation failed"):
        super().__init__(message, 400)