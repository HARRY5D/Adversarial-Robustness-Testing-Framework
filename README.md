# Adversarial Robustness Testing Framework

A production-ready FastAPI service for testing machine learning model robustness against adversarial attacks. This framework evaluates model security by running FGSM and PGD attacks and measuring robustness metrics.

## 🎯 What Are Adversarial Attacks?

**Adversarial attacks** are techniques that exploit vulnerabilities in machine learning models by adding carefully crafted, often imperceptible perturbations to input data. These perturbations cause models to make incorrect predictions while appearing normal to humans.

### Why This Matters

- **Security Risk**: Deployed ML models can be fooled by malicious actors
- **Safety Critical**: Important for autonomous systems, fraud detection, content moderation
- **Model Validation**: Essential for understanding real-world model robustness beyond test accuracy

### Attack Methods Implemented

#### 1. FGSM (Fast Gradient Sign Method)
- **Type**: Single-step white-box attack
- **How it works**: Adds perturbation in the direction of the gradient's sign
- **Formula**: `x_adv = x + ε × sign(∇_x L(θ, x, y))`
- **Characteristics**:
  - Fast and computationally efficient
  - Effective against non-robust models
  - One backward pass per sample

#### 2. PGD (Projected Gradient Descent)
- **Type**: Iterative white-box attack
- **How it works**: Applies FGSM iteratively with projection to epsilon ball
- **Characteristics**:
  - Much stronger than FGSM
  - Considered one of the strongest first-order attacks
  - Multiple iterations ensure finding effective perturbations
  - Default: 40 iterations with step size α = ε/10

## 📊 How Robustness Is Measured

### Key Metrics

1. **Clean Accuracy**
   - Accuracy on original, unperturbed examples
   - Baseline model performance
   - Formula: `(correct_predictions / total_samples) × 100`

2. **Robust Accuracy**
   - Accuracy on adversarial examples
   - Measures model resilience to attacks
   - Lower values indicate vulnerability

3. **Attack Success Rate (ASR)**
   - Percentage of correctly classified clean examples that are misclassified after attack
   - Formula: `(successful_attacks / correct_clean_predictions) × 100`
   - Higher ASR = more successful attack = less robust model

### Example Interpretation

```
Clean Accuracy: 92.3%
Robust Accuracy: 12.1%
Attack Success Rate: 86.9%
```

This means:
- Model correctly classifies 92.3% of clean images
- After PGD attack (ε=0.05), only 12.1% remain correct
- Of the 92.3% correctly classified images, 86.9% were successfully attacked

## 🏗️ Project Structure

```
adversarial-test-framework/
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration (paths, defaults)
│   ├── schemas.py              # Pydantic models for API
│   ├── attacks/
│   │   ├── __init__.py
│   │   ├── fgsm.py             # FGSM implementation
│   │   └── pgd.py              # PGD implementation
│   ├── evaluation/
│   │   ├── __init__.py
│   │   ├── metrics.py          # Robustness metrics calculation
│   │   └── runner.py           # Test orchestration
│   ├── models/
│   │   ├── __init__.py
│   │   └── loader.py           # Model loading utilities
│   └── storage/
│       ├── __init__.py
│       ├── database.py         # SQLite operations
│       └── schema.sql          # Database schema
├── models/
│   ├── cifar10_resnet20.pth    # CIFAR-10 ResNet20 weights
│   └── mnist_simplecnn.pth     # MNIST SimpleCNN weights
├── requirements.txt
└── README.md
```

## 🚀 Installation and Setup

### Prerequisites

- Python 3.10+
- PyTorch 2.0+
- 4GB+ RAM
- GPU (optional, but recommended for faster testing)

### Step 1: Install Dependencies

```bash
cd D:\JAVA\CODE\PYTHON\ML\DL\Model_Attack
pip install -r requirements.txt
```

### Step 2: Verify Model Files

Ensure your pre-trained models are in the `models/` directory:

