# 🚀 YOUR DEPLOYMENT GUIDE - HP25

## Your Hugging Face Space Details
- **Username:** HP25
- **Space Name:** adversarial-robustness-Tester
- **Your API URL:** `https://hp25-adversarial-robustness-tester.hf.space`
- **API Docs:** `https://hp25-adversarial-robustness-tester.hf.space/docs`

---

## ⚡ FASTEST WAY - Run This ONE Command

Open PowerShell in your project folder and run:

```powershell
.\deploy_to_hf.bat
```

**That's it!** The script will:
- ✅ Check Git LFS installation
- ✅ Track your model files
- ✅ Set up Hugging Face remote
- ✅ Push your code to HF
- ✅ Start deployment automatically

---

## 📋 Step-by-Step (If Script Doesn't Work)

### Prerequisites

**1. Install Git LFS** (if not installed)
```powershell
# Download from: https://git-lfs.github.com/
# Then run:
git lfs install
```

**2. Create Hugging Face Space** (if not already created)
- Go to: https://huggingface.co/new-space
- Space name: `adversarial-robustness-Tester`
- SDK: **Docker** ⚠️ CRITICAL
- Hardware: CPU Basic (free) or GPU T4 (recommended)
- Click "Create Space"

---

### Deployment Commands

**Open PowerShell in this folder:**
```powershell
cd "D:\JAVA\CODE\PYTHON\ML\DL\Adversarial-Robustness-Testing-Framework"
```

**Run these commands:**

```powershell
# 1. Initialize Git LFS
git lfs install

# 2. Track model files with Git LFS
git lfs track "models/*.pth"
git add .gitattributes

# 3. Initialize Git (if not already done)
git init

# 4. Add Hugging Face remote
git remote add hf https://huggingface.co/spaces/HP25/adversarial-robustness-Tester

# 5. Stage all files
git add .

# 6. Commit
git commit -m "Deploy Adversarial Robustness Testing API"

# 7. Push to Hugging Face (you'll need to login)
git push hf main
```

---

## 🔑 Authentication

When you push, you'll be asked for credentials:

**Username:** `HP25`
**Password:** Use your **Hugging Face Access Token** (NOT your password!)

### How to Get Access Token:
1. Go to: https://huggingface.co/settings/tokens
2. Click "New token"
3. Name: "Deploy API"
4. Type: Write
5. Copy the token
6. Paste when prompted for password

---

## ⏱️ Wait for Build (5-10 minutes)

After pushing, check build status:
1. Go to: https://huggingface.co/spaces/HP25/adversarial-robustness-Tester
2. Click "Logs" tab
3. Wait for "Running" status

---

## ✅ Test Your Deployment

### Test 1: Health Check
```powershell
curl https://hp25-adversarial-robustness-tester.hf.space/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "models_available": ["cifar10_resnet20", "mnist_simplecnn"],
  "device": "cuda" or "cpu"
}
```

### Test 2: Run Attack
```powershell
curl -X POST "https://hp25-adversarial-robustness-tester.hf.space/run_attack" `
  -H "Content-Type: application/json" `
  -d '{\"model_name\":\"cifar10_resnet20\",\"attack\":\"fgsm\",\"epsilon\":0.05,\"num_samples\":100}'
```

### Test 3: Interactive Docs
Open in browser:
```
https://hp25-adversarial-robustness-tester.hf.space/docs
```

### Test 4: Python Client
```powershell
python example_client.py
```

---

## 🎯 After Deployment

### Share Your API

Your public API is now live at:
```
https://hp25-adversarial-robustness-tester.hf.space
```

**Anyone can use it like this:**

```python
import requests

response = requests.post(
    "https://hp25-adversarial-robustness-tester.hf.space/run_attack",
    json={
        "model_name": "cifar10_resnet20",
        "attack": "pgd",
        "epsilon": 0.05,
        "num_samples": 500
    }
)

result = response.json()
print(f"Clean Accuracy: {result['clean_accuracy']}%")
print(f"Robust Accuracy: {result['robust_accuracy']}%")
print(f"Attack Success Rate: {result['attack_success_rate']}%")
```

---

## 🐛 Troubleshooting

### Problem: "git lfs not found"
**Solution:**
```powershell
# Download and install Git LFS from:
https://git-lfs.github.com/

# Then run:
git lfs install
```

### Problem: "Model files not uploading"
**Solution:**
```powershell
# Verify LFS is tracking files:
git lfs ls-files

# Should show your .pth files
# If not, run:
git lfs track "models/*.pth"
git add .gitattributes models/
git commit -m "Track models with LFS"
git push hf main --force
```

### Problem: "Authentication failed"
**Solution:**
- Use Access Token (not password)
- Get token from: https://huggingface.co/settings/tokens
- Make sure token has "Write" permission

### Problem: "Build fails on Hugging Face"
**Solution:**
1. Check "Logs" tab on your Space
2. Common fixes:
   - Verify `requirements.txt` has all dependencies
   - Check `Dockerfile` copied correctly
   - Ensure models are in `models/` directory

### Problem: "API returns 500 error"
**Solution:**
1. Check Space logs for Python errors
2. Verify models loaded correctly
3. Check if `data/` directory was created

---

## 🚀 Upgrade to GPU (Optional)

For 20-50x faster inference:

1. Go to your Space: https://huggingface.co/spaces/HP25/adversarial-robustness-Tester
2. Click "Settings"
3. Hardware → Select "GPU T4 small"
4. Click "Save"
5. Space will restart with GPU (~60 seconds)

**Cost:** ~$0.60/hour (only charged when Space is running)

---

## 📊 Expected Performance

### Free CPU Tier:
- Health check: < 1 second
- FGSM (500 samples): 30-60 seconds
- PGD (500 samples): 2-5 minutes

### GPU T4 Tier:
- Health check: < 1 second
- FGSM (500 samples): 5-10 seconds ⚡
- PGD (500 samples): 30-60 seconds ⚡

---

## 📚 Your Files (All Updated with HP25 credentials)

✅ `example_client.py` - Python client (already configured)
✅ `deploy_to_hf.bat` - Windows deployment script (auto-configured)
✅ `deploy_to_hf.sh` - Mac/Linux script (auto-configured)
✅ `QUICKSTART.md` - Quick reference (updated with your URLs)
✅ `Dockerfile` - Docker configuration (ready to deploy)
✅ All other deployment files ready!

---

## 🎉 Quick Summary

**To deploy RIGHT NOW:**

```powershell
# Option 1: One command (easiest)
.\deploy_to_hf.bat

# Option 2: Manual (if script fails)
git lfs install
git lfs track "models/*.pth"
git remote add hf https://huggingface.co/spaces/HP25/adversarial-robustness-Tester
git add .
git commit -m "Deploy"
git push hf main
```

**Wait 5-10 minutes, then test:**
```powershell
curl https://hp25-adversarial-robustness-tester.hf.space/health
```

**Your API is live! 🚀**

---

**Need help?** Check the Space logs at:
https://huggingface.co/spaces/HP25/adversarial-robustness-Tester/logs
