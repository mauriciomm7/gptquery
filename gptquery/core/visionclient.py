# gptquery/core/clientfile.py
"""

"""
import time
import random
import requests
from pathlib import Path
from typing import Optional, Dict, Any, List
from ..processing.file_encoding import encode_image


class AuthenticationError(Exception):
    pass


class ModelValidationError(Exception):
    pass


class APIError(Exception):
    pass


class RateLimitError(Exception):
    pass


class GPTVisionClient:
    """OpenAI GPT client that supports chat completions with multimodal (image + text) input."""

    API_URL = "https://api.openai.com/v1/chat/completions"
    AVAILABLE_MODELS = [
        "gpt-5", "gpt-5-2025-08-07", "gpt-5-mini", "gpt-5-mini-2025-08-07",
        "gpt-4.1", "gpt-4.1-2025-04-14", "gpt-4.1-mini",
        "gpt-4o", "chatgpt-4o", "gpt-4o-mini"
    ]
    AUTH_HEADER = "Authorization"
    AUTH_PREFIX = "Bearer "
    USER_AGENT = "GPT-Query-OpenAI-Client"

    def __init__(self, api_key: str):
        if not api_key or not api_key.strip():
            raise AuthenticationError("API key is required.")
        self.api_key = api_key

    def _validate_model(self, model: str) -> None:
        if model not in self.AVAILABLE_MODELS:
            raise ModelValidationError(
                f"Invalid model '{model}'. Available: {', '.join(self.AVAILABLE_MODELS)}"
            )

    def extract(
        self,
        user_msg: str,
        system_msg: str,
        model: str,
        image_paths: Optional[List[str]] = None,
        max_tokens: int = 2000,
        temperature: float = 1.0,
        top_p: float = 1.0,
        frequency_penalty: float = 0.0,
        presence_penalty: float = 0.0,
        timeout: int = 60,
        max_retries: int = 3,
    ) -> str:
        """
        Run a multimodal chat completion (text + images).
        - user_msg: the textual user instruction.
        - system_msg: system guidance.
        - image_paths: list of paths to local image files.
        """

        self._validate_model(model)

        if not user_msg or not system_msg:
            raise APIError("Both user_msg and system_msg are required.")

        # Base message
        user_content = [{"type": "text", "text": user_msg}]

        # Attach images (if any)
        if image_paths:
            for path in image_paths:
                abs_path = Path(path).resolve()
                mime_type = self._guess_mime_type(abs_path)
                encoded_image = encode_image(abs_path)
                user_content.append({
                    "type": "image_url",
                    "image_url": {"url": f"data:{mime_type};base64,{encoded_image}"}
                }) # type: ignore

        messages = [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_content},
        ]

        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty,
        }

        headers = {
            self.AUTH_HEADER: f"{self.AUTH_PREFIX}{self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": self.USER_AGENT,
        }

        return self._make_request(payload, headers, timeout, max_retries)

    def _make_request(
        self, payload: dict, headers: dict, timeout: int, max_retries: int
    ) -> str:
        """Send the request with retry and backoff logic."""
        for attempt in range(max_retries + 1):
            try:
                response = requests.post(
                    self.API_URL, headers=headers, json=payload, timeout=timeout
                )

                if response.status_code == 200:
                    return self._extract_content(response.json())

                elif response.status_code == 401:
                    raise AuthenticationError("Invalid API key.")
                elif response.status_code == 429:
                    if attempt < max_retries:
                        time.sleep(self._calculate_backoff(attempt))
                        continue
                    raise RateLimitError("Rate limit exceeded.")
                elif response.status_code == 400:
                    raise APIError(self._extract_error_detail(response))
                else:
                    raise APIError(f"HTTP {response.status_code}: {response.text}")

            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
                if attempt < max_retries:
                    time.sleep(self._calculate_backoff(attempt))
                    continue
                raise APIError("Connection/timeout error.")
            except requests.exceptions.RequestException as e:
                raise APIError(f"Request failed: {str(e)}")

        raise APIError("Unexpected error after retries.")

    def _extract_content(self, response_data: Dict[str, Any]) -> str:
        """Extract text output from OpenAI response."""
        try:
            return response_data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError):
            raise APIError("Failed to parse response.")

    def _extract_error_detail(self, response: requests.Response) -> str:
        try:
            return response.json().get("error", {}).get("message", response.text)
        except Exception:
            return response.text

    def _calculate_backoff(self, attempt: int) -> float:
        base_delay = 2 ** attempt
        jitter = random.uniform(0.1, 0.5)
        return base_delay + jitter

    def _guess_mime_type(self, path: Path) -> str:
        """Guess MIME type from extension (default: image/png)."""
        ext = path.suffix.lower()
        if ext in [".jpg", ".jpeg"]:
            return "image/jpeg"
        elif ext == ".webp":
            return "image/webp"
        elif ext == ".gif":
            return "image/gif"
        return "image/png"
