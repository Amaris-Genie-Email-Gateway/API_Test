import requests
import time
import json

model = "hf.co/unsloth/Qwen3-14B-GGUF:Q4_K_M"
prompt = "Explain the theory of relativity in detail."


response = requests.post(
    "http://192.168.1.21:11434/api/generate",
    json={
        "model": model,
        "prompt": prompt,
        "stream": True
    },
    stream=True
)

token_count = 0
start_time = time.time()

for line in response.iter_lines(decode_unicode=True):
    if line:
        data = json.loads(line)
        if "response" in data:
            token = data["response"]
            print(token, end="", flush=True)
            token_count += 1
        elif data.get("done", False):
            break

elapsed = time.time() - start_time
print(f"\n\nTotal tokens: {token_count}")
print(f"Time elapsed: {elapsed:.2f} seconds")
print(f"Speed: {token_count / elapsed:.2f} tokens/second")
