#!/bin/bash

# Create directories
mkdir -p app/api/routes
mkdir -p app/api/middleware
mkdir -p app/core
mkdir -p app/services
mkdir -p app/models
mkdir -p app/utils
mkdir -p uploads
mkdir -p outputs
mkdir -p tests/test_api
mkdir -p tests/test_services
mkdir -p tests/fixtures
mkdir -p docker
mkdir -p scripts
mkdir -p docs

# Create files
touch app/__init__.py
touch app/api/__init__.py
touch app/api/routes/__init__.py
touch app/api/routes/health.py
touch app/api/routes/transcription.py
touch app/api/routes/analysis.py
touch app/api/middleware/__init__.py
touch app/api/middleware/auth.py
touch app/api/middleware/cors.py
touch app/api/middleware/error_handlers.py
touch app/core/__init__.py
touch app/core/config.py
touch app/core/logging.py
touch app/core/exceptions.py
touch app/services/__init__.py
touch app/services/audio_processor.py
touch app/services/transcription_service.py
touch app/services/nlp_service.py
touch app/services/file_service.py
touch app/models/__init__.py
touch app/models/requests.py
touch app/models/responses.py
touch app/models/entities.py
touch app/utils/__init__.py
touch app/utils/validators.py
touch app/utils/helpers.py
touch app/utils/decorators.py
touch uploads/.gitkeep
touch outputs/.gitkeep
touch tests/__init__.py
touch tests/conftest.py
touch tests/test_api/__init__.py
touch tests/test_api/test_health.py
touch tests/test_api/test_transcription.py
touch tests/test_services/__init__.py
touch tests/test_services/test_audio_processor.py
touch tests/test_services/test_nlp_service.py
touch tests/fixtures/sample_audio.mp3
touch docker/Dockerfile
touch docker/docker-compose.yml
touch docker/.dockerignore
touch scripts/setup.sh
touch scripts/run_dev.sh
touch scripts/test.sh
touch docs/API.md
touch docs/DEPLOYMENT.md
touch docs/DEVELOPMENT.md
touch .env.example
touch .env
touch .gitignore
touch requirements.txt
touch requirements-dev.txt
touch setup.py
touch wsgi.py
touch run.py
touch README.md


