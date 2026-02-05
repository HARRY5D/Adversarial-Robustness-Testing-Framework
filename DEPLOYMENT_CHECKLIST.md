# 🚀 Deployment Checklist

## Pre-Deployment

### 1. Test Locally First ✅
- [ ] API runs on localhost: `python -m uvicorn app.main:app --reload`
- [ ] Health endpoint works: `http://localhost:8000/health`
- [ ] FGSM attack works (quick test)
- [ ] PGD attack works (full test)
- [ ] Database saves results correctly
- [ ] All endpoints return expected responses

### 2. Verify Project Structure ✅
```
✓ app/
  ✓ main.py
  ✓ config.py
  ✓ schemas.py
  ✓ attacks/ (fgsm.py, pgd.py)
  ✓ evaluation/ (runner.py, metrics.py)
  ✓ models/ (loader.py)
  ✓ storage/ (database.py)
✓ models/
  ✓ cifar10_resnet20.pth (verify size < 100MB)
  ✓ mnist_simplecnn.pth (verify size < 100MB)
✓ data/ (empty directory for SQLite)
✓ requirements.txt
✓ Dockerfile
✓ .dockerignore
✓ .gitattributes
✓ README.md
```

### 3. Check Model Files 📦
```bash
# Verify model files exist and are not corrupted
cd models/
ls -lh *.pth

# Expected output:
# cifar10_resnet20.pth  (~20-50 MB)
# mnist_simplecnn.pth   (~1-5 MB)
```

### 4. Update Requirements.txt 📋
```bash
# Make sure all dependencies are listed
pip freeze > requirements.txt

# Or use the minimal version (recommended):
# torch>=2.0.0
# torchvision>=0.15.0
# fastapi>=0.104.0
# uvicorn[standard]>=0.24.0
# pydantic>=2.0.0
# plotly>=5.17.0
# python-multipart>=0.0.6
```

---

## Hugging Face Deployment

