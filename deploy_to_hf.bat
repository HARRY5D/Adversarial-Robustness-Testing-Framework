@echo off
REM Quick deployment script for Hugging Face Spaces (Windows)

echo.
echo 🚀 Deploying Adversarial Robustness Testing API to Hugging Face
echo ==============================================================
echo.

REM Check if Git LFS is installed
git lfs version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git LFS not found. Please install from: https://git-lfs.github.com/
    echo After installing, run: git lfs install
    pause
    exit /b 1
) else (
    echo ✅ Git LFS is installed
)

REM Initialize Git if needed
if not exist .git (
    echo 📦 Initializing Git repository...
    git init
)

REM Configure Git LFS for model files
echo 📦 Configuring Git LFS for large files...
git lfs track "models/*.pth"
git lfs track "models/*.pt"
git add .gitattributes

REM Hugging Face credentials
set HF_USERNAME=HP25
set SPACE_NAME=adversarial-robustness-Tester

echo Using HF username: %HF_USERNAME%
echo Using Space name: %SPACE_NAME%
echo.

REM Set up Hugging Face remote
set HF_REPO=https://huggingface.co/spaces/%HF_USERNAME%/%SPACE_NAME%
echo 📡 Setting up remote: %HF_REPO%

REM Remove existing HF remote if it exists
git remote remove hf 2>nul

REM Add Hugging Face remote
git remote add hf %HF_REPO%

REM Copy HF readme
echo 📝 Preparing README for Hugging Face...
copy /Y README_HF.md README.md >nul

REM Stage all files
echo 📦 Staging files...
git add .

REM Commit
echo 💾 Creating commit...
git commit -m "Deploy to Hugging Face Spaces"

REM Push to Hugging Face
echo 🚀 Pushing to Hugging Face Spaces...
echo ⚠️  You may need to enter your Hugging Face credentials
git push hf main --force

echo.
echo ✅ Deployment complete!
echo.
echo 🌐 Your API will be available at:
echo    https://%HF_USERNAME%-%SPACE_NAME%.hf.space
echo.
echo 📚 API Documentation:
echo    https://%HF_USERNAME%-%SPACE_NAME%.hf.space/docs
echo.
echo ⏳ Note: First deployment may take 5-10 minutes to build
echo.
pause
