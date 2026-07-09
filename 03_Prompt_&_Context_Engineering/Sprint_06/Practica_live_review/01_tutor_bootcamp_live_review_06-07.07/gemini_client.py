"""gemini_client.py — Llamadas a la API de Gemini y métricas.

Qué hace este módulo:
  - `llamar_gemini_json(prompt)` — Fase 1: espera respuesta JSON del modelo.
  - `safe_generate_texto(prompt)` — Fase 2: texto libre + tokens y tiempo.
  - Comprueba que el prompt no supere `MAX_TOKENS_INPUT` antes de llamar.

Para qué sirve:
  - Centralizar la comunicación con Gemini (modelo, temperatura, errores de API).
  - Separar «construir el prompt» (prompts.py) de «enviarlo al modelo» (aquí).

Qué NO debes hacer aquí:
  - No construyas prompts en este archivo → usa `prompts.py`.
  - Este archivo ya está completo; no necesitas modificarlo en la práctica.
"""

import time
from dataclasses import dataclass

from google import genai
from google.genai import types

from config import MAX_TOKENS_INPUT, MODEL, TEMPERATURE_JSON, TEMPERATURE_TEXTO
from gemini_auth import configurar_gemini_api_key

_client: genai.Client | None = None


@dataclass
class MetricasLlamada:
    elapsed_ms: int
    prompt_tokens: int | None
    output_tokens: int | None
    total_tokens: int | None


def _cliente() -> genai.Client:
    global _client
    if _client is None:
        configurar_gemini_api_key()
        _client = genai.Client()
    return _client


def count_tokens(prompt: str) -> int:
    r = _cliente().models.count_tokens(model=MODEL, contents=prompt)
    return int(r.total_tokens or 0)


def llamar_gemini_json(prompt: str) -> str:
    response = _cliente().models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=TEMPERATURE_JSON,
            response_mime_type="application/json",
        ),
    )
    return (response.text or "").strip()


def llamar_gemini_texto(prompt: str) -> tuple[str, MetricasLlamada]:
    t0 = time.time()
    response = _cliente().models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(temperature=TEMPERATURE_TEXTO),
    )
    ms = int((time.time() - t0) * 1000)
    um = response.usage_metadata
    metricas = MetricasLlamada(
        elapsed_ms=ms,
        prompt_tokens=getattr(um, "prompt_token_count", None),
        output_tokens=getattr(um, "candidates_token_count", None),
        total_tokens=getattr(um, "total_token_count", None),
    )
    return (response.text or "").strip(), metricas


def safe_generate_texto(prompt: str) -> tuple[str, MetricasLlamada]:
    tokens = count_tokens(prompt)
    if tokens > MAX_TOKENS_INPUT:
        raise ValueError(
            f"Prompt demasiado grande: {tokens} tokens (máx {MAX_TOKENS_INPUT}). "
            "Recorta contexto en Python."
        )
    return llamar_gemini_texto(prompt)
