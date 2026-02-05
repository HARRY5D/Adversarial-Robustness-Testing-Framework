"""
Example Client for Deployed Adversarial Robustness Testing API

This script demonstrates how to use the deployed API on Hugging Face Spaces.
Replace YOUR_USERNAME with your actual Hugging Face username.
"""

import requests
import json
import time
from typing import Dict, List

# Your deployed API URL
API_URL = "https://hp25-adversarial-robustness-tester.hf.space"

# Alternative URL format
# API_URL = "https://huggingface.co/spaces/HP25/adversarial-robustness-Tester"


def check_api_health():
    """Check if the API is online and ready."""
    print("🔍 Checking API health...")
    
    try:
        response = requests.get(f"{API_URL}/health", timeout=10)
        response.raise_for_status()
        data = response.json()
        
        print("✅ API is online!")
        print(f"   Status: {data['status']}")
        print(f"   Available models: {', '.join(data['models_available'])}")
        print(f"   Device: {data['device']}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ API not available: {e}")
        print("\n💡 Tips:")
        print("   1. Check if the Space is running on Hugging Face")
        print("   2. Update API_URL with your actual username")
        print("   3. Wait a few minutes if the Space is just starting")
        return False


def test_model_robustness(
    model_name: str = "cifar10_resnet20",
    attack: str = "pgd",
    epsilon: float = 0.05,
    num_samples: int = 500
) -> Dict:
    """
    Test model robustness against adversarial attacks.
    
    Args:
        model_name: Model to test ('cifar10_resnet20' or 'mnist_simplecnn')
        attack: Attack type ('fgsm' or 'pgd')
        epsilon: Perturbation budget (0.0 to 1.0)
        num_samples: Number of samples to test
    
    Returns:
        Dictionary with test results
    """
    print(f"\n⚔️  Testing {model_name} with {attack.upper()} attack (ε={epsilon})...")
    print(f"   Testing {num_samples} samples...")
    
    payload = {
        "model_name": model_name,
        "attack": attack,
        "epsilon": epsilon,
        "num_samples": num_samples,
        "save_result": True
    }
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{API_URL}/run_attack",
            json=payload,
            timeout=300  # 5 minute timeout for large tests
        )
        response.raise_for_status()
        elapsed = time.time() - start_time
        
        result = response.json()
        
        print(f"\n✅ Attack completed in {elapsed:.1f} seconds")
        print(f"   Clean Accuracy: {result['clean_accuracy']:.2f}%")
        print(f"   Robust Accuracy: {result['robust_accuracy']:.2f}%")
        print(f"   Attack Success Rate: {result['attack_success_rate']:.2f}%")
        print(f"   Result ID: {result.get('result_id', 'N/A')}")
        
        return result
        
    except requests.exceptions.Timeout:
        print("❌ Request timed out. Try reducing num_samples.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return None


def compare_attacks(model_name: str = "cifar10_resnet20", epsilon: float = 0.05):
    """Compare FGSM vs PGD attack effectiveness."""
    print(f"\n📊 Comparing FGSM vs PGD on {model_name}")
    print("=" * 60)
    
    results = {}
    
    # Test FGSM
    print("\n1. Testing FGSM (fast single-step attack)...")
    results['fgsm'] = test_model_robustness(model_name, "fgsm", epsilon, 500)
    time.sleep(2)  # Be nice to the server
    
    # Test PGD
    print("\n2. Testing PGD (strong iterative attack)...")
    results['pgd'] = test_model_robustness(model_name, "pgd", epsilon, 500)
    
    # Compare
    if results['fgsm'] and results['pgd']:
        print("\n" + "=" * 60)
        print("📈 COMPARISON RESULTS")
        print("=" * 60)
        print(f"{'Attack':<10} {'Clean Acc':<12} {'Robust Acc':<12} {'Success Rate':<15}")
        print("-" * 60)
        print(f"{'FGSM':<10} {results['fgsm']['clean_accuracy']:<12.2f} "
              f"{results['fgsm']['robust_accuracy']:<12.2f} "
              f"{results['fgsm']['attack_success_rate']:<15.2f}")
        print(f"{'PGD':<10} {results['pgd']['clean_accuracy']:<12.2f} "
              f"{results['pgd']['robust_accuracy']:<12.2f} "
              f"{results['pgd']['attack_success_rate']:<15.2f}")
        print("-" * 60)
        
        # Analysis
        pgd_stronger = results['pgd']['attack_success_rate'] > results['fgsm']['attack_success_rate']
        diff = abs(results['pgd']['attack_success_rate'] - results['fgsm']['attack_success_rate'])
        
        print(f"\n💡 Analysis:")
        print(f"   PGD is {'stronger' if pgd_stronger else 'weaker'} than FGSM by {diff:.1f}%")
        print(f"   Model robustness: {'Very Vulnerable' if results['pgd']['robust_accuracy'] < 20 else 'Moderate' if results['pgd']['robust_accuracy'] < 50 else 'Good'}")


def test_robustness_curve(model_name: str = "mnist_simplecnn"):
    """Test model at multiple epsilon values to create robustness curve."""
    print(f"\n📈 Testing robustness curve for {model_name}")
    print("=" * 60)
    
    # Different epsilons for different models
    if "mnist" in model_name.lower():
        epsilons = [0.0, 0.05, 0.1, 0.15, 0.2]
    else:
        epsilons = [0.0, 0.01, 0.03, 0.05, 0.1]
    
    results = []
    
    for eps in epsilons:
        if eps == 0.0:
            print(f"\n   Testing ε={eps} (clean samples)...")
        else:
            print(f"\n   Testing ε={eps}...")
        
        result = test_model_robustness(model_name, "pgd", eps, 300)
        if result:
            results.append(result)
        time.sleep(2)
    
    # Plot results
    if results:
        print("\n" + "=" * 60)
        print("📊 ROBUSTNESS CURVE")
        print("=" * 60)
        print(f"{'Epsilon':<12} {'Clean Acc':<12} {'Robust Acc':<12} {'ASR':<12}")
        print("-" * 60)
        for r in results:
            print(f"{r['epsilon']:<12.2f} {r['clean_accuracy']:<12.2f} "
                  f"{r['robust_accuracy']:<12.2f} {r['attack_success_rate']:<12.2f}")
        print("-" * 60)
        
        print(f"\n💡 Observation:")
        print(f"   As epsilon increases, robust accuracy decreases")
        print(f"   This shows the model's vulnerability to stronger attacks")


def get_recent_results(limit: int = 5):
    """Retrieve recent test results from the database."""
    print(f"\n📜 Fetching {limit} most recent results...")
    
    try:
        response = requests.get(f"{API_URL}/results/recent?limit={limit}", timeout=10)
        response.raise_for_status()
        data = response.json()
        
        print(f"\n✅ Found {data['total_results']} results")
        
        if data['results']:
            print("\n" + "=" * 80)
            print("Recent Test Results")
            print("=" * 80)
            for i, result in enumerate(data['results'], 1):
                print(f"\n{i}. {result['model_name']} - {result['attack_type'].upper()}")
                print(f"   Epsilon: {result['epsilon']}")
                print(f"   Clean Acc: {result['clean_accuracy']:.2f}% | "
                      f"Robust Acc: {result['robust_accuracy']:.2f}% | "
                      f"ASR: {result['attack_success_rate']:.2f}%")
                print(f"   Tested: {result['timestamp']}")
        else:
            print("   No results found. Run some tests first!")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to fetch results: {e}")


def main():
    """Main demo function."""
    print("\n" + "=" * 70)
    print(" 🛡️  ADVERSARIAL ROBUSTNESS TESTING - CLIENT DEMO")
    print("=" * 70)
    print(f"\n📡 API URL: {API_URL}")
    print("\n⚠️  Remember to update API_URL with your Hugging Face Space URL!")
    
    # Check if API is available
    if not check_api_health():
        return
    
    print("\n" + "=" * 70)
    print("Choose a demo:")
    print("=" * 70)
    print("1. Quick test - CIFAR-10 with PGD")
    print("2. Compare FGSM vs PGD attacks")
    print("3. Generate robustness curve (multiple epsilons)")
    print("4. View recent test results")
    print("5. Run all demos")
    print("0. Exit")
    
    choice = input("\nEnter your choice (0-5): ").strip()
    
    if choice == "1":
        test_model_robustness("cifar10_resnet20", "pgd", 0.05, 500)
    elif choice == "2":
        compare_attacks("cifar10_resnet20", 0.05)
    elif choice == "3":
        test_robustness_curve("mnist_simplecnn")
    elif choice == "4":
        get_recent_results(10)
    elif choice == "5":
        print("\n🚀 Running all demos...\n")
        test_model_robustness("cifar10_resnet20", "fgsm", 0.05, 500)
        time.sleep(3)
        compare_attacks("mnist_simplecnn", 0.1)
        time.sleep(3)
        test_robustness_curve("cifar10_resnet20")
        time.sleep(2)
        get_recent_results(5)
    elif choice == "0":
        print("\n👋 Goodbye!")
        return
    else:
        print("\n❌ Invalid choice")
        return
    
    print("\n" + "=" * 70)
    print("✅ Demo completed!")
    print("\n📚 Next steps:")
    print("   1. Try different epsilon values")
    print("   2. Test both models (CIFAR-10 and MNIST)")
    print("   3. Compare FGSM vs PGD effectiveness")
    print("   4. Check API docs: " + API_URL + "/docs")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
