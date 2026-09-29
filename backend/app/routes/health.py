"""
Health check route module for API status and model readiness monitoring.
"""

from fastapi import APIRouter
from app.services.prediction_service import get_model_and_features

router = APIRouter()


@router.get("/api/health", summary="Check backend service health & model readiness")
async def health_check():
    """
    Health check endpoint to verify backend service availability and ML model loading state.
    """
    model_loaded = False
    try:
        model, cols = get_model_and_features()
        if model is not None and cols is not None:
            model_loaded = True
    except Exception:
        model_loaded = False

    return {
        "status": "healthy" if model_loaded else "degraded",
        "service": "PhishGuard AI API",
        "model_loaded": model_loaded
    }
