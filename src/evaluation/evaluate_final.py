
import json
import time
import requests
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

TEST_FILE = ROOT / "data" / "processed" / "test.json"
PROMPT_FILE = ROOT / "configs" / "system_prompt.txt"
OUTPUT_FILE = ROOT / "reports" / "final_results.json"

MODEL_NAME = "qwen2.5:0.5b"
OLLAMA_URL = "http://localhost:11434/api/generate"

STOP_WORDS = {
    "a", "an", "the", "is", "are", "was", "were",
    "of", "to", "for", "and", "in", "that", "with",
    "it", "this", "used", "uses"
}


def keyword_coverage(expected, actual):
    expected_words = {
        word.lower().strip(".,!?")
        for word in expected.split()
        if word.lower().strip(".,!?") not in STOP_WORDS
    }

    actual_words = {
        word.lower().strip(".,!?")
        for word in actual.split()
    }

    if not expected_words:
        return 0

    matched = expected_words.intersection(actual_words)
    return round(len(matched) / len(expected_words) * 100, 2)


with open(TEST_FILE, "r", encoding="utf-8") as file:
    test_cases = json.load(file)

with open(PROMPT_FILE, "r", encoding="utf-8") as file:
    system_prompt = file.read()

results = []
total_latency = 0
valid_responses = 0
total_coverage = 0

for case in test_cases:
    question = case["question"]
    expected = case["answer"]

    prompt = (
        system_prompt
        + "\n\nUser Question: "
        + question
        + "\n\nAnswer:"
    )

    start_time = time.time()

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False
            },
            timeout=180
        )

        response.raise_for_status()
        answer = response.json()["response"].strip()

        latency = round(time.time() - start_time, 2)
        coverage = keyword_coverage(expected, answer)

        if answer:
            valid_responses += 1

        total_latency += latency
        total_coverage += coverage

        results.append({
            "question": question,
            "expected_answer": expected,
            "model_answer": answer,
            "latency_seconds": latency,
            "valid_response": bool(answer),
            "keyword_coverage_percent": coverage
        })

        print("\nQuestion:", question)
        print("Model Answer:", answer)
        print("Latency:", latency, "seconds")
        print("Keyword Coverage:", coverage, "%")

    except requests.RequestException as error:
        print("Model request failed:", error)

        results.append({
            "question": question,
            "error": str(error),
            "valid_response": False
        })

count = len(test_cases)

summary = {
    "model": MODEL_NAME,
    "total_test_cases": count,
    "valid_responses": valid_responses,
    "average_latency_seconds": round(total_latency / count, 2),
    "average_keyword_coverage_percent": round(
        total_coverage / count, 2
    ),
    "evaluation_results": results
}

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    json.dump(summary, file, indent=4)

print("\nFinal Evaluation Completed!")
print("Valid Responses:", valid_responses, "/", count)
print("Average Latency:", summary["average_latency_seconds"])
print("Average Keyword Coverage:",
      summary["average_keyword_coverage_percent"], "%")
print("Saved to:", OUTPUT_FILE)
