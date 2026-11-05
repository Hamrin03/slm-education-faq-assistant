from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import requests

app = FastAPI(
    title="AI Education FAQ Assistant",
    description="A local SLM-powered Education FAQ API",
    version="1.0.0"
)

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:0.5b"


class ChatRequest(BaseModel):
    question: str = Field(
        min_length=3,
        max_length=500
    )


class ChatResponse(BaseModel):
    question: str
    answer: str
    model: str


@app.get("/")
def home():
    return {
        "message": "AI Education FAQ Assistant is running!"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model": MODEL_NAME
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    try:
        with open(
            "configs/system_prompt.txt",
            "r",
            encoding="utf-8"
        ) as file:
            system_prompt = file.read()

        prompt = (
            system_prompt
            + "\n\nUser Question: "
            + request.question
            + "\n\nAnswer:"
        )

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

        if not answer:
            raise HTTPException(
                status_code=502,
                detail="The model returned an empty response."
            )

        return ChatResponse(
            question=request.question,
            answer=answer,
            model=MODEL_NAME
        )

    except requests.RequestException:
        raise HTTPException(
            status_code=503,
            detail="Local SLM service is unavailable."
        )
    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail="System prompt file not found."
        )