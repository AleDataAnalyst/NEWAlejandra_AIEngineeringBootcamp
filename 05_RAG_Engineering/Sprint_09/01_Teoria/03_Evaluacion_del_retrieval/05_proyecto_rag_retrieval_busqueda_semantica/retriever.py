"""Retriever — Sprint 9: pregunta → top-K chunks desde ChromaDB.

Flujo:
  1. Embeddear la pregunta con el mismo modelo que el índice (Gemini).
  2. collection.query() busca los vectores más cercanos (distancia coseno).
  3. Devolver texto + metadata + distance de cada hit.
"""

from google import genai

from config import COLLECTION_NAME, TOP_K
from embed import embeddear_consulta
from gemini_auth import configurar_gemini_api_key
from index import obtener_cliente_chroma, obtener_coleccion


def _log_retrieval(pregunta: str, top_k: int) -> None:
    """Mensajes de depuración en consola."""
    print(f'\n[RETRIEVAL] query="{pregunta}"')
    print(f"[RETRIEVAL] top_k={top_k} collection={COLLECTION_NAME}")


def _resultados_a_chunks(results: dict) -> list[dict]:
    """Convierte la respuesta anidada de Chroma en una lista plana de dicts.

    Chroma devuelve listas dentro de listas (una query → results[0]).
    """
    ids = results.get("ids", [[]])[0]
    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    chunks: list[dict] = []
    for i, chunk_id in enumerate(ids):
        chunk = {
            "id": chunk_id,
            "text": documents[i] if i < len(documents) else "",
            "metadata": metadatas[i] if i < len(metadatas) else {},
            "distance": distances[i] if i < len(distances) else None,
        }
        chunks.append(chunk)
    return chunks


def _imprimir_hits(chunks: list[dict]) -> None:
    """Resumen de cada fragmento recuperado (id, distancia, fuente)."""
    for i, chunk in enumerate(chunks, start=1):
        source = chunk.get("metadata", {}).get("source", "?")
        dist = chunk.get("distance")
        dist_txt = f"{dist:.4f}" if dist is not None else "n/a"
        print(f"[RETRIEVAL] #{i} id={chunk['id']} distance={dist_txt} source={source}")


def recuperar(pregunta: str, top_k: int | None = None) -> list[dict]:
    """Embed de la pregunta + similarity search en Chroma.

    Entrada: texto de la pregunta y cuántos chunks devolver (TOP_K por defecto).
    Salida: lista ordenada por similitud (menor distance = más parecido).
    """
    k = top_k if top_k is not None else TOP_K
    if k < 1:
        raise ValueError("top_k debe ser >= 1")

    _log_retrieval(pregunta, k)

    configurar_gemini_api_key()
    client = genai.Client()
    vector = embeddear_consulta(client, pregunta)

    chroma = obtener_cliente_chroma()
    collection = obtener_coleccion(chroma, crear=False)

    if collection.count() == 0:
        raise RuntimeError(
            "La colección Chroma está vacía. Ejecuta: python main.py --index"
        )

    results = collection.query(
        query_embeddings=[vector],
        n_results=min(k, collection.count()),
        include=["documents", "metadatas", "distances"],
    )

    chunks = _resultados_a_chunks(results)
    _imprimir_hits(chunks)
    return chunks
