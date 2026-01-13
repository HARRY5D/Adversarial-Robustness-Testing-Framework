"""
Projected Gradient Descent (PGD) Attack Implementation

PGD is an iterative adversarial attack that is considered one of the strongest
first-order attacks. It applies FGSM iteratively with projection to stay within
the epsilon ball.

Reference: Madry et al., "Towards Deep Learning Models Resistant to Adversarial Attacks" (2018)
"""

import torch
import torch.nn as nn
from typing import Tuple


def pgd_attack(
    model: nn.Module,
    images: torch.Tensor,
    labels: torch.Tensor,
    epsilon: float = 0.05,
    alpha: float = 0.01,
    iters: int = 40,
    device: str = "cpu"
) -> torch.Tensor:
    """
    Generate adversarial examples using Projected Gradient Descent (PGD).
    
    PGD is an iterative attack that applies the gradient sign method multiple times,
    projecting the result back into an epsilon ball after each step. This makes it
    much stronger than single-step attacks like FGSM.
    
    Algorithm:
        1. Start with x_0 = x (or x + random noise)
        2. For t = 0 to iters-1:
            a. x_{t+1} = x_t + alpha * sign(∇_x L(θ, x_t, y))
            b. Project x_{t+1} back into epsilon ball around x
            c. Clamp to valid input range
    
    Args:
        model: PyTorch model to attack
        images: Input images tensor [batch_size, channels, height, width]
        labels: True labels tensor [batch_size]
        epsilon: Maximum perturbation magnitude (L∞ norm bound)
        alpha: Step size for each iteration (typically epsilon/iters)
        iters: Number of iterations
        device: Device to run computations on ('cpu' or 'cuda')
    
    Returns:
        Adversarial examples tensor with same shape as images
        
    Example:
        >>> model = load_model('mnist_simplecnn')
        >>> adv_images = pgd_attack(model, images, labels, epsilon=0.1, alpha=0.01, iters=40)
    """
    # Ensure model is in evaluation mode
    model.eval()
    
    # Move tensors to the specified device
    images = images.to(device)
    labels = labels.to(device)
    
    # Store original images for projection
    original_images = images.clone().detach()
    
    # Initialize adversarial images (start from original)
    adv_images = images.clone().detach()
    
    # Iteratively perturb the images
    for i in range(iters):
        # Enable gradient computation
        adv_images.requires_grad = True
        
        # Forward pass
        outputs = model(adv_images)
        
        # Calculate loss
        loss = nn.CrossEntropyLoss()(outputs, labels)
        
        # Zero existing gradients
        model.zero_grad()
        
        # Backward pass to compute gradients
        loss.backward()
        
        # Get gradient sign
        data_grad = adv_images.grad.data
        
        # Update adversarial images in the direction of gradient sign
        adv_images = adv_images + alpha * data_grad.sign()
        
        # Project back to epsilon ball around original image
        # This ensures ||x_adv - x||_∞ <= epsilon
        eta = torch.clamp(adv_images - original_images, min=-epsilon, max=epsilon)
        adv_images = original_images + eta
        
        # Clamp to maintain valid pixel range
        adv_images = torch.clamp(adv_images, images.min(), images.max())
        
        # Detach to prevent gradients from flowing through
        adv_images = adv_images.detach()
    
    return adv_images
