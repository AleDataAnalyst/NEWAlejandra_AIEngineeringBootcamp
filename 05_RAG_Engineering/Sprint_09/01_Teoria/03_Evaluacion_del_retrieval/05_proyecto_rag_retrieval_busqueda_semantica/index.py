"""Indexación de embeddings.json en ChromaDB — Sprint 9.

Flujo: embeddings.json → collection.add() → output/chroma_db/

Chroma persiste los vectores en disco para buscar por similitud sin
volver a embeddear todo el corpus en cada consulta.
"""

import json
from pathlib import Path

import chromadb

from config import (
    CHROMA_DIR,
    COLLECTION_NAME,
    EMBEDDING_MODEL,
    EMBEDDINGS_JSON,
    INDEX_BATCH_SIZE,
)


def _sanitizar_metadata(metadata: dict) -> dict:
    """Chroma solo acepta str, int, float, bool en metadatas (no listas ni None)."""
    limpia: dict = {}
    for clave, valor in metadata.items():
        if valor is None:
            continue
        if isinstance(valor, (str, int, float, bool)):
            limpia[clave] = valor
        else:
            limpia[clave] = str(valor)
    return limpia


def cargar_embeddings_json() -> tuple[list[dict], str]:
    """Lee embeddings.json y devuelve (items, nombre del modelo usado)."""
    if not EMBEDDINGS_JSON.exists():
        raise FileNotFoundError(
            f"No existe {EMBEDDINGS_JSON}. Ejecuta antes: python main.py --prepare"
        )
    data = json.loads(EMBEDDINGS_JSON.read_text(encoding="utf-8"))
    modelo = data.get("embedding_model", EMBEDDING_MODEL)
    return data.get("items", []), modelo


def _generar_id(item: dict, indice: int) -> str:
    """ID único del chunk en Chroma (p. ej. chunk_0, chunk_1…)."""
    meta = item.get("metadata", {})
    chunk_index = meta.get("chunk_index", indice)
    return f"chunk_{chunk_index}"


def obtener_cliente_chroma() -> chromadb.PersistentClient:
    """Cliente Chroma que guarda el índice en CHROMA_DIR (persistente en disco)."""
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(path=str(CHROMA_DIR))


def obtener_coleccion(
    client: chromadb.PersistentClient,
    crear: bool = True,
) -> chromadb.Collection:
    """Abre o crea la colección. Métrica: coseno (hnsw:space=cosine)."""
    if crear:
        return client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )
    return client.get_collection(name=COLLECTION_NAME)


def borrar_coleccion(client: chromadb.PersistentClient) -> None:
    """Elimina la colección (útil con --recreate-index)."""
    try:
        client.delete_collection(COLLECTION_NAME)
        print(f"  Colección '{COLLECTION_NAME}' eliminada.")
    except Exception:
        print(f"  Colección '{COLLECTION_NAME}' no existía.")


def ejecutar_indexacion(recreate: bool = False) -> int:
    """Carga embeddings.json en Chroma. Devuelve el total indexado."""
    items, modelo_json = cargar_embeddings_json()
    if not items:
        raise ValueError("embeddings.json no contiene items.")

    client = obtener_cliente_chroma()
    if recreate:
        borrar_coleccion(client)

    collection = obtener_coleccion(client)

    ids: list[str] = []
    embeddings: list[list[float]] = []
    documents: list[str] = []
    metadatas: list[dict] = []

    for i, item in enumerate(items):
        ids.append(_generar_id(item, i))
        embeddings.append(item["vector"])
        documents.append(item["text"])
        meta = _sanitizar_metadata(item.get("metadata", {}))
        meta["embedding_model"] = modelo_json
        metadatas.append(meta)

    print(f"Indexando {len(ids)} vectores en '{COLLECTION_NAME}' ...")

    # Insertamos en lotes para no saturar memoria con corpus grandes
    for inicio in range(0, len(ids), INDEX_BATCH_SIZE):
        fin = inicio + INDEX_BATCH_SIZE
        collection.add(
            ids=ids[inicio:fin],
            embeddings=embeddings[inicio:fin],
            documents=documents[inicio:fin],
            metadatas=metadatas[inicio:fin],
        )

    total = collection.count()
    print(f"  ChromaDB: {total} documentos en {CHROMA_DIR}")
    return total
