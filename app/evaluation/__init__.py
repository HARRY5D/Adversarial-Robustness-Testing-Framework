"""
Evaluation Module

Provides metrics calculation and test orchestration for adversarial robustness.
"""

from .metrics import (
    calculate_clean_accuracy,
    calculate_robust_accuracy,
    evaluate_model_robustness
)
from .runner import RobustnessTestRunner

__all__ = [
    'calculate_clean_accuracy',
    'calculate_robust_accuracy',
    'evaluate_model_robustness',
    'RobustnessTestRunner'
]
