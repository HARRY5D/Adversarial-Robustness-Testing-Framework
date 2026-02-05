"""
Pydantic Schemas for API Request/Response Models

Defines the data structures for API endpoints.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime


class AttackRequest(BaseModel):
    """Request model for running an adversarial attack."""
    
    model_name: str = Field(
        ...,
        description="Name of the model to test",
        example="cifar10_resnet20"
    )
    attack: str = Field(
        ...,
        description="Type of adversarial attack",
        example="pgd"
    )
    epsilon: float = Field(
        ...,
        description="Perturbation budget (L-infinity norm)",
        example=0.05,
        gt=0,
        le=1.0
    )
    num_samples: Optional[int] = Field(
        1000,
        description="Number of test samples to use (default: 1000)",
        example=1000,
        gt=0,
        le=10000
    )
    batch_size: Optional[int] = Field(
        128,
        description="Batch size for processing (default: 128)",
        example=128,
        gt=0,
        le=512
    )
    alpha: Optional[float] = Field(
        None,
        description="Step size for PGD attack (default: epsilon/10)",
        example=0.01,
        gt=0
    )
    iters: Optional[int] = Field(
        40,
        description="Number of iterations for PGD attack (default: 40)",
        example=40,
        gt=0,
        le=100
    )
    save_result: Optional[bool] = Field(
        True,
        description="Whether to save result to database (default: True)",
        example=True
    )
    
    @validator('model_name')
    def validate_model_name(cls, v):
        valid_models = ['cifar10_resnet20', 'mnist_simplecnn']
        if v not in valid_models:
            raise ValueError(f"model_name must be one of {valid_models}")
        return v
    
    @validator('attack')
    def validate_attack(cls, v):
        valid_attacks = ['fgsm', 'pgd']
        if v.lower() not in valid_attacks:
            raise ValueError(f"attack must be one of {valid_attacks}")
        return v.lower()
    
    class Config:
        schema_extra = {
            "example": {
                "model_name": "cifar10_resnet20",
                "attack": "pgd",
                "epsilon": 0.05,
                "num_samples": 1000,
                "batch_size": 128,
                "alpha": 0.01,
                "iters": 40,
                "save_result": True
            }
        }


class AttackResponse(BaseModel):
    """Response model for attack execution results."""
    
    clean_accuracy: float = Field(
        ...,
        description="Accuracy on clean (unperturbed) examples (%)",
        example=92.3
    )
    robust_accuracy: float = Field(
        ...,
        description="Accuracy on adversarial examples (%)",
        example=12.1
    )
    attack_success_rate: float = Field(
        ...,
        description="Percentage of successful attacks on correctly classified examples (%)",
        example=86.9
    )
    model_name: str = Field(
        ...,
        description="Model that was tested",
        example="cifar10_resnet20"
    )
    attack: str = Field(
        ...,
        description="Attack type used",
        example="pgd"
    )
    epsilon: float = Field(
        ...,
        description="Perturbation budget used",
        example=0.05
    )
    total_samples: int = Field(
        ...,
        description="Number of samples evaluated",
        example=1000
    )
    timestamp: str = Field(
        ...,
        description="ISO timestamp of the test",
        example="2024-01-13T10:30:00"
    )
    device: str = Field(
        ...,
        description="Device used for computation",
        example="cuda"
    )
    alpha: Optional[float] = Field(
        None,
        description="Step size (for PGD)",
        example=0.01
    )
    iters: Optional[int] = Field(
        None,
        description="Number of iterations (for PGD)",
        example=40
    )
    result_id: Optional[int] = Field(
        None,
        description="Database ID if result was saved",
        example=42
    )
    
    class Config:
        schema_extra = {
            "example": {
                "clean_accuracy": 92.3,
                "robust_accuracy": 12.1,
                "attack_success_rate": 86.9,
                "model_name": "cifar10_resnet20",
                "attack": "pgd",
                "epsilon": 0.05,
                "total_samples": 1000,
                "timestamp": "2024-01-13T10:30:00",
                "device": "cuda",
                "alpha": 0.01,
                "iters": 40,
                "result_id": 42
            }
        }


class HealthResponse(BaseModel):
    """Response model for health check endpoint."""
    
    status: str = Field(..., example="healthy")
    timestamp: str = Field(..., example="2024-01-13T10:30:00")
    models_available: List[str] = Field(..., example=["cifar10_resnet20", "mnist_simplecnn"])
    device: str = Field(..., example="cuda")


class HistoryResponse(BaseModel):
    """Response model for historical results."""
    
    total_results: int = Field(..., description="Total number of results", example=10)
    results: List[dict] = Field(..., description="List of test results")


class ErrorResponse(BaseModel):
    """Response model for errors."""
    
    error: str = Field(..., description="Error message", example="Model file not found")
    detail: Optional[str] = Field(None, description="Detailed error information")
    timestamp: str = Field(..., example="2024-01-13T10:30:00")
