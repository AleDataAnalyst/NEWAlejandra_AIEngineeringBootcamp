"""Cliente de la API de Gemini con medición de métricas.

Envía prompts al modelo indicado y devuelve la respuesta junto con
latencia (ms) y conteo de tokens (prompt, salida y total).
Reutiliza una única instancia del cliente para todas las llamadas.
"""

import time
from dataclasses import dataclass

from google import genai
from google.genai import types

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


def llamar_gemini(
    prompt: str,
    *,
    model: str,
    temperature: float = 0.3,
) -> tuple[str, MetricasLlamada]:
    started = time.time()
    response = _client().models.generate_content(
        model=model,
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
