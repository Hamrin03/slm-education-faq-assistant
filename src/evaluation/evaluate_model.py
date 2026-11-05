import json
import time
import requests
from pathlib import Path

MODEL_NAME = "qwen2.5:0.5b"
API_URL = "http://localhost:11434/api/generate"

TEST_FILE = Path("data/processed/test.json")
OUTPUT_FILE = Path("reports/baseline_results.json")


def evaluate_model():
    with open(TEST_FILE, "r", encoding="utf-8") as file:
        test_data = json.load(file)

    results = []
    total_time = 0
    valid_responses = 0

    for item in test_data:
        question = item["question"]
        expected_answer = item["answer"]

        payload = {
            "model": MODEL_NAME,
            "prompt": question,
            "stream": False
        }

        start_time = time.time()

        response = requests.post(
            API_URL,
            json=payload,
            timeout=180
        )

        response.raise_for_status()

        answer = response.json()["response"]
        latency = time.time() - start_time

        total_time += latency

        if answer.strip():
            valid_responses += 1

        results.append({
            "question": question,
            "expected_answer": expected_answer,
            "model_answer": answer,
            "latency_seconds": round(latency, 2),
            "valid_response": bool(answer.strip())
        })

        print("Question:", question)
        print("Answer:", answer)
        print("Latency:", round(latency, 2), "seconds")
        print("-" * 40)

    summary = {
        "model": MODEL_NAME,
        "total_test_cases": len(test_data),
        "valid_responses": valid_responses,
        "average_latency_seconds": round(
            total_time / len(test_data), 2
        ) if test_data else 0,
        "results": results
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(summary, file, indent=4, ensure_ascii=False)

    print("\nBaseline Evaluation Completed!")
    print("Total Test Cases:", len(test_data))
    print("Valid Responses:", valid_responses)
    print("Average Latency:", summary["average_latency_seconds"])
    print("Saved to:", OUTPUT_FILE)


if __name__ == "__main__":
    evaluate_model()