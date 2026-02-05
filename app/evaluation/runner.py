"""
Robustness Test Runner Module

Orchestrates end-to-end adversarial robustness testing.
"""

import torch
from typing import Dict, Optional
import logging
from datetime import datetime

from ..models.loader import load_model, get_dataloader
from ..attacks import fgsm_attack, pgd_attack
from .metrics import evaluate_model_robustness

logger = logging.getLogger(__name__)


class RobustnessTestRunner:
    """
    Main class for running adversarial robustness tests.
    
    This class orchestrates the entire testing pipeline:
    1. Load model
    2. Load test data
    3. Run adversarial attacks
    4. Calculate robustness metrics
    """
    
    def __init__(self, models_dir: str = "models"):
        """
        Initialize the test runner.
        
        Args:
            models_dir: Directory containing model weight files
        """
        self.models_dir = models_dir
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"RobustnessTestRunner initialized with device: {self.device}")
        
        # Attack function mapping
        self.attack_map = {
            "fgsm": fgsm_attack,
            "pgd": pgd_attack
        }
    
    def run_attack(
        self,
        model_name: str,
        attack: str,
        epsilon: float,
        num_samples: Optional[int] = 1000,
        batch_size: int = 128,
        **attack_kwargs
    ) -> Dict[str, float]:
        """
        Run a complete adversarial attack test.
        
        Args:
            model_name: Name of the model ('cifar10_resnet20' or 'mnist_simplecnn')
            attack: Attack type ('fgsm' or 'pgd')
            epsilon: Perturbation budget
            num_samples: Number of test samples to use (None = all)
            batch_size: Batch size for processing
            **attack_kwargs: Additional attack parameters (e.g., alpha, iters for PGD)
        
        Returns:
            Dictionary with robustness metrics
            
        Raises:
            ValueError: If model_name or attack is not supported
            FileNotFoundError: If model file doesn't exist
        """
        # Validate inputs
        if attack.lower() not in self.attack_map:
            raise ValueError(
                f"Unsupported attack: {attack}. "
                f"Supported attacks: {list(self.attack_map.keys())}"
            )
        
        # Construct model path
        model_path = f"{self.models_dir}/{model_name}.pth"
        
        logger.info(f"Starting robustness test for {model_name} with {attack} attack")
        logger.info(f"Parameters: epsilon={epsilon}, num_samples={num_samples}")
        
        try:
            # Load model
            model = load_model(model_name, model_path, self.device)
            
            # Load test data
            dataloader = get_dataloader(
                model_name,
                batch_size=batch_size,
                num_samples=num_samples
            )
            
            # Get attack function
            attack_fn = self.attack_map[attack.lower()]
            
            # Set default PGD parameters if not provided
            if attack.lower() == "pgd":
                attack_kwargs.setdefault("alpha", epsilon / 10)
                attack_kwargs.setdefault("iters", 40)
            
            # Run evaluation
            results = evaluate_model_robustness(
                model=model,
                dataloader=dataloader,
                attack_fn=attack_fn,
                epsilon=epsilon,
                attack_name=attack.upper(),
                device=self.device,
                **attack_kwargs
            )
            
            # Add metadata
            results["model_name"] = model_name
            results["attack"] = attack.lower()
            results["epsilon"] = epsilon
            results["timestamp"] = datetime.now().isoformat()
            results["device"] = self.device
            
            # Add attack-specific parameters
            if attack.lower() == "pgd":
                results["alpha"] = attack_kwargs.get("alpha")
                results["iters"] = attack_kwargs.get("iters")
            
            logger.info(f"✅ Test completed successfully")
            return results
            
        except Exception as e:
            logger.error(f"Test failed: {e}")
            raise
    
    def run_multiple_epsilons(
        self,
        model_name: str,
        attack: str,
        epsilons: list,
        **kwargs
    ) -> list:
        """
        Run attack with multiple epsilon values.
        
        Args:
            model_name: Model to test
            attack: Attack type
            epsilons: List of epsilon values to test
            **kwargs: Additional parameters for run_attack
        
        Returns:
            List of result dictionaries, one per epsilon
        """
        results = []
        for eps in epsilons:
            result = self.run_attack(model_name, attack, eps, **kwargs)
            results.append(result)
        return results