```
models/
├── cifar10_resnet20.pth
└── mnist_simplecnn.pth
```

These models should already exist from your Colab training.

### Step 3: Start the API Server

```bash
# From the Model_Attack directory
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Or simply:

```bash
python -m app.main
```

### Step 4: Access the API

- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 📡 API Usage

### 1. Check System Health

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-13T10:30:00",
  "models_available": ["cifar10_resnet20", "mnist_simplecnn"],
  "device": "cuda"
}
```

### 2. Run FGSM Attack

```bash
curl -X POST "http://localhost:8000/run_attack" \
  -H "Content-Type: application/json" \
  -d '{
    "model_name": "cifar10_resnet20",
    "attack": "fgsm",
    "epsilon": 0.05,
    "num_samples": 1000
  }'
```

### 3. Run PGD Attack (Recommended for Thorough Testing)

```bash
curl -X POST "http://localhost:8000/run_attack" \
  -H "Content-Type: application/json" \
  -d '{
    "model_name": "mnist_simplecnn",
    "attack": "pgd",
    "epsilon": 0.1,
    "num_samples": 1000,
    "alpha": 0.01,
    "iters": 40
  }'
```

### 4. Get Recent Test Results

```bash
curl http://localhost:8000/results/recent?limit=5
```

### 5. Get Robustness Curve Data

```bash
curl http://localhost:8000/results/robustness_curve/cifar10_resnet20/pgd
```

## 🔧 API Request Parameters

### POST /run_attack

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `model_name` | string | Yes | - | Model to test: `cifar10_resnet20` or `mnist_simplecnn` |
| `attack` | string | Yes | - | Attack type: `fgsm` or `pgd` |
| `epsilon` | float | Yes | - | Perturbation budget (0.0 to 1.0) |
| `num_samples` | int | No | 1000 | Number of test samples |
| `batch_size` | int | No | 128 | Batch size for processing |
| `alpha` | float | No | ε/10 | Step size for PGD |
| `iters` | int | No | 40 | Iterations for PGD |
| `save_result` | bool | No | true | Save result to database |

### Response Format

```json
{
  "clean_accuracy": 92.3,
  "robust_accuracy": 12.1,
  "attack_success_rate": 86.9,
  "model_name": "cifar10_resnet20",
  "attack": "pgd",
  "epsilon": 0.05,
  "total_samples": 1000,
  "timestamp": "2024-01-13T10:30:00.123456",
  "device": "cuda",
  "alpha": 0.01,
  "iters": 40,
  "result_id": 42
}
```

## 🧪 Testing Examples

### Python Script Example

```python
import requests

# API endpoint
url = "http://localhost:8000/run_attack"

# Test CIFAR-10 with PGD
payload = {
    "model_name": "cifar10_resnet20",
    "attack": "pgd",
    "epsilon": 0.05,
    "num_samples": 1000
}

response = requests.post(url, json=payload)
result = response.json()

print(f"Clean Accuracy: {result['clean_accuracy']}%")
print(f"Robust Accuracy: {result['robust_accuracy']}%")
print(f"Attack Success Rate: {result['attack_success_rate']}%")
```

### Test Multiple Epsilons

```python
import requests

epsilons = [0.01, 0.03, 0.05, 0.1]

for eps in epsilons:
    response = requests.post("http://localhost:8000/run_attack", json={
        "model_name": "cifar10_resnet20",
        "attack": "pgd",
        "epsilon": eps,
        "num_samples": 500
    })
    
    result = response.json()
    print(f"ε={eps}: Robust Acc = {result['robust_accuracy']}%")
```

## 📈 Database Schema

Results are automatically stored in SQLite (`results.db`):

```sql
CREATE TABLE test_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    model_name TEXT NOT NULL,
    attack_type TEXT NOT NULL,
    epsilon REAL NOT NULL,
    clean_accuracy REAL NOT NULL,
    robust_accuracy REAL NOT NULL,
    attack_success_rate REAL NOT NULL,
    total_samples INTEGER NOT NULL,
    device TEXT,
    alpha REAL,
    iters INTEGER,
    notes TEXT
);
```

