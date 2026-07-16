"""context.py — Selección de contexto desde el FAQ (código dado).

Qué hace este módulo:
  - `cargar_faq()` lee `data/faq.json`.
  - `seleccionar_faq()` elige entradas relevantes por keywords (sin embeddings).

Para qué sirve:
  - No inyectar todo el FAQ en cada prompt (ahorro de tokens y ruido).

Qué NO debes hacer aquí:
  - Este archivo ya está completo en la práctica. Léelo antes de la live review.
  - Si quieres repasar la lógica, consulta los vídeos del Sprint 5.
"""

import json
from pathlib import Path


def cargar_faq(ruta: Path) -> list[dict]:
    """Carga faq.json desde disco."""
    with ruta.open(encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("faq.json debe ser una lista de entradas")
    return data


def seleccionar_faq(faq: list[dict], consulta: str, max_entradas: int = 1) -> list[dict]:
    """Elige entradas del FAQ por keywords (sin vector DB)."""
    q = (consulta or "").lower()
    puntuaciones: list[tuple[int, dict]] = []

    for entry in faq:
        score = 0
        for kw in entry.get("keywords", []):
            if kw.lower() in q:
                score += 2
        if entry.get("topic_id", "").lower() in q:
            score += 3
        if score > 0:
            puntuaciones.append((score, entry))

    puntuaciones.sort(key=lambda x: x[0], reverse=True)
    return [e for _, e in puntuaciones[:max_entradas]]