### 1. Create Account 🆕
- [ ] Sign up at [huggingface.co](https://huggingface.co/join)
- [ ] Verify email
- [ ] Set up profile

### 2. Install Git LFS 📦
```bash
# Windows
# Download from: https://git-lfs.github.com/
git lfs install

# Mac
brew install git-lfs
git lfs install

# Linux
sudo apt-get install git-lfs
git lfs install
```

### 3. Create New Space 🌐
1. Go to [huggingface.co/new-space](https://huggingface.co/new-space)
2. Configure:
   - **Owner:** Your username
   - **Space name:** `adversarial-robustness-tester`
   - **License:** MIT
   - **SDK:** Docker ⚠️ IMPORTANT
   - **Hardware:** 
     - CPU Basic (Free, slower)
     - CPU Upgrade ($0.50/hr, faster)
     - GPU T4 ($0.60/hr, fastest) ⭐ Recommended for testing
   - **Public/Private:** Public (for free tier)

### 4. Deploy Using Script 🚀

**Option A: Windows**
```bash
# Run the deployment script
.\deploy_to_hf.bat

# When prompted:
# - Enter your Hugging Face username
# - Enter Space name (or press Enter for default)
# - Enter credentials if asked
```

**Option B: Manual Deployment**
```bash
# 1. Initialize Git LFS
git lfs install
git lfs track "models/*.pth"
git add .gitattributes

# 2. Initialize Git (if needed)
git init

# 3. Add Hugging Face remote (replace YOUR_USERNAME)
git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/adversarial-robustness-tester

# 4. Stage all files
git add .

# 5. Commit
git commit -m "Initial deployment to Hugging Face Spaces"

# 6. Push (you'll need HF credentials)
git push hf main
```

### 5. Configure Space Settings ⚙️

On Hugging Face Space page:

**Files Tab:**
- [ ] Verify all files uploaded correctly
- [ ] Check models/ directory has .pth files
- [ ] Confirm Dockerfile is present

**Settings Tab:**
- [ ] Hardware: Choose CPU or GPU
- [ ] Visibility: Public
- [ ] Persistent Storage: Enable (optional, for database)
- [ ] Secrets: None needed (unless using API keys)

**Build Logs:**
- [ ] Monitor build progress
- [ ] Check for errors
- [ ] Wait for "Running" status (5-10 minutes)

---

## Post-Deployment Testing

### 1. Verify Deployment ✅

**Check Health Endpoint:**
```bash
# Replace YOUR_USERNAME with your Hugging Face username
curl https://YOUR_USERNAME-adversarial-robustness-tester.hf.space/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2024-...",
  "models_available": ["cifar10_resnet20", "mnist_simplecnn"],
  "device": "cuda" or "cpu"
}
```

### 2. Test API Functionality 🧪

**Quick FGSM Test:**
```bash
curl -X POST "https://YOUR_USERNAME-adversarial-robustness-tester.hf.space/run_attack" \
  -H "Content-Type: application/json" \
  -d '{
    "model_name": "cifar10_resnet20",
    "attack": "fgsm",
    "epsilon": 0.05,
    "num_samples": 100
  }'
```

**Full PGD Test:**
```bash
curl -X POST "https://YOUR_USERNAME-adversarial-robustness-tester.hf.space/run_attack" \
  -H "Content-Type: application/json" \
  -d '{
    "model_name": "mnist_simplecnn",
    "attack": "pgd",
    "epsilon": 0.1,
    "num_samples": 500
  }'
```

### 3. Test Interactive Docs 📚
- [ ] Visit: `https://YOUR_USERNAME-adversarial-robustness-tester.hf.space/docs`
- [ ] Try "Try it out" for each endpoint
- [ ] Verify all parameters work correctly

### 4. Test Client Script 🖥️
```bash
# Update API_URL in example_client.py
# Then run:
python example_client.py
```

---

## Troubleshooting Common Issues

### ❌ Build Fails

**Error: "torch not found"**
```bash
# Solution: Check requirements.txt has:
torch>=2.0.0
torchvision>=0.15.0
```

**Error: "Out of memory during build"**
```bash
# Solution: 
# 1. Use smaller base image in Dockerfile: python:3.10-slim
# 2. Remove unnecessary files via .dockerignore
# 3. Don't install dev dependencies
```

### ❌ Models Not Loading

**Error: "FileNotFoundError: models/cifar10_resnet20.pth"**
```bash
# Solution:
# 1. Verify Git LFS tracked the files:
git lfs ls-files

# 2. Re-track and re-push:
git lfs track "models/*.pth"
git add .gitattributes models/
git commit -m "Fix model tracking"
git push hf main --force
```

### ❌ API Returns 500 Error

**Check Logs:**
1. Go to Space page
2. Click "Logs" tab
3. Look for Python errors
4. Common fixes:
   - Missing dependencies → Update requirements.txt
   - Path issues → Check Dockerfile COPY commands
   - Database errors → Ensure data/ directory exists

### ❌ Slow Performance

**Solutions:**
1. **Upgrade to GPU Hardware:**
   - Space Settings → Hardware → GPU T4
   - 20-50x faster inference
   
2. **Reduce Default Parameters:**
   ```python
   # In app/config.py
   DEFAULT_BATCH_SIZE = 32  # Instead of 128
   MAX_SAMPLES = 5000  # Instead of 10000
   ```

3. **Enable Model Caching:**
   ```python
   # Cache model loading
   from functools import lru_cache
   
   @lru_cache(maxsize=2)
   def load_model(model_name):
       ...
   ```

---

## Production Checklist

### Security 🔒
- [ ] Add rate limiting (optional)
- [ ] Add API key authentication (optional)
- [ ] Enable CORS properly
- [ ] Sanitize error messages
- [ ] Log all requests

### Monitoring 📊
- [ ] Set up external uptime monitoring
- [ ] Track API usage in database
- [ ] Monitor response times
- [ ] Alert on errors

### Documentation 📚
- [ ] Update README with deployment URL
- [ ] Add example requests
- [ ] Document all endpoints
- [ ] Provide client code examples

### Optimization ⚡
- [ ] Enable model caching
- [ ] Use batch processing
- [ ] Optimize database queries
- [ ] Add response compression

---

## Maintenance

### Regular Updates 🔄
```bash
# Update code
git add .
git commit -m "Update: description"
git push hf main

# Space will automatically rebuild
```

### Monitor Usage 📈
- Check Space analytics on HF dashboard
- Review API logs weekly
- Update models if needed
- Optimize based on usage patterns

### Backups 💾
```bash
# Backup database (if using persistent storage)
# Download from Space Files tab
# Or via API endpoint (implement if needed)
```

---

## Success Criteria ✅

Your deployment is successful when:

- [x] Health endpoint returns "healthy" status
- [x] Both models load correctly
- [x] FGSM attacks work (< 30 seconds for 500 samples)
- [x] PGD attacks work (< 2 minutes for 500 samples)
- [x] Results save to database
- [x] Recent results endpoint returns data
- [x] Interactive docs accessible at /docs
- [x] No errors in Space logs
- [x] Client script works with deployed URL

---

## Next Steps 🚀

After successful deployment:

1. **Share Your API:**
   - Add to your portfolio
   - Share on Twitter/LinkedIn
   - Write a blog post
   
2. **Enhance Features:**
   - Add web UI (Gradio/Streamlit)
   - Implement new attacks (C&W, DeepFool)
   - Support custom model upload
   
3. **Scale Up:**
   - Upgrade to GPU hardware
   - Add caching for common requests
   - Implement load balancing (if needed)

---

**Need Help?**
- Hugging Face Discord: [hf.co/join/discord](https://hf.co/join/discord)
- GitHub Discussions: Create an issue
- Documentation: [huggingface.co/docs/hub/spaces](https://huggingface.co/docs/hub/spaces)
