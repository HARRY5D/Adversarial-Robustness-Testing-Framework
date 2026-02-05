"""
Fast Gradient Sign Method (FGSM) Attack Implementation

FGSM is a single-step adversarial attack that perturbs inputs in the direction
of the gradient to maximize loss and cause misclassification.

Reference: Goodfellow et al., "Explaining and Harnessing Adversarial Examples" (2015)
"""

import torch
import torch.nn as nn
from typing import Tuple


def fgsm_attack(
    model: nn.Module,
    images: torch.Tensor,
    labels: torch.Tensor,
    epsilon: float = 0.05,
    device: str = "cpu"
) -> torch.Tensor:
    """
    Generate adversarial examples using Fast Gradient Sign Method (FGSM).
    
    FGSM is a single-step attack that adds perturbation in the direction of the
    gradient's sign to maximize the loss function.
    
    Formula: x_adv = x + epsilon * sign(∇_x L(θ, x, y))
    
    Args:
        model: PyTorch model to attack
        images: Input images tensor [batch_size, channels, height, width]
        labels: True labels tensor [batch_size]
        epsilon: Maximum perturbation magnitude (L∞ norm bound)
        device: Device to run computations on ('cpu' or 'cuda')
    
    Returns:
        Adversarial examples tensor with same shape as images
        
    Example:
        >>> model = load_model('cifar10_resnet20')
        >>> adv_images = fgsm_attack(model, images, labels, epsilon=0.05)
    """
    # Ensure model is in evaluation mode
    model.eval()
    
    # Move tensors to the specified device
    images = images.to(device)
    labels = labels.to(device)
    
    # Enable gradient computation for input images
    images.requires_grad = True
    
    # Forward pass
    outputs = model(images)
    
    # Calculate loss
    loss = nn.CrossEntropyLoss()(outputs, labels)
    
    # Zero existing gradients
    model.zero_grad()
    
    # Backward pass to compute gradients w.r.t. input
    loss.backward()
    
    # Get gradient sign
    data_grad = images.grad.data
    
    # Create adversarial example by adding epsilon-scaled gradient sign
    perturbed_image = images + epsilon * data_grad.sign()
    
    # Clamp to maintain valid pixel range
    # We clamp to the range of the input images to preserve normalization
    perturbed_image = torch.clamp(perturbed_image, images.min(), images.max())
    
    # Detach from computation graph
    perturbed_image = perturbed_image.detach()
    
    return perturbed_image
