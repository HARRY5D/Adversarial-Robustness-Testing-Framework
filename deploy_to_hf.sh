#!/bin/bash
# Quick deployment script for Hugging Face Spaces

echo "🚀 Deploying Adversarial Robustness Testing API to Hugging Face"
echo "=============================================================="

# Check if Git LFS is installed
if ! command -v git-lfs &> /dev/null; then
    echo "❌ Git LFS not found. Installing..."
    git lfs install
else
    echo "✅ Git LFS is installed"
fi

# Initialize Git if needed
if [ ! -d .git ]; then
    echo "📦 Initializing Git repository..."
    git init
fi

# Configure Git LFS for model files
echo "📦 Configuring Git LFS for large files..."
git lfs track "models/*.pth"
git lfs track "models/*.pt"
git add .gitattributes

# Hugging Face credentials
HF_USERNAME="HP25"
SPACE_NAME="adversarial-robustness-Tester"

echo "Using HF username: ${HF_USERNAME}"
echo "Using Space name: ${SPACE_NAME}"
echo ""

# Set up Hugging Face remote
HF_REPO="https://huggingface.co/spaces/${HF_USERNAME}/${SPACE_NAME}"
echo "📡 Setting up remote: ${HF_REPO}"

# Remove existing HF remote if it exists
git remote remove hf 2>/dev/null || true

# Add Hugging Face remote
git remote add hf ${HF_REPO}

# Copy HF readme
echo "📝 Preparing README for Hugging Face..."
cp README_HF.md README.md

# Stage all files
echo "📦 Staging files..."
git add .

# Commit
echo "💾 Creating commit..."
git commit -m "Deploy to Hugging Face Spaces" || echo "No changes to commit"

# Push to Hugging Face
echo "🚀 Pushing to Hugging Face Spaces..."
echo "⚠️  You may need to enter your Hugging Face credentials"
git push hf main --force

echo ""
echo "✅ Deployment complete!"
echo ""
echo "🌐 Your API will be available at:"
echo "   https://${HF_USERNAME}-${SPACE_NAME}.hf.space"
echo ""
echo "📚 API Documentation:"
echo "   https://${HF_USERNAME}-${SPACE_NAME}.hf.space/docs"
echo ""
echo "⏳ Note: First deployment may take 5-10 minutes to build"
echo ""
