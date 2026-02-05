# 🚀 Quick Start Guide - Deploy in 5 Minutes

## Prerequisites
- Git installed
- Hugging Face account (free)
- Project models in `models/` directory

---

## 🎯 Option 1: One-Click Deploy (Windows)

```bash
# Just run this script:
.\deploy_to_hf.bat

# Enter your HF username when prompted
# Wait 5-10 minutes for build
# Done! ✅
```

---

## 🎯 Option 2: Manual Deploy (3 Commands)

```bash
# 1. Install Git LFS
git lfs install

# 2. Track model files
git lfs track "models/*.pth"

# 3. Push to Hugging Face
git init
git remote add hf https://huggingface.co/spaces/HP25/adversarial-robustness-Tester
git add .
git commit -m "Deploy"
git push hf main
```

---

## 📊 Test Your Deployment

**1. Check Health:**
```bash
curl https://hp25-adversarial-robustness-tester.hf.space/health
```

**2. Run Attack:**
```bash
curl -X POST "https://hp25-adversarial-robustness-tester.hf.space/run_attack" \
  -H "Content-Type: application/json" \
  -d '{"model_name":"cifar10_resnet20","attack":"fgsm","epsilon":0.05,"num_samples":100}'
```

**3. View Docs:**
```
https://hp25-adversarial-robustness-tester.hf.space/docs
```

---

## 🎨 Use the Client

```bash
# 1. Update API_URL in example_client.py
# 2. Run:
python example_client.py
```

---

## ❓ Troubleshooting

**Build fails?**
- Check `requirements.txt` has all dependencies
- Verify model files are < 100MB each

**Models not found?**
```bash
git lfs ls-files  # Should show *.pth files
```

**API slow?**
- Upgrade to GPU hardware in Space settings
- Reduce `num_samples` parameter

---

## 📚 Full Documentation

- [Deployment Guide](README_DEPLOYMENT.md) - Complete instructions
- [Deployment Checklist](DEPLOYMENT_CHECKLIST.md) - Step-by-step checklist
- [Example Client](example_client.py) - Python client code

---

**Need help?** Check the logs tab on your Hugging Face Space!
