from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
import os

from openai import OpenAI

@dataclass
class LLMConfig:
    model: str = "gpt-4o-mini"  # cheap + good enough for structured extraction
    temperature: float = 0.0

class OpenAILLM:
    def __init__(self, cfg: LLMConfig, api_key: Optional[str] = None):
        self.cfg = cfg
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))

    def generate(self, system: str, user: str) -> str:
        # Chat Completions style for simplicity; we can migrate to Responses later.
        resp = self.client.chat.completions.create(
            model=self.cfg.model,
            temperature=self.cfg.temperature,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
        return resp.choices[0].message.content
