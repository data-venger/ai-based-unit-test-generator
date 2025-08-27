import json
import requests
from typing import Optional


class OllamaClient:
    def __init__(self, endpoint: str, model: str, temperature: float = 0.2):
        self.endpoint = endpoint.rstrip("/")
        self.model = model
        self.temperature = temperature

    def generate(self, prompt: str, max_tokens: int = 1024, stop=None) -> str:
        """
        Calls Ollama /api/generate (non-stream) by aggregating stream chunks.
        """
        payload = {
            "model": self.model,
            "prompt": prompt,
            "temperature": self.temperature,
            "options": {"num_predict": max_tokens},
            "stream": True if "generate" in self.endpoint else True,
        }
        if stop:
            payload["stop"] = stop

        with requests.post(self.endpoint, json=payload, stream=True, timeout=600) as r:
            r.raise_for_status()
            chunks = []
            for line in r.iter_lines():
                if not line:
                    continue
                try:
                    obj = json.loads(line.decode("utf-8"))
                except Exception:
                    continue
                if "response" in obj:
                    chunks.append(obj["response"])
                if obj.get("done"):
                    break
            return "".join(chunks)
