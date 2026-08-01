"""Orquestación online RAG — Sprint 10 (COMPLETAR).

Contrato público: responder(pregunta) → dict
Usado por main.py --ask y app.py (Streamlit).
"""

from pathlib import Path

from .context import formatear_contexto
from .generate import generar_respuesta
from .prompts import build_rag_prompt
from .retriever import recuperar


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
    """Pipeline: retrieve → prompt → generate.

    Returns:
        dict con: respuesta, contexto, chunks, fuentes, error (o None).
    """
    # TODO:
    # 1. Si pregunta vacía → return con error y campos vacíos
    # 2. chunks = recuperar(pregunta, top_k=top_k)
    # 3. contexto = formatear_contexto(chunks)
    # 4. prompt = build_rag_prompt(contexto, pregunta)
    # 5. respuesta = generar_respuesta(prompt)
    # 6. return dict completo (error=None si OK)
    raise NotImplementedError("Implementa responder() en src/logic.py")
