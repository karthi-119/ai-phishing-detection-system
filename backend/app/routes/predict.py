"""
FastAPI Prediction Route Module for AI Phishing Detection System.

Defines POST /api/predict endpoint, Pydantic request/response models,
and security validation checks.
"""

from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from app.utils.url_validator import validate_and_normalize_url
from app.services.prediction_service import predict_url

router = APIRouter()


class URLRequest(BaseModel):
    """
    Request model for URL phishing prediction endpoint.
    """
    url: str = Field(
        ...,
        description="Target web URL to analyze",
        json_schema_extra={"example": "https://example.com"}
    )


class ModelInfo(BaseModel):
    name: str = Field("Random Forest Classifier", json_schema_extra={"example": "Random Forest Classifier"})
    algorithm: str = Field("Random Forest", json_schema_extra={"example": "Random Forest"})
    feature_count: int = Field(30, json_schema_extra={"example": 30})


class IndicatorItem(BaseModel):
    name: str = Field(..., json_schema_extra={"example": "Domain Hyphen"})
    severity: str = Field(..., json_schema_extra={"example": "medium"})
    description: str = Field(..., json_schema_extra={"example": "Domain contains a hyphen commonly used in brand spoofing."})
    detected: bool = Field(True, json_schema_extra={"example": True})


class TechniqueItem(BaseModel):
    technique: str = Field(..., json_schema_extra={"example": "IP-Based URL"})
    severity: str = Field(..., json_schema_extra={"example": "high"})
    description: str = Field(..., json_schema_extra={"example": "The URL uses a raw IP address instead of a domain name."})
    evidence: str = Field(..., json_schema_extra={"example": "Raw IP address used as host: 192.168.1.50"})


class PredictionResponse(BaseModel):
    """
    Enriched response model for URL phishing prediction endpoint (Phase 9).
    """
    success: bool = Field(..., json_schema_extra={"example": True})
    url: str = Field(..., json_schema_extra={"example": "https://example.com"})
    prediction: str = Field(..., description="likely_legitimate or likely_phishing", json_schema_extra={"example": "likely_legitimate"})
    risk_level: str = Field(..., description="low, medium, high, or critical", json_schema_extra={"example": "low"})
    risk_score: int = Field(..., description="AI Risk Score (0 to 100)", json_schema_extra={"example": 15})
    confidence: Optional[float] = Field(..., description="Confidence score percentage (0 - 100)", json_schema_extra={"example": 91.5})
    summary: str = Field(..., json_schema_extra={"example": "LOW RISK URL based on available URL-level evidence."})
    risk_indicators: List[IndicatorItem] = Field(..., description="List of structured risk indicators")
    phishing_techniques: List[TechniqueItem] = Field(default=[], description="List of detected phishing attack techniques")
    heuristic_analysis: Dict[str, Any] = Field(default={}, description="Advanced URL heuristic structure and pattern analysis")
    trust_analysis: Dict[str, Any] = Field(default={}, description="Offline trust and protocol analysis")
    analyzed_features: Dict[str, Any] = Field(..., description="Map of 30 extracted feature values (-1, 0, 1)")
    model: ModelInfo
    limitations: List[str] = Field(default=[], description="List of system limitations and security boundaries")


class ErrorResponse(BaseModel):
    """
    Standard error response model.
    """
    success: bool = Field(False, json_schema_extra={"example": False})
    error: str = Field(..., json_schema_extra={"example": "Invalid URL"})
    detail: str = Field(..., json_schema_extra={"example": "Only http:// and https:// protocol schemes are supported."})


@router.post(
    "/api/predict",
    response_model=PredictionResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid URL input or forbidden host"},
        422: {"model": ErrorResponse, "description": "Unprocessable request payload"},
        500: {"model": ErrorResponse, "description": "Internal prediction processing error"}
    },
    summary="Analyze URL and predict phishing likelihood",
    description="Extracts 30 URL features, evaluates Random Forest classifier, and returns explainable risk breakdown."
)
async def predict_phishing_url(payload: URLRequest):
    """
    POST /api/predict endpoint implementation.
    Validates target URL using server-side url_validator and returns model inference result.
    """
    # 1. Server-Side URL Validation & SSRF Check
    try:
        validated_url = validate_and_normalize_url(payload.url)
    except ValueError as val_err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(val_err)
        )

    # 2. Call prediction service
    try:
        result = predict_url(validated_url)
        return result
    except FileNotFoundError as fnf_err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction service failure: Model artifact not found. ({str(fnf_err)})"
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while analyzing the URL: {str(exc)}"
        )
