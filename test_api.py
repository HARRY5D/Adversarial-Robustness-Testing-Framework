"""
API Test Script - Demonstrates Adversarial Robustness Testing

This script tests the FastAPI endpoints and demonstrates the framework functionality.
"""

import requests
import json
import time
from typing import Dict

# API base URL
BASE_URL = "http://127.0.0.1:8000"


def print_section(title: str):
    """Print a formatted section header."""
    print("\n" + "=" * 70)
    print(f" {title}")
    print("=" * 70)


def print_result(result: Dict):
    """Print test results in a formatted way."""
    print(f"\n✅ Test Result ID: {result.get('result_id', 'N/A')}")
    print(f"   Model: {result['model_name']}")
    print(f"   Attack: {result['attack'].upper()} (epsilon={result['epsilon']})")
    print(f"   Clean Accuracy: {result['clean_accuracy']:.2f}%")
    print(f"   Robust Accuracy: {result['robust_accuracy']:.2f}%")
    print(f"   Attack Success Rate: {result['attack_success_rate']:.2f}%")
    print(f"   Samples Tested: {result['total_samples']}")
    print(f"   Device: {result['device']}")
    if result.get('alpha'):
        print(f"   PGD Parameters: alpha={result['alpha']}, iters={result['iters']}")


def test_health():
    """Test the health endpoint."""
    print_section("1. Testing Health Endpoint")
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        response.raise_for_status()
        data = response.json()
        
        print(f"\n✅ API is {data['status']}")
        print(f"   Available models: {', '.join(data['models_available'])}")
        print(f"   Device: {data['device']}")
        return True
        
    except Exception as e:
        print(f"\n❌ Health check failed: {e}")
        return False


def test_fgsm_attack():
    """Test FGSM attack on CIFAR-10."""
    print_section("2. Testing FGSM Attack (CIFAR-10 ResNet20)")
    
    payload = {
        "model_name": "cifar10_resnet20",
        "attack": "fgsm",
        "epsilon": 0.05,
        "num_samples": 500,
        "batch_size": 128,
        "save_result": True
    }
    
    print(f"\nRequest: {json.dumps(payload, indent=2)}")
    print("\n⏳ Running FGSM attack (this may take 15-30 seconds)...")
    
    try:
        start_time = time.time()
        response = requests.post(f"{BASE_URL}/run_attack", json=payload)
        response.raise_for_status()
        elapsed = time.time() - start_time
        
        result = response.json()
        print_result(result)
        print(f"   Execution Time: {elapsed:.2f} seconds")
        return result
        
    except Exception as e:
        print(f"\n❌ FGSM test failed: {e}")
        return None


def test_pgd_attack():
    """Test PGD attack on MNIST."""
    print_section("3. Testing PGD Attack (MNIST SimpleCNN)")
    
    payload = {
        "model_name": "mnist_simplecnn",
        "attack": "pgd",
        "epsilon": 0.1,
        "num_samples": 500,
        "batch_size": 128,
        "alpha": 0.01,
        "iters": 40,
        "save_result": True
    }
    
    print(f"\nRequest: {json.dumps(payload, indent=2)}")
    print("\n⏳ Running PGD attack (this may take 60-90 seconds)...")
    
    try:
        start_time = time.time()
        response = requests.post(f"{BASE_URL}/run_attack", json=payload)
        response.raise_for_status()
        elapsed = time.time() - start_time
        
        result = response.json()
        print_result(result)
        print(f"   Execution Time: {elapsed:.2f} seconds")
        return result
        
    except Exception as e:
        print(f"\n❌ PGD test failed: {e}")
        return None


