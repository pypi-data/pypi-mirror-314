"""OpenAI API client for the Scout app."""

import requests

TIMEOUT_SECONDS = 30


class OpenAIClient:
    """Encapsulates the OpenAI API client."""

    def __init__(self, api_key: str):
        """
        Initialize the OpenAIClient class with the API key.

        Raises:
            ValueError: If the OPENAI_API_KEY environment variable is not set.
        """
        self.api_key = api_key
        self.base_url = "https://api.openai.com/v1/chat/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

    def ask(self, messages: list, model: str = "gpt-4o", temperature: float = 0) -> str:
        """
        Ask a question to the OpenAI API.

        Args:
            messages (list): A list of messages in the conversation.
            model (str): The model to use for completion.
            temperature (float): The sampling temperature.

        Returns:
            str: The response from the OpenAI API.
        """
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
        }
        response = requests.post(
            self.base_url, headers=self.headers, json=payload, timeout=TIMEOUT_SECONDS
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
