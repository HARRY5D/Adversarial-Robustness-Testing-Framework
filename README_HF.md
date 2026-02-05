---
title: Adversarial Robustness Testing API
emoji: 🛡️
colorFrom: red
colorTo: blue
sdk: docker
pinned: false
license: mit
---

# 🛡️ Adversarial Robustness Testing API

A production-ready FastAPI service for testing machine learning model security against adversarial attacks. Evaluate how robust your models are against FGSM and PGD attacks.

## 🎯 What Does This Do?

This API tests neural networks against **adversarial attacks** - tiny, carefully crafted perturbations that fool ML models while being imperceptible to humans.

### Example Results
```
Clean Accuracy: 92.3%  ← Model works normally
Robust Accuracy: 12.1% ← Model fails under attack
Attack Success: 86.9%  ← Attack highly effective
```

## 🚀 Quick Start

### Test via API

```python
import requests

API_URL = "https://huggingface.co/spaces/YOUR_USERNAME/adversarial-robustness-tester"

# Run PGD attack on CIFAR-10
response = requests.post(f"{API_URL}/run_attack", json={
    "model_name": "cifar10_resnet20",
    "attack": "pgd",
    "epsilon": 0.05,
    "num_samples": 500
})

result = response.json()
print(f"Clean Accuracy: {result['clean_accuracy']}%")
print(f"Robust Accuracy: {result['robust_accuracy']}%")
print(f"Attack Success Rate: {result['attack_success_rate']}%")
```

### Interactive Documentation

Access the interactive API docs at `/docs` endpoint to test all features directly in your browser.

## 📡 Available Endpoints

### 1. `/health` - Check API Status
```bash
GET /health
```
Returns available models and system status.

### 2. `/run_attack` - Test Model Robustness
```bash
POST /run_attack
Content-Type: application/json

{
  "model_name": "cifar10_resnet20",
  "attack": "pgd",
  "epsilon": 0.05,
  "num_samples": 1000
}
```

### 3. `/results/recent` - Get Historical Results
```bash
GET /results/recent?limit=10
```

### 4. `/results/robustness_curve/{model}/{attack}` - Get Robustness Data
```bash
GET /results/robustness_curve/cifar10_resnet20/pgd
```

## 🎨 Supported Models

- **CIFAR-10 ResNet20**: Image classification (32×32 RGB)
- **MNIST SimpleCNN**: Digit recognition (28×28 grayscale)

## ⚔️ Attack Methods

### FGSM (Fast Gradient Sign Method)
- Single-step attack
- Fast computation
- Good for quick testing

### PGD (Projected Gradient Descent)
- Multi-step iterative attack
- Stronger than FGSM
- Recommended for thorough testing

## 📊 Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `model_name` | string | Model to test | Required |
| `attack` | string | Attack type (fgsm/pgd) | Required |
| `epsilon` | float | Perturbation budget (0-1) | Required |
| `num_samples` | int | Number of test samples | 1000 |
| `batch_size` | int | Processing batch size | 128 |
| `alpha` | float | PGD step size | ε/10 |
| `iters` | int | PGD iterations | 40 |

## 🔬 Understanding Epsilon

- **ε = 0.01**: Very small, barely visible
- **ε = 0.05**: Standard test (CIFAR-10)
- **ε = 0.1**: Large perturbation (MNIST)
- **ε = 0.3**: Very strong attack

## 💡 Use Cases

1. **Security Auditing**: Evaluate ML model vulnerabilities
2. **Research**: Study adversarial robustness
3. **Model Comparison**: Compare robustness across architectures
4. **Education**: Learn about adversarial machine learning

## 📈 Typical Results

**CIFAR-10 with PGD (ε=0.05)**
- Clean: ~90%
- Robust: ~10%
- ASR: ~88%

**MNIST with FGSM (ε=0.1)**
- Clean: ~98%
- Robust: ~50%
- ASR: ~49%

## 🛡️ Why This Matters

Adversarial attacks are a critical security concern for:
- Autonomous vehicles
- Face recognition systems
- Malware detection
- Content moderation
- Financial fraud detection

Testing robustness ensures your models are ready for real-world deployment.

## 📚 Learn More

- **FGSM Paper**: [Explaining and Harnessing Adversarial Examples](https://arxiv.org/abs/1412.6572)
- **PGD Paper**: [Towards Deep Learning Models Resistant to Adversarial Attacks](https://arxiv.org/abs/1706.06083)
- **Robustness Survey**: [Adversarial Robustness - Theory and Practice](https://adversarial-ml-tutorial.org/)

## 🔧 Technical Stack

- **Backend**: FastAPI + Uvicorn
- **ML**: PyTorch 2.0+
- **Database**: SQLite
- **Deployment**: Docker on Hugging Face Spaces

## 📄 License

MIT License - Free for research and educational use

## 🤝 Contributing

Found a bug? Have a feature request? Open an issue!

---

**Built for ML Security Research** 🔒