def test_robustness_curve():
    """Test multiple epsilons for robustness curve."""
    print_section("4. Testing Robustness Curve (Multiple Epsilons)")
    
    epsilons = [0.01, 0.03, 0.05]
    results = []
    
    print(f"\nTesting FGSM on CIFAR-10 with epsilons: {epsilons}")
    print("⏳ This will take a few minutes...\n")
    
    for eps in epsilons:
        payload = {
            "model_name": "cifar10_resnet20",
            "attack": "fgsm",
            "epsilon": eps,
            "num_samples": 300,
            "save_result": True
        }
        
        try:
            print(f"   Testing epsilon={eps}...", end=" ")
            response = requests.post(f"{BASE_URL}/run_attack", json=payload)
            response.raise_for_status()
            result = response.json()
            results.append(result)
            print(f"Robust Acc: {result['robust_accuracy']:.2f}%")
            
        except Exception as e:
            print(f"❌ Failed: {e}")
    
    if results:
        print(f"\n✅ Robustness Curve Data:")
        print(f"   {'Epsilon':<10} {'Clean Acc':<12} {'Robust Acc':<12} {'ASR':<12}")
        print(f"   {'-'*46}")
        for r in results:
            print(f"   {r['epsilon']:<10} {r['clean_accuracy']:<12.2f} "
                  f"{r['robust_accuracy']:<12.2f} {r['attack_success_rate']:<12.2f}")
    
    return results


def test_get_results():
    """Test retrieving historical results."""
    print_section("5. Testing Results Retrieval")
    
    try:
        # Get recent results
        response = requests.get(f"{BASE_URL}/results/recent?limit=5")
        response.raise_for_status()
        data = response.json()
        
        print(f"\n✅ Found {data['total_results']} recent results")
        if data['results']:
            print("\n   Most recent test:")
            latest = data['results'][0]
            print(f"   - Model: {latest['model_name']}")
            print(f"   - Attack: {latest['attack_type']} (ε={latest['epsilon']})")
            print(f"   - Robust Acc: {latest['robust_accuracy']:.2f}%")
            print(f"   - Timestamp: {latest['timestamp']}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Results retrieval failed: {e}")
        return False


def main():
    """Run all tests."""
    print("\n" + "=" * 70)
    print(" ADVERSARIAL ROBUSTNESS TESTING API - DEMO")
    print(" Testing Framework Functionality")
    print("=" * 70)
    
    print("\n⚠️  Make sure the FastAPI server is running on http://127.0.0.1:8000")
    print("   Start it with: python -m uvicorn app.main:app\n")
    
    input("Press Enter to start the tests...")
    
    # Run tests
    tests_passed = []
    
    # Test 1: Health check
    tests_passed.append(test_health())
    time.sleep(1)
    
    if not tests_passed[0]:
        print("\n❌ Server is not responding. Please start the server first.")
        return
    
    # Test 2: FGSM attack
    fgsm_result = test_fgsm_attack()
    tests_passed.append(fgsm_result is not None)
    time.sleep(2)
    
    # Test 3: PGD attack  
    pgd_result = test_pgd_attack()
    tests_passed.append(pgd_result is not None)
    time.sleep(2)
    
    # Test 4: Robustness curve
    curve_results = test_robustness_curve()
    tests_passed.append(len(curve_results) > 0)
    time.sleep(2)
    
    # Test 5: Get results
    tests_passed.append(test_get_results())
    
    # Summary
    print_section("SUMMARY")
    print(f"\nTests Passed: {sum(tests_passed)}/{len(tests_passed)}")
    
    if all(tests_passed):
        print("\n🎉 All tests passed! The adversarial robustness testing framework is working correctly.")
        print("\n📊 Key Observations:")
        if fgsm_result:
            print(f"   - FGSM reduced CIFAR-10 accuracy from {fgsm_result['clean_accuracy']:.1f}% "
                  f"to {fgsm_result['robust_accuracy']:.1f}%")
        if pgd_result:
            print(f"   - PGD reduced MNIST accuracy from {pgd_result['clean_accuracy']:.1f}% "
                  f"to {pgd_result['robust_accuracy']:.1f}%")
        if curve_results:
            print(f"   - Robustness degrades as epsilon increases (tested {len(curve_results)} values)")
        
        print("\n📚 Next Steps:")
        print("   1. Access interactive API docs: http://127.0.0.1:8000/docs")
        print("   2. Test with different epsilon values")
        print("   3. Compare FGSM vs PGD attack strength")
        print("   4. Analyze results in the SQLite database (results.db)")
        print("   5. Build visualizations using the robustness curve data")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
