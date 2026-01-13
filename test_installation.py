"""
Quick Test Script for Adversarial Robustness Testing Framework

Run this script to verify the installation and basic functionality.
"""

import sys
from pathlib import Path

def test_imports():
    """Test that all required packages can be imported."""
    print("=" * 60)
    print("Testing Package Imports...")
    print("=" * 60)
    
    try:
        import torch
        print(f"✅ PyTorch {torch.__version__}")
        print(f"   CUDA available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"   CUDA version: {torch.version.cuda}")
            print(f"   Device: {torch.cuda.get_device_name(0)}")
    except ImportError as e:
        print(f"❌ PyTorch import failed: {e}")
        return False
    
    try:
        import torchvision
        print(f"✅ Torchvision {torchvision.__version__}")
    except ImportError as e:
        print(f"❌ Torchvision import failed: {e}")
        return False
    
    try:
        import fastapi
        print(f"✅ FastAPI {fastapi.__version__}")
    except ImportError as e:
        print(f"❌ FastAPI import failed: {e}")
        return False
    
    try:
        import uvicorn
        print(f"✅ Uvicorn installed")
    except ImportError as e:
        print(f"❌ Uvicorn import failed: {e}")
        return False
    
    try:
        import pydantic
        print(f"✅ Pydantic {pydantic.__version__}")
    except ImportError as e:
        print(f"❌ Pydantic import failed: {e}")
        return False
    
    try:
        import plotly
        print(f"✅ Plotly {plotly.__version__}")
    except ImportError as e:
        print(f"❌ Plotly import failed: {e}")
        return False
    
    print("\n✅ All required packages imported successfully!\n")
    return True


def test_project_structure():
    """Test that all required files and directories exist."""
    print("=" * 60)
    print("Testing Project Structure...")
    print("=" * 60)
    
    base_dir = Path(__file__).parent
    
    required_paths = [
        "app/main.py",
        "app/config.py",
        "app/schemas.py",
        "app/attacks/fgsm.py",
        "app/attacks/pgd.py",
        "app/evaluation/metrics.py",
        "app/evaluation/runner.py",
        "app/models/loader.py",
        "app/storage/database.py",
        "app/storage/schema.sql",
        "requirements.txt",
        "README.md"
    ]
    
    all_exist = True
    for path_str in required_paths:
        path = base_dir / path_str
        if path.exists():
            print(f"✅ {path_str}")
        else:
            print(f"❌ {path_str} - NOT FOUND")
            all_exist = False
    
    print()
    
    # Check for model files
    model_dir = base_dir / "models"
    model_files = ["cifar10_resnet20.pth", "mnist_simplecnn.pth"]
    
    print("Checking model files:")
    for model_file in model_files:
        model_path = model_dir / model_file
        if model_path.exists():
            size_mb = model_path.stat().st_size / (1024 * 1024)
            print(f"✅ {model_file} ({size_mb:.2f} MB)")
        else:
            print(f"⚠️  {model_file} - NOT FOUND (will need to be added)")
    
    print()
    if all_exist:
        print("✅ All required project files exist!\n")
    else:
        print("❌ Some required files are missing!\n")
    
    return all_exist


def test_module_imports():
    """Test that custom modules can be imported."""
    print("=" * 60)
    print("Testing Custom Module Imports...")
    print("=" * 60)
    
    try:
        from app.attacks import fgsm_attack, pgd_attack
        print("✅ Attack modules imported")
    except ImportError as e:
        print(f"❌ Attack modules import failed: {e}")
        return False
    
    try:
        from app.models import load_model, get_dataloader
        print("✅ Model loader imported")
    except ImportError as e:
        print(f"❌ Model loader import failed: {e}")
        return False
    
    try:
        from app.evaluation import RobustnessTestRunner
        print("✅ Evaluation modules imported")
    except ImportError as e:
        print(f"❌ Evaluation modules import failed: {e}")
        return False
    
    try:
        from app.storage import DatabaseManager
        print("✅ Storage modules imported")
    except ImportError as e:
        print(f"❌ Storage modules import failed: {e}")
        return False
    
    try:
        from app.schemas import AttackRequest, AttackResponse
        print("✅ Pydantic schemas imported")
    except ImportError as e:
        print(f"❌ Pydantic schemas import failed: {e}")
        return False
    
    print("\n✅ All custom modules imported successfully!\n")
    return True


def test_database_init():
    """Test database initialization."""
    print("=" * 60)
    print("Testing Database Initialization...")
    print("=" * 60)
    
    try:
        from app.storage import DatabaseManager
        
        # Create test database
        db = DatabaseManager(db_path="test_results.db")
        print("✅ Database connection established")
        
        # Try a simple query
        recent = db.get_recent_results(limit=1)
        print(f"✅ Database query successful (found {len(recent)} results)")
        
        db.close()
        print("✅ Database closed successfully")
        
        # Clean up test database
        import os
        if os.path.exists("test_results.db"):
            os.remove("test_results.db")
            print("✅ Test database cleaned up")
        
        print("\n✅ Database initialization successful!\n")
        return True
        
    except Exception as e:
        print(f"❌ Database initialization failed: {e}\n")
        return False


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print(" ADVERSARIAL ROBUSTNESS TESTING FRAMEWORK")
    print(" Installation Verification Script")
    print("=" * 60 + "\n")
    
    results = []
    
    # Run tests
    results.append(("Package Imports", test_imports()))
    results.append(("Project Structure", test_project_structure()))
    results.append(("Custom Modules", test_module_imports()))
    results.append(("Database Init", test_database_init()))
    
    # Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n🎉 All tests passed! Your installation is ready.")
        print("\nNext steps:")
        print("1. Ensure model files are in the models/ directory:")
        print("   - cifar10_resnet20.pth")
        print("   - mnist_simplecnn.pth")
        print("\n2. Start the API server:")
        print("   python -m uvicorn app.main:app --reload")
        print("\n3. Access the API documentation:")
        print("   http://localhost:8000/docs")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
