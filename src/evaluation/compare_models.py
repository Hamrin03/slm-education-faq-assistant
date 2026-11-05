import json
import time
import requests
from pathlib import Path

API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:0.5b"

TEST_FILE = Path("data/processed/test.json")
PROMPT_FILE = Path("configs/system_prompt.txt")
OUTPUT_FILE = Path("reports/optimization_comparison.json")


def generate_answer(prompt, optimized=False):
    options = {}

    if optimized:
        options = {
            "num_predict": 100,
            "num_ctx": 512,
            "temperature": 0.2
        }

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": options
    }

    start = time.time()

    response = requests.post(
        API_URL,
        json=payload,
        timeout=180
    )
    response.raise_for_status()

    answer = response.json()["response"]
    latency = time.time() - start

    return answer, round(latency, 2)


def compare_models():
    with open(TEST_FILE, "r", encoding="utf-8") as file:
        test_data = json.load(file)

    with open(PROMPT_FILE, "r", encoding="utf-8") as file:
        system_prompt = file.read()

    results = []

    baseline_times = []
    optimized_times = []

    for item in test_data:
        prompt = (
            system_prompt
            + "\n\nUser Question: "
            + item["question"]
            + "\n\nAnswer:"
        )

        baseline_answer, baseline_time = generate_answer(
            prompt, optimized=False
        )

        optimized_answer, optimized_time = generate_answer(
            prompt, optimized=True
        )

        baseline_times.append(baseline_time)
        optimized_times.append(optimized_time)

        results.append({
            "question": item["question"],
            "baseline_answer": baseline_answer,
            "baseline_latency": baseline_time,
            "optimized_answer": optimized_answer,
            "optimized_latency": optimized_time
        })

        print("Question:", item["question"])
        print("Baseline Latency:", baseline_time)
        print("Optimized Latency:", optimized_time)
        print("-" * 40)

    summary = {
        "model": MODEL_NAME,
        "test_cases": len(test_data),
        "average_baseline_latency": round(
            sum(baseline_times) / len(baseline_times), 2
        ),
        "average_optimized_latency": round(
            sum(optimized_times) / len(optimized_times), 2
        ),
        "results": results
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(summary, file, indent=4, ensure_ascii=False)

    print("\nModel Comparison Completed!")
    print("Average Baseline Latency:",
          summary["average_baseline_latency"])
    print("Average Optimized Latency:",
          summary["average_optimized_latency"])
    print("Saved to:", OUTPUT_FILE)


if __name__ == "__main__":
    compare_models()
