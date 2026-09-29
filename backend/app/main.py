"""
Main Entry Point for the FastAPI Backend Application.
Configures CORS middleware, security headers, request logging, exception handlers, and API routers.
"""

import time
import logging
from fastapi import FastAPI, Request, Response, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.config import API_NAME, API_VERSION, CORS_ORIGINS

# Configure safe application logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("phishguard_api")

# Instantiate FastAPI application with metadata
app = FastAPI(
    title=API_NAME,
    description=(
        "Real-Time AI Phishing Detection System API powered by Random Forest Classifier. "
        "Extracts 30 URL features, evaluates phishing risk levels, and generates explainable risk reports."
    ),
    version=API_VERSION
)

# CORS Configuration for local frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


# Global Exception Handlers to prevent exposing internal stack traces
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.warning(f"HTTPException [{exc.status_code}] on {request.url.path}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": "INVALID_INPUT" if exc.status_code in [400, 422] else "SERVER_ERROR",
                "message": str(exc.detail)
            },
            "detail": str(exc.detail)
        }
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled Internal Error on {request.url.path}: {str(exc)}", exc_info=False)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected server error occurred while processing the request."
            },
            "detail": "An unexpected server error occurred while processing the request."
        }
    )


# Security Headers & Safe Request Logging Middleware
@app.middleware("http")
async def security_and_logging_middleware(request: Request, call_next):
    start_time = time.time()
    response: Response = await call_next(request)
    duration_ms = round((time.time() - start_time) * 1000, 2)
    
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"

    logger.info(
        f"Method={request.method} Path={request.url.path} Status={response.status_code} Duration={duration_ms}ms"
    )

    return response


# Register Routers lazily to ensure clean exception handling
from app.routes.health import router as health_router
from app.routes.predict import router as predict_router
from app.routes.insights import router as insights_router

app.include_router(health_router)
app.include_router(predict_router)
app.include_router(insights_router)


# Root route welcoming developers to the API
@app.get("/", summary="API Root Welcome Endpoint")
async def root():
    """
    Root endpoint returning basic information about the API service.
    """
    return {
        "message": f"Welcome to {API_NAME}",
        "version": API_VERSION,
        "docs_url": "/docs",
        "health_check": "/api/health",
        "predict_endpoint": "POST /api/predict",
        "insights_endpoint": "GET /api/model/insights"
    }
