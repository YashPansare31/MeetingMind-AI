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

