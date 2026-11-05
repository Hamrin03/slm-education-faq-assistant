# AI Education FAQ Assistant – Small Language Model Project

## 1. Project Overview
I developed an AI Education FAQ Assistant using a Small Language Model (SLM). It answers beginner-friendly questions about Python, Artificial Intelligence, Machine Learning, Deep Learning and related technical topics.

## 2. Model Information
- Model: Qwen2.5 0.5B
- Runtime: Ollama
- Model Adaptation: Custom System Prompt
- Execution: Local CPU-based inference

## 3. Technologies Used
- Python
- FastAPI
- Ollama
- Qwen2.5 0.5B
- Pydantic
- Requests

## 4. Dataset Details
- Total records: 20
- Training: 14
- Validation: 3
- Testing: 3

## 5. Project Features
- FAQ dataset preparation and cleaning
- Local SLM inference
- Prompt-based adaptation
- Inference optimization
- Baseline and optimized model comparison
- FastAPI deployment
- Input validation and error handling

## 6. Benchmark Results
- Baseline average latency: 7.67 seconds
- Optimized average latency: 7.67 seconds

The optimization configuration limits output tokens and context size. No average latency improvement was observed in the recorded tests.

## 7. How to Run the Project

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Download the Model
```bash
ollama pull qwen2.5:0.5b
```

### Step 3: Start Ollama
Make sure the Ollama service is running. If it is not running, open another terminal and execute:

```bash
ollama serve
```

### Step 4: Start FastAPI
From the project root directory, run:

```bash
python -m uvicorn src.api.main:app --reload
```

### Step 5: Open Swagger Documentation
Open this URL in your browser:

http://127.0.0.1:8000/docs

Use the Swagger interface to test the API endpoints.

## 8. API Endpoints
- GET / – Welcome message
- GET /health – Model health status
- POST /chat – Ask an education-related question

## 9. Model Adaptation
I implemented prompt-based adaptation using a custom system prompt. LoRA/QLoRA fine-tuning was not performed due to hardware limitations.

## 10. Limitations
- Small FAQ dataset.
- Evaluation performed using three test questions.
- No measured average latency improvement.
- Further fine-tuning and larger-scale evaluation can improve the system.

## 11. Submitted By
Hamrinssssss