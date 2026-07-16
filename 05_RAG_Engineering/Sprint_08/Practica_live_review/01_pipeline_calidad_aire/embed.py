"""Generación de embeddings con Gemini.

Lee output/chunks.json, convierte cada chunk en un vector numérico y guarda
output/embeddings.json. Requiere GEMINI_API_KEY en .env (ver gemini_auth.py).
"""

import json
import time
from pathlib import Path

from google import genai
from google.genai import types

from config import (
    CHUNKS_JSON,
    EMBED_BATCH_SIZE,
    EMBEDDING_MODEL,
    EMBEDDINGS_JSON,
    MAX_CHUNKS_EMBED,
)
from gemini_auth import configurar_gemini_api_key


def _extraer_vector(embedding_obj) -> list[float]:
    """La API devuelve objetos con .values; esto unifica el formato a list[float]."""
    if hasattr(embedding_obj, "values"):
        return list(embedding_obj.values)
    return list(embedding_obj)


def cargar_chunks_json() -> list[dict]:
    """Lee la lista de chunks generada en la Fase 1 (pipeline.py)."""
    if not CHUNKS_JSON.exists():
        raise FileNotFoundError(
            f"No existe {CHUNKS_JSON}. Ejecuta antes la ingesta (Fase 1)."
        )
    data = json.loads(CHUNKS_JSON.read_text(encoding="utf-8"))
    return data.get("chunks", [])


def embeddear_textos(client: genai.Client, textos: list[str]) -> list[list[float]]:
    """Envía textos a Gemini en lotes y devuelve vectores en el mismo orden."""
    if not textos:
        return []

    vectores: list[list[float]] = []

    for inicio in range(0, len(textos), EMBED_BATCH_SIZE):
        lote = textos[inicio : inicio + EMBED_BATCH_SIZE]

        # Formato que espera la API: lista de Content, cada uno con el texto
        contents = [types.Content(parts=[types.Part(text=t)]) for t in lote]

        result = client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=contents,
        )

        lote_vectores = [_extraer_vector(emb) for emb in result.embeddings]
        vectores.extend(lote_vectores)

    return vectores


def ejecutar_embeddings() -> tuple[list[dict], Path]:
    """Orquesta Fase 2: chunks.json → vectores → embeddings.json."""
    configurar_gemini_api_key()
    client = genai.Client()

    chunks = cargar_chunks_json()
    total_disponibles = len(chunks)

    # Límite de práctica para no saturar la API (configurable en config.py)
    if MAX_CHUNKS_EMBED is not None:
        chunks = chunks[:MAX_CHUNKS_EMBED]

    textos = [c["text"] for c in chunks]

    inicio = time.perf_counter()
    vectores = embeddear_textos(client, textos)
    latencia_ms = (time.perf_counter() - inicio) * 1000

    print(
        f"Embeddings: {len(textos)} chunks en {latencia_ms:.0f} ms ({EMBEDDING_MODEL})"
    )
    if len(textos) < total_disponibles:
        print(f"  (de {total_disponibles} en {CHUNKS_JSON.name}; ver MAX_CHUNKS_EMBED)")

    # Un item = texto + vector + metadata (misma metadata que en chunks.json)
    items = []
    for chunk, vector in zip(chunks, vectores):
        items.append(
            {
                "text": chunk["text"],
                "vector": vector,
                "metadata": chunk.get("metadata", {}),
            }
        )

    payload = {
        "embedding_model": EMBEDDING_MODEL,
        "total": len(items),
        "total_chunks_en_origen": total_disponibles,
        "dimensions": len(vectores[0]) if vectores else 0,
        "items": items,
    }

    EMBEDDINGS_JSON.parent.mkdir(parents=True, exist_ok=True)
    EMBEDDINGS_JSON.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"  Guardado: {EMBEDDINGS_JSON} ({payload['dimensions']} dimensiones)")

    return items, EMBEDDINGS_JSON
