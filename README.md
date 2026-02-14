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

[![Hugging Face Spaces](https://img.shields.io/badge/🤗%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/HP25/adversarial-robustness-Tester)
[![API Status](https://img.shields.io/badge/API-Live-brightgreen)](https://hp25-adversarial-robustness-tester.hf.space/health)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A production-ready FastAPI service for testing machine learning model security against adversarial attacks. Evaluate how robust your models are against FGSM and PGD attacks.

## 🌐 **Live Demo - Try It Now!**

**🚀 API Endpoint:** `https://hp25-adversarial-robustness-tester.hf.space`

**📚 Interactive Docs:** [https://hp25-adversarial-robustness-tester.hf.space/docs](https://hp25-adversarial-robustness-tester.hf.space/docs)

**✅ Status Check:** [https://hp25-adversarial-robustness-tester.hf.space/health](https://hp25-adversarial-robustness-tester.hf.space/health)

> **No installation required!** The API is deployed on Hugging Face Spaces and ready to use.

---

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

# Use the live deployed API
API_URL = "https://hp25-adversarial-robustness-tester.hf.space"

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

### Try in Browser (No Code Required!)

**Interactive Swagger UI:** [https://hp25-adversarial-robustness-tester.hf.space/docs](https://hp25-adversarial-robustness-tester.hf.space/docs)

Click "Try it out" on any endpoint to test directly in your browser - no coding needed!

## 📡 Available Endpoints

**Base URL:** `https://hp25-adversarial-robustness-tester.hf.space`

### 1. `/health` - Check API Status
```bash
curl https://hp25-adversarial-robustness-tester.hf.space/health
```
Returns available models and system status.

### 2. `/run_attack` - Test Model Robustness
```bash
curl -X POST "https://hp25-adversarial-robustness-tester.hf.space/run_attack" \
  -H "Content-Type: application/json" \
  -d '{
    "model_name": "cifar10_resnet20",
    "attack": "pgd",
    "epsilon": 0.05,
    "num_samples": 500
  }'
```

### 3. `/results/recent` - Get Historical Results
```bash
curl "https://hp25-adversarial-robustness-tester.hf.space/results/recent?limit=10"
```

### 4. `/results/robustness_curve/{model}/{attack}` - Get Robustness Data
```bash
curl "https://hp25-adversarial-robustness-tester.hf.space/results/robustness_curve/cifar10_resnet20/pgd
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
- **Deployment**: Docker on Hugging Face Spaces ✅
- **Status**: Live and production-ready

## 🖥️ Local Development

Want to run locally? Clone and run:

```bash
git clone https://github.com/HARRY5D/Adversarial-Robustness-Testing-Framework.git
cd Adversarial-Robustness-Testing-Framework
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Access at `http://localhost:8000`

## 📦 Deploy Your Own

Deploy your own instance on Hugging Face Spaces:

1. Fork this repository
2. Create a new Space on Hugging Face
3. Select "Docker" SDK
4. Push code to your Space

See [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) for detailed instructions.

## 📄 License

MIT License - Free for research and educational use

## 🤝 Contributing

Found a bug? Have a feature request? Open an issue on [GitHub](https://github.com/HARRY5D/Adversarial-Robustness-Testing-Framework)!

## 🔗 Links

- **Live API**: [https://hp25-adversarial-robustness-tester.hf.space](https://hp25-adversarial-robustness-tester.hf.space)
- **API Docs**: [https://hp25-adversarial-robustness-tester.hf.space/docs](https://hp25-adversarial-robustness-tester.hf.space/docs)
- **GitHub**: [HARRY5D/Adversarial-Robustness-Testing-Framework](https://github.com/HARRY5D/Adversarial-Robustness-Testing-Framework)
- **Hugging Face Space**: [HP25/adversarial-robustness-Tester](https://huggingface.co/spaces/HP25/adversarial-robustness-Tester)

## 👨‍💻 Author

**HP25** - [@HARRY5D](https://github.com/HARRY5D)

---

**Built for ML Security Research** 🔒 | **Deployed on Hugging Face Spaces** 🤗
