import sys
import os

# Add backend directory to sys.path
backend_path = os.path.join(os.path.dirname(__file__), "backend")
sys.path.insert(0, backend_path)

from app.utils.eval_benchmark import run_reproducible_evaluation


def main():
    print("======================================================================")
    print("      AI-POWERED CUSTOMER SUPPORT PLATFORM: EVALUATION BENCHMARK       ")
    print("======================================================================")
    print("Evaluating 250 Predefined Ticket Scenarios across 7 categories...")
    
    report = run_reproducible_evaluation()
    
    print("\n------------------------- BENCHMARK RESULTS -------------------------")
    print(f"Total Scenarios Evaluated       : {report['total_scenarios']}")
    print(f"Classification Accuracy         : {report['classification_accuracy_percent']}%  (Target: >= 86.0%)")
    print(f"Routing Accuracy                : {report['routing_accuracy_percent']}%  (Target: >= 86.0%)")
    print(f"Priority Detection Accuracy     : {report['priority_accuracy_percent']}%")
    print(f"Retrieval Relevance             : {report['retrieval_relevance_percent']}%")
    print(f"Confidence Calibration Score    : {report['confidence_calibration_score']} / 1.000")
    print("------------------------- LATENCY BENCHMARK -------------------------")
    print(f"Average Asynchronous Latency    : {report['average_async_latency_ms']} ms")
    print(f"Synchronous Baseline Latency    : {report['sync_baseline_latency_ms']} ms")
    print(f"Latency Reduction vs Baseline   : {report['latency_reduction_percent']}%  (Target: >= 24.0%)")
    print("------------------------- TARGET VERIFICATION -----------------------")
    acc_pass = "PASSED" if report["targets_met"]["target_86_accuracy"] else "FAILED"
    lat_pass = "PASSED" if report["targets_met"]["target_24_latency_reduction"] else "FAILED"
    print(f"Target 1 (>=86% Accuracy)       : {acc_pass}")
    print(f"Target 2 (>=24% Latency Drop)   : {lat_pass}")
    print("======================================================================\n")


if __name__ == "__main__":
    main()
