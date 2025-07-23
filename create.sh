#!/bin/bash

# Create directories
mkdir -p backend/app
mkdir -p tests

# Create files for backend/app
touch backend/app/__init__.py
touch backend/app/main.py
touch backend/app/models.py
touch backend/app/services.py

# Create other backend files
touch backend/requirements.txt
touch backend/.env.example
touch backend/run.py

# Create test files
touch tests/__init__.py
touch tests/test_api.py
touch tests/sample_audio.mp3

# Create root-level files
touch .gitignore
touch README.md
touch docker-compose.yml

