# 🚀 Deployment Guide - Adversarial Robustness Testing Framework

## Deployment on Hugging Face Spaces (Recommended)

### Why Hugging Face?
- ✅ **Free GPU access** for faster inference
- ✅ **Built for ML models** - perfect for PyTorch apps
- ✅ **Auto-scaling** and reliability
- ✅ **Public API** - users can access directly via URL
- ✅ **No credit card required** for basic tier

---

## 📦 Step-by-Step Deployment

### 1. Create Hugging Face Account
1. Go to [huggingface.co](https://huggingface.co/join)
2. Sign up (free)
3. Verify your email

### 2. Create a New Space
1. Click "New Space" at [huggingface.co/new-space](https://huggingface.co/new-space)
2. Configure:
   - **Name:** `adversarial-robustness-tester`
   - **License:** MIT
   - **SDK:** Docker
   - **Hardware:** CPU Basic (free) or GPU (if available)

### 3. Upload Your Code

**Option A: Using Git (Recommended)**
```bash
# Navigate to your project
cd "D:\JAVA\CODE\PYTHON\ML\DL\Adversarial-Robustness-Testing-Framework"

# Install Git LFS (for large model files)
git lfs install

# Track model files with Git LFS
git lfs track "models/*.pth"
git add .gitattributes

# Initialize Git (if not already)
git init

# Add Hugging Face remote (replace YOUR_USERNAME)
git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/adversarial-robustness-tester

# Add and commit files
git add .
git commit -m "Initial deployment"

# Push to Hugging Face
git push hf main
```

**Option B: Using Web Interface**
1. Zip your project (excluding `__pycache__`, `.git`, `*.db`)
2. Upload via Hugging Face web interface
3. Extract in the Space

### 4. Configure Environment (Optional)

Create `.env` file in the Space:
```env
# Performance settings
WORKERS=2
TIMEOUT=300

# Model settings
DEFAULT_BATCH_SIZE=64
MAX_SAMPLES=10000
```

### 5. Monitor Deployment

1. Go to your Space: `https://huggingface.co/spaces/YOUR_USERNAME/adversarial-robustness-tester`
2. Check "Logs" tab for build progress
3. Wait 5-10 minutes for first build
4. Once ready, you'll see "Running" status

---

## 🌐 Accessing Your Deployed API

### Base URL
```
https://YOUR_USERNAME-adversarial-robustness-tester.hf.space
```

### API Endpoints

**1. Health Check**
```bash
curl https://YOUR_USERNAME-adversarial-robustness-tester.hf.space/health
```

**2. Interactive Docs**
```
https://YOUR_USERNAME-adversarial-robustness-tester.hf.space/docs
```

**3. Run Attack**
```bash
curl -X POST "https://YOUR_USERNAME-adversarial-robustness-tester.hf.space/run_attack" \
  -H "Content-Type: application/json" \
  -d '{
    "model_name": "cifar10_resnet20",
    "attack": "pgd",
    "epsilon": 0.05,
    "num_samples": 500
  }'
```

**4. Python Client**
```python
import requests

API_URL = "https://YOUR_USERNAME-adversarial-robustness-tester.hf.space"

# Test model robustness
response = requests.post(f"{API_URL}/run_attack", json={
    "model_name": "mnist_simplecnn",
    "attack": "fgsm",
    "epsilon": 0.1,
    "num_samples": 1000
})

result = response.json()
print(f"Robust Accuracy: {result['robust_accuracy']}%")
```

---

## 🔧 Alternative Deployments

### Option 2: Railway
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
railway init
railway up
```

### Option 3: Render
1. Create `render.yaml`:
```yaml
services:
  - type: web
    name: adversarial-robustness-api
    env: docker
    plan: free
    envVars:
      - key: PORT
        value: 8000
```
2. Connect GitHub repo to Render
3. Auto-deploys on push

### Option 4: Local Docker
```bash
# Build image
docker build -t adversarial-robustness-api .

# Run container
docker run -p 8000:7860 adversarial-robustness-api

# Access at http://localhost:8000
```

---

## 📊 Performance Optimization

### 1. Enable GPU (Hugging Face)
- Upgrade to GPU hardware in Space settings
- Speeds up attacks by 20-50x
- Free GPU hours available

### 2. Reduce Memory Usage
Edit `app/config.py`:
```python
# Reduce batch size for free tier
DEFAULT_BATCH_SIZE = 32  # Instead of 128

# Limit max samples
MAX_SAMPLES = 5000  # Instead of 10000
```

### 3. Add Caching
```python
# In app/main.py
from functools import lru_cache

@lru_cache(maxsize=100)
def get_cached_result(model_name, attack, epsilon):
    # Cache frequently tested configurations
    pass
```

---

## 🐛 Troubleshooting

### Build Fails
**Error:** `torch not found`
**Solution:** Check `requirements.txt` has `torch>=2.0.0`

**Error:** `Out of memory`
**Solution:** Reduce batch_size in config or upgrade to larger instance

### Models Not Loading
**Error:** `FileNotFoundError: models/cifar10_resnet20.pth`
**Solution:** 
1. Verify models are in Git LFS
2. Check file paths in Dockerfile
3. Ensure models were pushed correctly

### Slow Performance
**Solution:**
- Use GPU hardware tier
- Reduce `num_samples` parameter
- Enable batch processing

### Database Issues
**Error:** `database is locked`
**Solution:** SQLite doesn't handle concurrent writes well
- Consider PostgreSQL for production
- Or disable `save_result=True` for high traffic

---

## 🔐 Security Best Practices

### 1. Add Rate Limiting
```python
# Install: pip install slowapi
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/run_attack")
@limiter.limit("10/minute")  # Max 10 attacks per minute
async def run_attack(request: AttackRequest):
    ...
```

### 2. Add Authentication (Optional)
```python
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

@app.post("/run_attack")
async def run_attack(
    request: AttackRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    if credentials.credentials != "YOUR_API_KEY":
        raise HTTPException(status_code=401, detail="Invalid token")
    ...
```

### 3. Input Validation
Already implemented via Pydantic schemas ✅

---

## 📈 Monitoring & Analytics

### 1. Add Logging
```python
# app/main.py already has logging configured ✅
# View logs in Hugging Face Space console
```

### 2. Usage Analytics
```python
# Track API usage in database
CREATE TABLE api_usage (
    id INTEGER PRIMARY KEY,
    timestamp DATETIME,
    endpoint TEXT,
    user_ip TEXT,
    response_time REAL
);
```

### 3. Health Monitoring
```bash
# Set up external monitoring (UptimeRobot, etc.)
https://YOUR_USERNAME-adversarial-robustness-tester.hf.space/health
```

---

## 💰 Cost Comparison

| Platform | Free Tier | GPU | Scaling | Best For |
|----------|-----------|-----|---------|----------|
| **Hugging Face** | ✅ Yes | ✅ Yes | Auto | ML APIs ⭐ |
| Railway | ✅ $5 credit | ❌ No | Auto | General apps |
| Render | ✅ Yes | ❌ No | Limited | Static/simple apps |
| AWS Lambda | ✅ 1M requests | ❌ No | Excellent | Serverless |
| DigitalOcean | ❌ $4/month | ❌ No | Manual | Full control |

---

## 🎯 Next Steps After Deployment

1. **Test the deployed API**
   ```bash
   python test_api.py  # Update BASE_URL to your HF Space URL
   ```

2. **Share with users**
   - Provide API documentation link
   - Create example notebooks
   - Add to your portfolio

3. **Monitor usage**
   - Check Space logs
   - Analyze attack patterns
   - Optimize based on usage

4. **Iterate**
   - Add new models
   - Implement new attacks
   - Build a web UI (Streamlit/Gradio)

---

## 📚 Resources

- [Hugging Face Spaces Docs](https://huggingface.co/docs/hub/spaces)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [PyTorch Model Optimization](https://pytorch.org/tutorials/recipes/recipes/tuning_guide.html)

---

## 🤝 Support

**Issues with deployment?**
1. Check Space logs: `https://huggingface.co/spaces/YOUR_USERNAME/adversarial-robustness-tester/logs`
2. Test locally with Docker first: `docker build -t test . && docker run -p 8000:7860 test`
3. Open issue on your repository

**Questions?**
- Hugging Face Discord: [hf.co/join/discord](https://hf.co/join/discord)
- FastAPI Discussions: [github.com/tiangolo/fastapi/discussions](https://github.com/tiangolo/fastapi/discussions)

---

**Happy Deploying! 🚀**
