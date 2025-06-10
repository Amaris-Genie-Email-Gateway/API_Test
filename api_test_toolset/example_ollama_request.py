import requests

API_URL = "http://192.168.1.21:11434/api/generate"

def query_ollama(model: str, prompt: str) -> str:
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(API_URL, json=payload)
    response.raise_for_status()
    return response.json()["response"]

result = query_ollama("hf.co/NEWWWWWbie/cybertron_merge_01-Q8_0-GGUF:latest", "Explain the concept of overfitting in machine learning.")
print("hf.co/NEWWWWWbie/cybertron_merge_01-Q8_0-GGUF:latest:\n", result)

