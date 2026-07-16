"""Generación de embeddings con Gemini a partir de chunks.json.

Lee los fragmentos de texto, los envía a la API de Gemini y guarda los vectores
en embeddings.json (un vector numérico por chunk).
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
    """Convierte la respuesta de la API en una lista de floats.

    La API devuelve un objeto con atributo .values; esta función
    extrae la lista de números que forman el vector.
    """
    if hasattr(embedding_obj, "values"):
        return list(embedding_obj.values)
    return list(embedding_obj)


def cargar_chunks_json() -> list[dict]:
    """Lee chunks.json y devuelve la lista de fragmentos.

    Entrada: config.CHUNKS_JSON (generado por el pipeline de ingesta).
    Salida: lista de dicts, cada uno con 'text' y 'metadata'.
    """
    if not CHUNKS_JSON.exists():
        raise FileNotFoundError(
            f"No existe {CHUNKS_JSON}. Ejecuta antes: python main.py"
        )
    data = json.loads(CHUNKS_JSON.read_text(encoding="utf-8"))
    return data.get("chunks", [])


def embeddear_textos(client: genai.Client, textos: list[str]) -> list[list[float]]:
    """Pide a Gemini un vector de embedding por cada texto.

    Entrada: cliente de API y lista de textos (un chunk = un texto).
    Salida: lista de vectores (cada vector es una lista de floats).

    Importante: cada texto va en un types.Content separado para obtener
    un embedding independiente por chunk (no uno solo para todo el lote).
    """
    if not textos:
        return []

    vectores: list[list[float]] = []

    # Procesamos en lotes para no enviar demasiados textos en una sola llamada
    for inicio in range(0, len(textos), EMBED_BATCH_SIZE):
        lote = textos[inicio : inicio + EMBED_BATCH_SIZE]

        # Un types.Content por texto → un vector por chunk
        contents = [types.Content(parts=[types.Part(text=t)]) for t in lote]

        result = client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=contents,
        )

        lote_vectores = [_extraer_vector(emb) for emb in result.embeddings]

        # Comprobación: la API debe devolver tantos vectores como textos enviados
        if len(lote_vectores) != len(lote):
            raise RuntimeError(
                f"Se esperaban {len(lote)} embeddings, se recibieron {len(lote_vectores)}. "
                "¿Usaste types.Content por texto?"
            )
        vectores.extend(lote_vectores)

    return vectores


def ejecutar_embeddings() -> tuple[list[dict], Path]:
    """Lee chunks.json, genera vectores con Gemini y guarda embeddings.json.

    Usa config.EMBEDDING_MODEL y respeta config.MAX_CHUNKS_EMBED si está definido.
    Salida: (items con text+vector+metadata, ruta del JSON guardado).
    """
    configurar_gemini_api_key()
    client = genai.Client()

    chunks = cargar_chunks_json()
    total_disponibles = len(chunks)

    # En demo limitamos cuántos chunks embeddear (ver MAX_CHUNKS_EMBED en config.py)
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

    # Unimos cada chunk con su vector correspondiente (mismo orden)
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
