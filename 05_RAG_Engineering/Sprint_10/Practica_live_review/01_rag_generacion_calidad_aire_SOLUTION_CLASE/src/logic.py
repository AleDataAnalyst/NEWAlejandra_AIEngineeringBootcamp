"""Orquestación online RAG — Sprint 10 (SOLUTION)."""

from pathlib import Path

from .context import formatear_contexto
from .generate import generar_respuesta
from .prompts import build_rag_prompt
from .retriever import recuperar


def _extraer_fuentes(chunks: list[dict]) -> list[str]:
    fuentes: list[str] = []
    vistos: set[str] = set()
    for chunk in chunks:
        source = chunk.get("metadata", {}).get("source", "?")
        nombre = Path(str(source)).name
        if nombre not in vistos:
            vistos.add(nombre)
            fuentes.append(nombre)
    return fuentes


def responder(pregunta: str, top_k: int | None = None) -> dict:
    """Pipeline: retrieve → prompt → generate."""
    if not (pregunta or "").strip():
        return {
            "respuesta": "",
            "contexto": "",
            "chunks": [],
            "fuentes": [],
            "error": "La pregunta no puede estar vacía.",
        }

    chunks = recuperar(pregunta.strip(), top_k=top_k)
    contexto = formatear_contexto(chunks)
    prompt = build_rag_prompt(contexto, pregunta.strip())
    respuesta = generar_respuesta(prompt)

    return {
        "respuesta": respuesta,
        "contexto": contexto,
        "chunks": chunks,
        "fuentes": _extraer_fuentes(chunks),
        "error": None,
    }
