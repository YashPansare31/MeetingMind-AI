# run.py
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


# wsgi.py
"""
Production WSGI entry point
Usage with gunicorn: gunicorn wsgi:application
"""
from app import create_app
from app.core.config import ProductionConfig

application = create_app(ProductionConfig)

if __name__ == "__main__":
    application.run()


# setup.py
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="meeting-analytics-api",
    version="1.0.0",
    author="Meeting Analytics Team",
    author_email="team@meetinganalytics.com",
    description="AI-powered meeting analytics system for transcription and action item extraction",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-org/meeting-analytics-api",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-cov>=4.1.0",
            "black>=23.11.0",
            "flake8>=6.1.0",
            "mypy>=1.7.1",
        ]
    },
    entry_points={
        "console_scripts": [
            "meeting-analytics=run:main",
        ],
    },
)


# README.md
# Meeting Analytics API

AI-powered meeting analytics system that provides transcription and action item extraction from audio recordings.

## Features

- 🎙️ **Audio Transcription**: High-quality transcription using OpenAI Whisper
- 📋 **Action Item Extraction**: Automatic detection of tasks, assignees, and deadlines
- 🎯 **Priority Detection**: Classify action items by priority level
- 🔍 **Named Entity Recognition**: Extract people, dates, and important entities
- 🌐 **RESTful API**: Clean REST API for easy integration
- 🐳 **Docker Support**: Containerized deployment
- 📊 **Comprehensive Analytics**: Detailed summaries and metrics

## Quick Start

### Prerequisites

- Python 3.8+
- FFmpeg (for audio processing)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd meeting-analytics-api
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment**
   ```bash
   cp .env.example .env
   # Edit .env file with your configuration
   ```

5. **Create required directories**
   ```bash
   mkdir -p uploads outputs logs
   ```

### Running the Development Server

```bash
python run.py
```

The API will be available at `http://localhost:5000`

### API Endpoints

#### Health Check
```http
GET /api/health
```

#### Transcription Only
```http
POST /api/transcribe
Content-Type: multipart/form-data

{
  "audio_file": <file>,
  "model_size": "base",  // optional: tiny, base, small, medium, large
  "language": "en"       // optional: auto-detect if not provided
}
```

#### Complete Analysis
```http
POST /api/analyze
Content-Type: multipart/form-data

{
  "audio_file": <file>,
  "model_size": "base",           // optional
  "language": "en",               // optional
  "extract_action_items": "true", // optional
  "custom_keywords": "follow up,urgent,deadline"  // optional
}
```

#### Text-only Analysis
```http
POST /api/analyze/text
Content-Type: application/json

{
  "text": "John needs to follow up with the client by Friday...",
  "custom_keywords": ["follow up", "urgent"]  // optional
}
```

### Example Response

```json
{
  "success": true,
  "file_id": "abc123",
  "metadata": {
    "processed_at": "2025-01-23T10:30:00Z",
    "processing_time": 25.5,
    "model_used": "base",
    "original_filename": "meeting.mp3"
  },
  "transcript": {
    "text": "Let's start the meeting. John, you need to follow up with the client by Friday...",
    "language": "en",
    "duration": 300.0
  },
  "action_items": [
    {
      "id": 1,
      "task": "John needs to follow up with the client by Friday",
      "assignees": ["John"],
      "deadlines": ["by Friday"],
      "priority": "medium",
      "confidence": 0.85
    }
  ],
  "summary": {
    "total_action_items": 5,
    "high_priority_items": 1,
    "items_with_assignees": 3,
    "items_with_deadlines": 2
  }
}
```

## Testing

### Run Unit Tests
```bash
pytest
```

### Run with Coverage
```bash
pytest --cov=app tests/
```

### Run Specific Tests
```bash
pytest tests/test_api/test_transcription.py
```

## Docker Deployment

### Build Image
```bash
docker build -t meeting-analytics-api .
```

### Run Container
```bash
docker run -p 5000:5000 \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/outputs:/app/outputs \
  meeting-analytics-api
```

### Using Docker Compose
```bash
docker-compose up -d
```

## Production Deployment

### Using Gunicorn
```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 wsgi:application
```

### Environment Variables for Production
```bash
export FLASK_ENV=production
export SECRET_KEY=your-production-secret-key
export WHISPER_MODEL_SIZE=base
export MAX_FILE_SIZE=100MB
```

## Configuration

### Whisper Model Sizes
- **tiny**: Fastest, least accurate (~39 MB)
- **base**: Good balance (~74 MB) - **Recommended for MVP**
- **small**: Better accuracy (~244 MB)
- **medium**: High accuracy (~769 MB)
- **large**: Best accuracy (~1550 MB)

### Supported Audio Formats
- MP3
- WAV
- M4A
- OGG
- FLAC

## API Documentation

### Error Responses
All endpoints return consistent error responses:

```json
{
  "success": false,
  "error": "FileUploadError",
  "message": "File size exceeds maximum limit",
  "details": {
    "max_size": "100MB",
    "uploaded_size": "150MB"
  }
}
```

### Status Codes
- `200`: Success
- `400`: Bad Request / Validation Error
- `413`: File Too Large
- `422`: Processing Error
- `500`: Internal Server Error

## Development

### Project Structure
```
meeting-analytics-api/
├── app/                    # Main application package
│   ├── api/               # API routes and middleware
│   ├── core/              # Core configuration and utilities
│   ├── services/          # Business logic services
│   ├── models/            # Data models and schemas
│   └── utils/             # Helper utilities
├── tests/                 # Test suite
├── docker/                # Docker configuration
├── scripts/               # Development scripts
└── docs/                  # Documentation
```

### Code Style
```bash
# Format code
black app/ tests/

# Check linting
flake8 app/ tests/

# Type checking
mypy app/
```

### Adding New Features

1. **Create service in `app/services/`**
2. **Add data models in `app/models/`**
3. **Create API routes in `app/api/routes/`**
4. **Add tests in `tests/`**
5. **Update documentation**

## Performance Tuning

### CPU Optimization
- Use `tiny` or `base` Whisper models for faster processing
- Implement request queuing for high load
- Consider caching frequently processed files

### Memory Management
- Models are lazy-loaded to save memory
- Files are cleaned up after processing
- Consider using smaller batch sizes for large files

### Scaling
- Use multiple worker processes (Gunicorn)
- Implement Redis for caching
- Consider GPU acceleration for production

## Monitoring

### Health Checks
- `/api/health` - Basic health check
- `/api/health/models` - Model loading status

### Logging
- Application logs: `logs/app.log`
- Rotating logs (10MB, 5 backups)
- JSON structured logging for production

### Metrics to Monitor
- Request processing time
- File upload success rate
- Model inference time
- Memory usage
- Disk space (uploads/outputs)

## Troubleshooting

### Common Issues

1. **FFmpeg not found**
   ```bash
   # Ubuntu/Debian
   sudo apt install ffmpeg
   
   # macOS
   brew install ffmpeg
   ```

2. **Out of memory errors**
   - Use smaller Whisper model (`tiny` or `base`)
   - Reduce batch size
   - Add swap space

3. **Slow processing**
   - Use `tiny` model for development
   - Check available CPU cores
   - Monitor disk I/O

4. **File upload failures**
   - Check file size limits
   - Verify supported formats
   - Check disk space

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support and questions:
- Create an issue on GitHub
- Check the documentation in `docs/`
- Review the API examples in `tests/`
