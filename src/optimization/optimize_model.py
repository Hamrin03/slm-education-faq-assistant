import requests
import time

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:0.5b"


def optimized_response(question):
    payload = {
        "model": MODEL_NAME,
        "prompt": question,
        "stream": False,
        "options": {
            "num_predict": 100,
            "num_ctx": 512,
            "temperature": 0.2
        }
    }

    start_time = time.time()

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=180
    )

    response.raise_for_status()

    answer = response.json()["response"]
    latency = time.time() - start_time

    print("Question:", question)
    print("Optimized Answer:", answer)
    print("Response Time:", round(latency, 2), "seconds")


if __name__ == "__main__":
    optimized_response(
        "What is Artificial Intelligence? Explain simply."
    )
    