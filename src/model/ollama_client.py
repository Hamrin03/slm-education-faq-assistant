import requests
from pathlib import Path

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:0.5b"

PROMPT_FILE = Path("configs/system_prompt.txt")


def ask_model(question):
    with open(PROMPT_FILE, "r", encoding="utf-8") as file:
        system_prompt = file.read()

    full_prompt = f"""
{system_prompt}

User Question: {question}

Answer:
"""

    payload = {
        "model": MODEL_NAME,
        "prompt": full_prompt,
        "stream": False
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=180
    )
    response.raise_for_status()

    return response.json()["response"]


if __name__ == "__main__":
    question = "What is Machine Learning? Explain in simple English."
    answer = ask_model(question)

    print("Question:", question)
    print("Adapted SLM Answer:", answer)