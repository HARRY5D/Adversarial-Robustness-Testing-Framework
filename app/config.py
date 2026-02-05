"""
Configuration Module

Central configuration for the adversarial robustness testing framework.
"""

from pathlib import Path
from typing import Dict, List

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"
DATA_DIR = BASE_DIR / "data"
DB_PATH = BASE_DIR / "results.db"

# Model configurations
MODEL_CONFIGS = {
    "cifar10_resnet20": {
        "path": MODELS_DIR / "cifar10_resnet20.pth",
        "dataset": "cifar10",
        "num_classes": 10,
        "input_shape": (3, 32, 32),
        "normalization": {
            "mean": [0.4914, 0.4822, 0.4465],
            "std": [0.2471, 0.2435, 0.2616]
        },
        "default_epsilons": [0.01, 0.03, 0.05, 0.1]
    },
    "mnist_simplecnn": {
        "path": MODELS_DIR / "mnist_simplecnn.pth",
        "dataset": "mnist",
        "num_classes": 10,
        "input_shape": (1, 28, 28),
        "normalization": {
            "mean": [0.1307],
            "std": [0.3081]
        },
        "default_epsilons": [0.05, 0.1, 0.2, 0.3]
    }
}

# Attack configurations
ATTACK_CONFIGS = {
    "fgsm": {
        "name": "Fast Gradient Sign Method",
        "params": {}
    },
    "pgd": {
        "name": "Projected Gradient Descent",
        "params": {
            "alpha": None,  # Will be set to epsilon/10 if not provided
            "iters": 40
        }
    }
}

# API configurations
API_CONFIG = {
    "title": "Adversarial Robustness Testing API",
    "description": """
    A production-ready API for testing ML model robustness against adversarial attacks.
    
    This service evaluates the security of machine learning models by testing them
    against adversarial perturbations using FGSM and PGD attacks.
    
    ## Features
    - Test pre-trained models (CIFAR-10 ResNet20, MNIST SimpleCNN)
    - Run FGSM and PGD adversarial attacks
    - Calculate robustness metrics (clean accuracy, robust accuracy, ASR)
    - Store and retrieve historical test results
    - Generate robustness reports
    
    ## Supported Models
    - `cifar10_resnet20`: ResNet20 trained on CIFAR-10
    - `mnist_simplecnn`: SimpleCNN trained on MNIST
    
    ## Supported Attacks
    - `fgsm`: Fast Gradient Sign Method (single-step)
    - `pgd`: Projected Gradient Descent (iterative, stronger)
    """,
    "version": "1.0.0",
    "contact": {
        "name": "MLOps Security Team",
        "email": "security@mlops.example.com"
    }
}

# Testing configurations
TEST_CONFIG = {
    "default_batch_size": 128,
    "default_num_samples": 1000,  # Limit for faster API responses
    "max_num_samples": 10000,
    "timeout_seconds": 300  # 5 minutes
}

# Logging configuration
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": "INFO"
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": "robustness_tests.log",
            "formatter": "default",
            "level": "DEBUG"
        }
    },
    "root": {
        "level": "INFO",
        "handlers": ["console", "file"]
    }
}


def get_model_path(model_name: str) -> Path:
    """Get the path to a model's weights file."""
    if model_name not in MODEL_CONFIGS:
        raise ValueError(f"Unknown model: {model_name}")
    return MODEL_CONFIGS[model_name]["path"]


def get_default_epsilons(model_name: str) -> List[float]:
    """Get default epsilon values for a model."""
    if model_name not in MODEL_CONFIGS:
        raise ValueError(f"Unknown model: {model_name}")
    return MODEL_CONFIGS[model_name]["default_epsilons"]


def get_attack_params(attack_name: str) -> Dict:
    """Get default parameters for an attack."""
    if attack_name not in ATTACK_CONFIGS:
        raise ValueError(f"Unknown attack: {attack_name}")
    return ATTACK_CONFIGS[attack_name]["params"].copy()
