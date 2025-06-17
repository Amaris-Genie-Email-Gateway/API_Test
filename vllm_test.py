import requests
from typing import List, Dict, Any

def send_vllm_request(
    ip: str,
    port: int,
    model_name: str,
    messages: List[Dict[str, str]],
    temperature: float = 0.7,
    max_tokens: int = 512
) -> str:
    """
    Send a chat request to a vLLM server using the OpenAI-compatible API.

    Args:
        ip (str): The IP address of the vLLM server.
        port (int): The port of the vLLM server.
        model_name (str): The name of the model to use.
        messages (List[Dict[str, str]]): A list of chat messages, each with 'role' and 'content'.
        temperature (float): Sampling temperature.
        max_tokens (int): Maximum number of tokens to generate.

    Returns:
        str: The content of the model's reply.
    """
    url = f"http://{ip}:{port}/v1/chat/completions"
    headers = {
        "Content-Type": "application/json"
    }
    payload: Dict[str, Any] = {
        "model": model_name,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']
    except requests.RequestException as e:
        raise RuntimeError(f"Request failed: {e}")
    except (KeyError, IndexError) as e:
        raise RuntimeError(f"Unexpected response format: {e}")

if __name__ == "__main__":
    # Example usage
    ip_address = "192.168.1.100"
    port_number = 8000
    model = "llama-3"

    conversation = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of France?"}
    ]

    try:
        reply = send_vllm_request(ip_address, port_number, model, conversation)
        print("Model reply:", reply)
    except RuntimeError as error:
        print("Error:", error)
