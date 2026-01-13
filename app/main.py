"""
Adversarial Robustness Testing API

Main FastAPI application for testing ML model robustness against adversarial attacks.
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import logging
import logging.config
import torch
from pathlib import Path

from .config import API_CONFIG, LOGGING_CONFIG, MODEL_CONFIGS
from .schemas import (
    AttackRequest,
    AttackResponse,
    HealthResponse,
    HistoryResponse,
    ErrorResponse
)
from .evaluation import RobustnessTestRunner
from .storage import DatabaseManager

# Configure logging
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=API_CONFIG["title"],
    description=API_CONFIG["description"],
    version=API_CONFIG["version"],
    contact=API_CONFIG["contact"]
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
test_runner = RobustnessTestRunner(models_dir="models")
db_manager = DatabaseManager()

logger.info("🚀 Adversarial Robustness Testing API started")


@app.get("/", tags=["Health"])
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Adversarial Robustness Testing API",
        "version": API_CONFIG["version"],
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    
    Returns system status and available models.
    """
    # Check which models are available
    available_models = []
    for model_name, config in MODEL_CONFIGS.items():
        if Path(config["path"]).exists():
            available_models.append(model_name)
    
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        models_available=available_models,
        device=test_runner.device
    )


@app.post(
    "/run_attack",
    response_model=AttackResponse,
    status_code=status.HTTP_200_OK,
    tags=["Testing"],
    responses={
        200: {"description": "Attack executed successfully"},
        400: {"description": "Invalid request parameters", "model": ErrorResponse},
        404: {"description": "Model not found", "model": ErrorResponse},
        500: {"description": "Internal server error", "model": ErrorResponse}
    }
)
async def run_attack(request: AttackRequest):
    """
    Run an adversarial attack on a specified model.
    
    This endpoint executes an adversarial attack (FGSM or PGD) on a pre-trained model
    and returns robustness metrics.
    
    ## Parameters
    - **model_name**: Model to test ('cifar10_resnet20' or 'mnist_simplecnn')
    - **attack**: Attack type ('fgsm' or 'pgd')
    - **epsilon**: Perturbation budget (0.0 to 1.0)
    - **num_samples**: Number of test samples (default: 1000)
    - **batch_size**: Batch size for processing (default: 128)
    - **alpha**: Step size for PGD (default: epsilon/10)
    - **iters**: Iterations for PGD (default: 40)
    - **save_result**: Save to database (default: True)
    
    ## Returns
    - **clean_accuracy**: Accuracy on clean examples (%)
    - **robust_accuracy**: Accuracy on adversarial examples (%)
    - **attack_success_rate**: Success rate of attacks (%)
    - Additional metadata (timestamp, device, etc.)
    
    ## Example
    ```json
    {
      "model_name": "cifar10_resnet20",
      "attack": "pgd",
      "epsilon": 0.05
    }
    ```
    """
    try:
        logger.info(f"Received attack request: {request.model_name} - {request.attack} (ε={request.epsilon})")
        
        # Prepare attack kwargs
        attack_kwargs = {}
        if request.attack == "pgd":
            if request.alpha is not None:
                attack_kwargs["alpha"] = request.alpha
            if request.iters is not None:
                attack_kwargs["iters"] = request.iters
        
        # Run the attack
        result = test_runner.run_attack(
            model_name=request.model_name,
            attack=request.attack,
            epsilon=request.epsilon,
            num_samples=request.num_samples,
            batch_size=request.batch_size,
            **attack_kwargs
        )
        
        # Save to database if requested
        result_id = None
        if request.save_result:
            try:
                result_id = db_manager.save_result(result)
                logger.info(f"Result saved to database with ID: {result_id}")
            except Exception as e:
                logger.error(f"Failed to save result to database: {e}")
                # Continue even if save fails
        
        # Prepare response
        response = AttackResponse(
            clean_accuracy=result["clean_accuracy"],
            robust_accuracy=result["robust_accuracy"],
            attack_success_rate=result["attack_success_rate"],
            model_name=result["model_name"],
            attack=result["attack"],
            epsilon=result["epsilon"],
            total_samples=result["total_samples"],
            timestamp=result["timestamp"],
            device=result["device"],
            alpha=result.get("alpha"),
            iters=result.get("iters"),
            result_id=result_id
        )
        
        logger.info(f"Attack completed successfully: {response.model_name} - {response.attack}")
        return response
        
    except FileNotFoundError as e:
        logger.error(f"Model file not found: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ValueError as e:
        logger.error(f"Invalid request: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@app.get("/results/recent", response_model=HistoryResponse, tags=["Results"])
async def get_recent_results(limit: int = 10):
    """
    Get recent test results.
    
    Returns the most recent test results from the database.
    
    ## Parameters
    - **limit**: Maximum number of results to return (default: 10)
    """
    try:
        results = db_manager.get_recent_results(limit=limit)
        return HistoryResponse(
            total_results=len(results),
            results=results
        )
    except Exception as e:
        logger.error(f"Failed to fetch recent results: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.get("/results/model/{model_name}", response_model=HistoryResponse, tags=["Results"])
async def get_model_results(model_name: str):
    """
    Get all test results for a specific model.
    
    ## Parameters
    - **model_name**: Name of the model
    """
    try:
        results = db_manager.get_results_by_model(model_name)
        return HistoryResponse(
            total_results=len(results),
            results=results
        )
    except Exception as e:
        logger.error(f"Failed to fetch model results: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.get("/results/robustness_curve/{model_name}/{attack_type}", tags=["Results"])
async def get_robustness_curve(model_name: str, attack_type: str):
    """
    Get robustness curve data (accuracy vs epsilon).
    
    Returns aggregated data for plotting robustness curves.
    
    ## Parameters
    - **model_name**: Name of the model
    - **attack_type**: Type of attack ('fgsm' or 'pgd')
    """
    try:
        curve_data = db_manager.get_robustness_curve(model_name, attack_type)
        return {
            "model_name": model_name,
            "attack_type": attack_type,
            "data_points": len(curve_data),
            "curve": curve_data
        }
    except Exception as e:
        logger.error(f"Failed to fetch robustness curve: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("Shutting down API...")
    db_manager.close()
    logger.info("Database connection closed")


# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom handler for HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "timestamp": datetime.now().isoformat()
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Custom handler for general exceptions."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "detail": str(exc),
            "timestamp": datetime.now().isoformat()
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
