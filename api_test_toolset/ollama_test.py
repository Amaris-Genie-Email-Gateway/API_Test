import requests
from typing import List, Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed


class OllamaModelTester:
    """
    A class for testing the reachability of models served by a local Ollama instance.
    """

    def __init__(self, api_base_url: str, prompt: str, test_models: Optional[List[str]] = None):
        """
        Initialize the tester, validate the base URL, and fetch the list of models.

        Args:
            api_base_url (str): The base URL of the Ollama API endpoint.
            prompt (str): The prompt message to send during testing.
            test_models (Optional[List[str]]): A list of specific models to test. If None, all available models will be tested.

        Raises:
            ConnectionError: If the API endpoint is not reachable.
            ValueError: If no models are found on the server or invalid test_models are provided.
        """
        self.api_base_url = api_base_url.rstrip("/")
        self.chat_url = f"{self.api_base_url}/api/chat"
        self.models_url = f"{self.api_base_url}/api/tags"
        self.prompt = prompt
        self.models: List[str] = []

        # Check server connectivity
        try:
            response = requests.get(self.api_base_url, timeout=5)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Failed to reach Ollama at {self.api_base_url}. Error: {e}")

        # Fetch available models
        available_models = self._fetch_models()
        if not available_models:
            raise ValueError("No models found on the Ollama server.")

        # Validate user-specified models if any
        if test_models is not None:
            invalid_models = [m for m in test_models if m not in available_models]
            if invalid_models:
                raise ValueError(f"Invalid model(s) specified: {invalid_models}")
            self.models = test_models
        else:
            self.models = available_models

    def _fetch_models(self) -> List[str]:
        """
        Retrieve the list of available models from the Ollama instance.

        Returns:
            List[str]: A list of model names.
        """
        try:
            response = requests.get(self.models_url, timeout=10)
            response.raise_for_status()
            data = response.json()
            return [item["name"] for item in data.get("models", [])]
        except requests.exceptions.RequestException as e:
            print(f"Error fetching model list: {e}")
            return []

    def _build_payload(self, model_name: str) -> Dict[str, Any]:
        """
        Construct the payload for chat API request.

        Args:
            model_name (str): Name of the model to query.

        Returns:
            Dict[str, Any]: JSON payload for the API request.
        """
        return {
            "model": model_name,
            "stream": False,
            "messages": [
                {"role": "user", "content": self.prompt}
            ]
        }

    def test_model(self, model_name: str) -> None:
        """
        Send a chat request to the specified model and print the result.

        Args:
            model_name (str): Name of the model to test.
        """
        print(f"\n[Testing model: {model_name}]")
        payload = self._build_payload(model_name)

        try:
            response = requests.post(self.chat_url, json=payload, timeout=300)
            response.raise_for_status()
            result = response.json()
            content = result.get("message", {}).get("content", "[No content returned]")
            print(f"{model_name}: Model is reachable.")
            print(f"Response: {content}")
        except requests.exceptions.RequestException as e:
            print(f"{model_name}: Failed to reach model.")
            print(f"Error: {e}")

    def run_sequential_test(self) -> None:
        """
        Run a sequential test on all available models.
        """
        print("=== Starting SEQUENTIAL model reachability test ===")
        for model in self.models:
            self.test_model(model)
        print("=== Sequential test completed ===\n")

    def run_concurrent_test(self) -> None:
        """
        Run a concurrent test on all available models using ThreadPoolExecutor.
        """
        print("=== Starting CONCURRENT model reachability test ===")
        with ThreadPoolExecutor(max_workers=len(self.models)) as executor:
            futures = {executor.submit(self.test_model, model): model for model in self.models}
            for future in as_completed(futures):
                model = futures[future]
                try:
                    future.result()
                except Exception as e:
                    print(f"{model}: Exception during concurrent test. Error: {e}")
        print("=== Concurrent test completed ===")


# Entry point example usage
if __name__ == "__main__":
    try:
        # Replace with your actual endpoint and prompt
        test_models=[
            "hf.co/unsloth/Qwen3-14B-GGUF:Q4_K_M",
            "hf.co/unsloth/DeepSeek-R1-0528-Qwen3-8B-GGUF:Q4_K_M",
            "cyberllm-02:latest"
            ]
        tester = OllamaModelTester(api_base_url="http://192.168.1.21:11434", prompt="Hello, who are you?",test_models=test_models)
        tester.run_concurrent_test()
    except (ConnectionError, ValueError) as e:
        print(f"Initialization failed: {e}")
