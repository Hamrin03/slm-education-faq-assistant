# Small Language Model Comparison

## 1. Models Selected for Comparison

I researched three Small Language Models for the AI Education FAQ Assistant.

### Model 1: Qwen2.5 0.5B Instruct
- Parameters: Approximately 0.49 Billion
- Context Length: 32,768 tokens
- License: Apache 2.0
- Quantization used: Q4_K_M
- Runtime: Ollama
- Suitability: Lightweight and suitable for local CPU-based inference.

### Model 2: SmolLM2 360M Instruct
- Parameters: Approximately 0.36 Billion
- Context Length: 2,048 tokens
- License: Apache 2.0
- Suitability: Very lightweight and designed for resource-efficient applications.

### Model 3: TinyLlama 1.1B Chat
- Parameters: Approximately 1.1 Billion
- Context Length: 2,048 tokens
- License: Apache 2.0
- Suitability: A compact conversational model with more parameters than the other two alternatives.

## 2. Model Comparison

| Criteria | Qwen2.5 0.5B | SmolLM2 360M | TinyLlama 1.1B |
|---|---|---|---|
| Parameters | 0.49B | 0.36B | 1.1B |
| Context | 32K | 2K | 2K |
| License | Apache 2.0 | Apache 2.0 | Apache 2.0 |
| Relative Size | Small | Smallest | Largest |
| Local CPU Suitability | Good with quantization | Good candidate | More resource demanding |

Note: Context lengths are based on the respective model documentation. Actual inference memory and speed depend on quantization, runtime and hardware.

## 3. Hardware Considerations

The development system has approximately 7.7 GB RAM and an Intel UHD integrated graphics processor without an NVIDIA GPU.

Therefore, a lightweight quantized model was preferred to reduce memory requirements and support local inference.

## 4. Selected Model and Justification

I selected Qwen2.5 0.5B Instruct for this project.

The main reasons are:
- Small model size.
- Apache 2.0 license.
- 32K context length.
- Support for local inference through Ollama.
- Q4_K_M quantization.
- Suitable for beginner-friendly educational FAQ responses.

I verified the installed model configuration using the Ollama model inspection command.

## 5. Research References

1. Qwen2.5: https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct
2. SmolLM2: https://huggingface.co/HuggingFaceTB/SmolLM2-360M-Instruct
3. TinyLlama: https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v1.0

## 6. Conclusion

Based on model size, context length, licensing and available hardware, Qwen2.5 0.5B was selected for the AI Education FAQ Assistant. It provides a practical balance between lightweight local execution and the requirements of this educational application.