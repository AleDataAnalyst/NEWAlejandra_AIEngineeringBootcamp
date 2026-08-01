"""Orquestación del pipeline RAG online — Sprint 10.

Función principal: responder(pregunta) — usada por main.py --ask y app.py Streamlit.
"""

from pathlib import Path

from .context import formatear_contexto
from .generate import generar_respuesta
from .prompts import build_rag_prompt
from .retriever import recuperar
from .validators import validar_contexto, validar_pregunta


def _extraer_fuentes(chunks: list[dict]) -> list[str]:
    """Lista única de nombres de archivo de los chunks recuperados."""
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
    """Pipeline completo: retrieve → prompt → generate.

    Returns:
        dict con claves: respuesta, contexto, chunks, fuentes, error (opcional).
    """
    ok, err = validar_pregunta(pregunta)
    if not ok:
        return {
            "respuesta": "",
            "contexto": "",
            "chunks": [],
            "fuentes": [],
            "error": err,
        }

    chunks = recuperar(pregunta, top_k=top_k)
    contexto = formatear_contexto(chunks)

    ok_ctx, err_ctx = validar_contexto(contexto)
    if not ok_ctx:
        return {
            "respuesta": "",
            "contexto": contexto,
            "chunks": chunks,
            "fuentes": _extraer_fuentes(chunks),
            "error": err_ctx,
        }

    prompt = build_rag_prompt(contexto, pregunta)
    respuesta = generar_respuesta(prompt)

    return {
        "respuesta": respuesta,
        "contexto": contexto,
        "chunks": chunks,
        "fuentes": _extraer_fuentes(chunks),
        "error": None,
    }