## 🔍 Understanding the Results

### Typical Robustness Patterns

**CIFAR-10 ResNet20** (default epsilons: [0.01, 0.03, 0.05, 0.1])
- Clean Accuracy: ~90-92%
- FGSM at ε=0.05: ~20-30% robust accuracy
- PGD at ε=0.05: ~0-10% robust accuracy (much stronger)

**MNIST SimpleCNN** (default epsilons: [0.05, 0.1, 0.2, 0.3])
- Clean Accuracy: ~98-99%
- FGSM at ε=0.1: ~40-60% robust accuracy
- PGD at ε=0.1: ~20-40% robust accuracy

### What Good Robustness Looks Like

- **Robust Model**: Small drop in accuracy even at higher epsilons
- **Vulnerable Model**: Accuracy drops to near 0% at small epsilons
- **Production-Ready**: ASR < 30% at operationally relevant epsilon

## 🛡️ Best Practices

### 1. Choosing Epsilon
- **CIFAR-10**: Start with ε=0.05 (8/255 in L∞ norm)
- **MNIST**: Start with ε=0.1
- **Rule of thumb**: Should be barely perceptible to humans

### 2. Attack Selection
- **Quick Test**: Use FGSM for rapid assessment
- **Thorough Test**: Always validate with PGD (it's stronger)
- **Production**: Report PGD results as worst-case robustness

### 3. Sample Size
- **Development**: 500-1000 samples for quick iteration
- **Production**: Full test set (10,000) for accurate metrics
- **Trade-off**: More samples = slower but more accurate

### 4. Performance Optimization
- Use GPU if available (20-50x faster)
- Batch processing (128-256 samples)
- Limit samples during development

## 🐛 Troubleshooting

### Model Not Found Error
```
FileNotFoundError: Model file not found: models/cifar10_resnet20.pth
```
**Solution**: Ensure model files are in the `models/` directory

### CUDA Out of Memory
```
RuntimeError: CUDA out of memory
```
**Solution**: Reduce `batch_size` or `num_samples`

### Slow Performance
**Solutions**:
- Check if GPU is being used: `torch.cuda.is_available()`
- Reduce `num_samples` for faster testing
- Use FGSM instead of PGD for quick tests

### Database Locked
**Solution**: Close other connections or delete `results.db` and restart

## 🔮 Future Enhancements

Potential additions for production deployment:

1. **Web Dashboard**
   - Plotly visualizations for robustness curves
   - Real-time attack visualization
   - Historical trends and comparisons

2. **Additional Attacks**
   - C&W (Carlini & Wagner)
   - DeepFool
   - Boundary attacks

3. **Defense Mechanisms**
   - Adversarial training
   - Input transformations
   - Certified defenses

4. **Model Support**
   - Custom model upload
   - HuggingFace integration
   - Text and tabular data support

## 📚 References

1. **FGSM**: Goodfellow et al., "Explaining and Harnessing Adversarial Examples" (2015)
2. **PGD**: Madry et al., "Towards Deep Learning Models Resistant to Adversarial Attacks" (2018)
3. **Robustness Metrics**: Carlini et al., "On Evaluating Adversarial Robustness" (2019)

## 📄 License

This is a research and educational project for MLOps security testing.

## 🤝 Contributing

For issues, enhancements, or questions about adversarial robustness testing, please open an issue.

## 📞 Support

For questions about:
- **API Usage**: Check `/docs` endpoint
- **Model Loading**: See `app/models/loader.py`
- **Attack Implementation**: See `app/attacks/`
- **Metrics Calculation**: See `app/evaluation/metrics.py`

---

**Built with**: PyTorch, FastAPI, SQLite  
**Version**: 1.0.0  
**Status**: Currently supports registered models; architecture is extensible to user-uploaded models with strict validation. 
