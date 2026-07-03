# gemini_client.py — llamadas a Gemini

import time
from dataclasses import dataclass

from google import genai
from google.genai import types

from config import MAX_TOKENS_INPUT, MODEL, TEMPERATURE
from gemini_auth import configurar_gemini_api_key

configurar_gemini_api_key()


@dataclass
class MetricasLlamada:
    elapsed_ms: int
    prompt_tokens: int | None
    output_tokens: int | None
    total_tokens: int | None


_client_instance: genai.Client | None = None


def _client() -> genai.Client:
    global _client_instance
    if _client_instance is None:
        _client_instance = genai.Client()
    return _client_instance


def count_tokens(contents: str) -> int:
    r = _client().models.count_tokens(model=MODEL, contents=contents)
    return int(r.total_tokens or 0)


def llamar_gemini(
    prompt: str,
    *,
    temperature: float = TEMPERATURE,
) -> tuple[str, MetricasLlamada]:
    started = time.time()
    response = _client().models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(temperature=temperature),
    )
    elapsed_ms = int((time.time() - started) * 1000)
    um = response.usage_metadata
    metricas = MetricasLlamada(
        elapsed_ms=elapsed_ms,
        prompt_tokens=getattr(um, "prompt_token_count", None),
        output_tokens=getattr(um, "candidates_token_count", None),
        total_tokens=getattr(um, "total_token_count", None),
    )
    return (response.text or "").strip(), metricas


def safe_generate(prompt: str, *, temperature: float = TEMPERATURE) -> tuple[str, MetricasLlamada]:
    tokens = count_tokens(prompt)
    if tokens > MAX_TOKENS_INPUT:
        raise ValueError(
            f"Prompt demasiado grande: {tokens} tokens (máx {MAX_TOKENS_INPUT})."
        )
    return llamar_gemini(prompt, temperature=temperature)
