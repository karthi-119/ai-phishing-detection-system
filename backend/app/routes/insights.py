"""
FastAPI Model Insights Route Module.

Defines GET /api/model/insights endpoint returning Top 10 feature importances
and algorithm metadata from the trained Random Forest model.
"""

from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
import pandas as pd
from app.services.prediction_service import get_model_and_features

router = APIRouter()


class FeatureImportanceItem(BaseModel):
    feature: str = Field(..., json_schema_extra={"example": "sslfinal_state"})
    importance: float = Field(..., json_schema_extra={"example": 0.3285})


class ModelInsightsResponse(BaseModel):
    success: bool = Field(True, json_schema_extra={"example": True})
    model: str = Field("Random Forest Classifier", json_schema_extra={"example": "Random Forest Classifier"})
    dataset: str = Field("UCI Phishing Websites Dataset (ID: 327)", json_schema_extra={"example": "UCI Phishing Websites Dataset (ID: 327)"})
    feature_count: int = Field(30, json_schema_extra={"example": 30})
    top_features: List[FeatureImportanceItem]


@router.get(
    "/api/model/insights",
    response_model=ModelInsightsResponse,
    summary="Get trained model insights & feature importances",
    description="Returns top 10 feature importance values extracted from the Random Forest model Gini impurity calculations."
)
async def get_model_insights():
    """
    GET /api/model/insights endpoint implementation.
    Reads trained model feature importances and returns top 10 features.
    """
    try:
        model, feature_columns = get_model_and_features()
        importances = model.feature_importances_

        # Pair features with importances and sort descending
        fi_pairs = [
            {"feature": col, "importance": round(float(imp), 4)}
            for col, imp in zip(feature_columns, importances)
        ]
        fi_pairs.sort(key=lambda x: x["importance"], reverse=True)

        top_10 = fi_pairs[:10]

        return {
            "success": True,
            "model": "Random Forest Classifier",
            "dataset": "UCI Phishing Websites Dataset (ID: 327)",
            "feature_count": len(feature_columns),
            "top_features": top_10
        }
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to load model insights: {str(exc)}"
        )
