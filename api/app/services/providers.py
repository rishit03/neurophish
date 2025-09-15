from typing import Optional
from openai import OpenAI
import os

PROVIDERS = {
    "Groq": {
        "base_url": "https://api.groq.com/openai/v1",
        "env": "GROQ_API_KEY",
    },
    "Together.ai": {
        "base_url": "https://api.together.xyz/v1",
        "env": "TOGETHER_API_KEY",
    },
    "OpenRouter.ai": {
        "base_url": "https://openrouter.ai/api/v1",
        "env": "OPENROUTER_API_KEY",
    },
}

class ProviderClient:
    def __init__(self, provider: str):
        meta = PROVIDERS[provider]
        key = os.getenv(meta["env"]) or ""
        if not key:
            raise RuntimeError(f"Missing API key for {provider} ({meta['env']})")
        self.client = OpenAI(api_key=key, base_url=meta["base_url"])

    def chat(self, model: str, prompt: str) -> str:
        res = self.client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=512,
        )
        return res.choices[0].message.content or ""
