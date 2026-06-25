import time
import os
from classifier import OfflineIntentClassifier

def run_benchmarks():
    model_path = "./model.pkl"
    
    # Assert size metric
    file_size_mb = os.path.getsize(model_path) / (1024 * 1024)
    print(f"--- Benchmark Metrics ---")
    print(f"Model Size: {file_size_mb:.2f} MB")
    assert file_size_mb < 50.0, "Model footprint exceeds 50MB constraint!"
    
    classifier = OfflineIntentClassifier(model_path)
    
    # Latency timing assertions
    test_messages = [
        "Can you remind me tomorrow morning to check the deployment engine sync loop?",
        "I feel completely broken and burnt out with this project architecture",
        "Let's add an action item to review code files next week",
        "Hey! What's up context windows?"
    ]
    
    for idx, msg in enumerate(test_messages):
        start_time = time.perf_counter()
        label, confidence = classifier.predict(msg)
        end_time = time.perf_counter()
        
        latency_ms = (end_time - start_time) * 1000
        print(f"Test {idx+1} Latency: {latency_ms:.2f}ms | Label: {label} | Conf: {confidence:.2f}")
        assert latency_ms < 200.0, "Inference latency window exceeded 200ms threshold!"

    print("All performance and constraints validations passed successfully.")

if __name__ == "__main__":
    run_benchmarks()
