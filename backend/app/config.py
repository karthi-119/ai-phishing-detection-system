"""
Centralized Application Configuration Module for PhishGuard AI Backend.

Reads settings from environment variables with safe defaults for development.
"""

import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ML_MODELS_DIR = BASE_DIR / "ml" / "models"

# Environment Settings
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DEBUG = os.getenv("DEBUG", "false").lower() in ("true", "1", "t")

# Network & Server Settings
API_HOST = os.getenv("API_HOST", "127.0.0.1")
API_PORT = int(os.getenv("API_PORT", "8000"))
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")

# Application Metadata
API_NAME = "PhishGuard AI API"
API_VERSION = "1.0.0"

# CORS Allowed Origins
CORS_ORIGINS = [
    FRONTEND_ORIGIN,
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000"
]

# Validation Constraints
MAX_URL_LENGTH = int(os.getenv("MAX_URL_LENGTH", "2048"))

# ML Artifact Paths
MODEL_PATH = Path(os.getenv("MODEL_PATH", str(ML_MODELS_DIR / "phishing_rf_model.pkl")))
FEATURE_COLS_PATH = Path(os.getenv("FEATURE_COLS_PATH", str(ML_MODELS_DIR / "feature_columns.pkl")))
METADATA_PATH = Path(os.getenv("METADATA_PATH", str(ML_MODELS_DIR / "model_metadata.json")))
