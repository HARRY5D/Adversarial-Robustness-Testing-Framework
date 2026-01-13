"""
Model Loader Module

Handles loading of pre-trained models for adversarial robustness testing.
Supports CIFAR-10 ResNet20 and MNIST SimpleCNN models.
"""

import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
from pathlib import Path
from typing import Tuple, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SimpleCNN(nn.Module):
    """
    Simple CNN architecture for MNIST classification.
    
    Architecture:
        - Conv2d(1, 32, 3, 1) -> ReLU
        - Conv2d(32, 64, 3, 1) -> ReLU
        - Dropout2d(0.25)
        - Flatten
        - Linear(36864, 128) -> ReLU
        - Dropout(0.5)
        - Linear(128, 10)
    """
    
    def __init__(self):
        super(SimpleCNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, 3, 1)
        self.relu1 = nn.ReLU()
        self.conv2 = nn.Conv2d(32, 64, 3, 1)
        self.relu2 = nn.ReLU()
        self.dropout1 = nn.Dropout2d(0.25)
        # Feature size after conv layers: 64 * 24 * 24 = 36864
        self.fc1 = nn.Linear(36864, 128)
        self.relu3 = nn.ReLU()
        self.dropout2 = nn.Dropout(0.5)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = self.relu1(self.conv1(x))
        x = self.relu2(self.conv2(x))
        x = self.dropout1(x)
        x = torch.flatten(x, 1)
        x = self.relu3(self.fc1(x))
        x = self.dropout2(x)
        return self.fc2(x)


def load_cifar10_model(model_path: str, device: str = "cpu") -> nn.Module:
    """
    Load pre-trained CIFAR-10 ResNet20 model.
    
    Args:
        model_path: Path to the model weights file (.pth)
        device: Device to load model on ('cpu' or 'cuda')
    
    Returns:
        Loaded PyTorch model in evaluation mode
        
    Raises:
        FileNotFoundError: If model file doesn't exist
        RuntimeError: If model loading fails
    """
    model_path = Path(model_path)
    
    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found: {model_path}")
    
    try:
        # Load ResNet20 architecture from torch hub
        logger.info("Loading CIFAR-10 ResNet20 architecture from torch.hub...")
        model = torch.hub.load(
            "chenyaofo/pytorch-cifar-models",
            "cifar10_resnet20",
            pretrained=False  # We'll load our own weights
        )
        
        # Load pre-trained weights
        logger.info(f"Loading weights from {model_path}...")
        state_dict = torch.load(model_path, map_location=device)
        model.load_state_dict(state_dict)
        
        # Move to device and set to eval mode
        model = model.to(device)
        model.eval()
        
        logger.info("✅ CIFAR-10 ResNet20 model loaded successfully")
        return model
        
    except Exception as e:
        logger.error(f"Failed to load CIFAR-10 model: {e}")
        raise RuntimeError(f"Model loading failed: {e}")


def load_mnist_model(model_path: str, device: str = "cpu") -> nn.Module:
    """
    Load pre-trained MNIST SimpleCNN model.
    
    Args:
        model_path: Path to the model weights file (.pth)
        device: Device to load model on ('cpu' or 'cuda')
    
    Returns:
        Loaded PyTorch model in evaluation mode
        
    Raises:
        FileNotFoundError: If model file doesn't exist
        RuntimeError: If model loading fails
    """
    model_path = Path(model_path)
    
    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found: {model_path}")
    
    try:
        # Initialize SimpleCNN architecture
        logger.info("Initializing MNIST SimpleCNN architecture...")
        model = SimpleCNN()
        
        # Load pre-trained weights
        logger.info(f"Loading weights from {model_path}...")
        state_dict = torch.load(model_path, map_location=device)
        model.load_state_dict(state_dict)
        
        # Move to device and set to eval mode
        model = model.to(device)
        model.eval()
        
        logger.info("✅ MNIST SimpleCNN model loaded successfully")
        return model
        
    except Exception as e:
        logger.error(f"Failed to load MNIST model: {e}")
        raise RuntimeError(f"Model loading failed: {e}")


def get_cifar10_dataloader(batch_size: int = 128, num_samples: Optional[int] = None):
    """
    Get CIFAR-10 test dataset dataloader with proper transforms.
    
    Args:
        batch_size: Batch size for the dataloader
        num_samples: Optional limit on number of samples to use
    
    Returns:
        DataLoader for CIFAR-10 test set
    """
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2471, 0.2435, 0.2616))
    ])
    
    testset = torchvision.datasets.CIFAR10(
        root='./data',
        train=False,
        download=True,
        transform=transform
    )
    
    # Limit samples if specified
    if num_samples is not None and num_samples < len(testset):
        indices = torch.randperm(len(testset))[:num_samples]
        testset = torch.utils.data.Subset(testset, indices)
    
    testloader = torch.utils.data.DataLoader(
        testset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=0  # Set to 0 for Windows compatibility
    )
    
    logger.info(f"✅ CIFAR-10 test dataloader created ({len(testset)} samples)")
    return testloader


def get_mnist_dataloader(batch_size: int = 128, num_samples: Optional[int] = None):
    """
    Get MNIST test dataset dataloader with proper transforms.
    
    Args:
        batch_size: Batch size for the dataloader
        num_samples: Optional limit on number of samples to use
    
    Returns:
        DataLoader for MNIST test set
    """
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])
    
    testset = torchvision.datasets.MNIST(
        root='./data',
        train=False,
        download=True,
        transform=transform
    )
    
    # Limit samples if specified
    if num_samples is not None and num_samples < len(testset):
        indices = torch.randperm(len(testset))[:num_samples]
        testset = torch.utils.data.Subset(testset, indices)
    
    testloader = torch.utils.data.DataLoader(
        testset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=0  # Set to 0 for Windows compatibility
    )
    
    logger.info(f"✅ MNIST test dataloader created ({len(testset)} samples)")
    return testloader


def load_model(model_name: str, model_path: str, device: str = "cpu") -> nn.Module:
    """
    Load a model by name.
    
    Args:
        model_name: Name of the model ('cifar10_resnet20' or 'mnist_simplecnn')
        model_path: Path to the model weights file
        device: Device to load model on
    
    Returns:
        Loaded model
        
    Raises:
        ValueError: If model_name is not supported
    """
    model_name = model_name.lower()
    
    if model_name == "cifar10_resnet20":
        return load_cifar10_model(model_path, device)
    elif model_name == "mnist_simplecnn":
        return load_mnist_model(model_path, device)
    else:
        raise ValueError(
            f"Unsupported model: {model_name}. "
            f"Supported models: cifar10_resnet20, mnist_simplecnn"
        )


def get_dataloader(model_name: str, batch_size: int = 128, num_samples: Optional[int] = None):
    """
    Get dataloader for a specific model.
    
    Args:
        model_name: Name of the model
        batch_size: Batch size for dataloader
        num_samples: Optional limit on number of samples
    
    Returns:
        Appropriate dataloader
        
    Raises:
        ValueError: If model_name is not supported
    """
    model_name = model_name.lower()
    
    if model_name == "cifar10_resnet20":
        return get_cifar10_dataloader(batch_size, num_samples)
    elif model_name == "mnist_simplecnn":
        return get_mnist_dataloader(batch_size, num_samples)
    else:
        raise ValueError(
            f"Unsupported model: {model_name}. "
            f"Supported models: cifar10_resnet20, mnist_simplecnn"
        )
