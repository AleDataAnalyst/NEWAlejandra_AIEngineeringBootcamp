"""Indexación de embeddings.json en ChromaDB — Sprint 9 (Fase 1).

Objetivo didáctico
------------------
En Sprint 8 generaste vectores y los guardaste en un JSON. Eso aún no es un
índice de búsqueda: aquí los cargas en ChromaDB para poder hacer similarity
search (Fase 2).

Flujo:
  embeddings.json  →  collection.add()  →  output/chroma_db/

Funciones a completar:
  - obtener_cliente_chroma()
  - obtener_coleccion()
  - ejecutar_indexacion()

Helpers ya dados (no los reescribas):
  - _sanitizar_metadata, cargar_embeddings_json, _generar_id, borrar_coleccion

Prueba: python main.py --index
"""

import json

import chromadb

from config import (
    CHROMA_DIR,
    COLLECTION_NAME,
    EMBEDDING_MODEL,
    EMBEDDINGS_JSON,
    INDEX_BATCH_SIZE,
)


def _sanitizar_metadata(metadata: dict) -> dict:
    """Chroma solo acepta str, int, float, bool (no listas ni None).

    Si pasas None o una lista, collection.add() falla. Por eso convertimos
    lo raro a str y saltamos los None.
    """
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
    """Lee embeddings.json y devuelve (items, nombre del modelo usado).

    Cada item suele tener: text, vector, metadata.
    El modelo se guarda en metadatos del índice para documentar con qué
    embedding se construyó (debe coincidir con el de la consulta en Fase 2).
    """
    if not EMBEDDINGS_JSON.exists():
        raise FileNotFoundError(
            f"No existe {EMBEDDINGS_JSON}. Ejecuta antes: python main.py --prepare"
        )
    data = json.loads(EMBEDDINGS_JSON.read_text(encoding="utf-8"))
    modelo = data.get("embedding_model", EMBEDDING_MODEL)
    return data.get("items", []), modelo


def _generar_id(item: dict, indice: int) -> str:
    """ID único del chunk en Chroma (p. ej. chunk_0, chunk_1…).

    Chroma exige un id por documento. Preferimos chunk_index de la metadata
    (estable entre ejecuciones) y, si falta, el índice del bucle.
    """
    meta = item.get("metadata", {})
    chunk_index = meta.get("chunk_index", indice)
    return f"chunk_{chunk_index}"


def obtener_cliente_chroma() -> chromadb.PersistentClient:
    """Cliente Chroma que guarda el índice en disco (CHROMA_DIR).

    ¿Por qué PersistentClient y no efímero?
      Porque quieres reutilizar el índice entre ejecuciones (--query, --eval)
      sin volver a indexar cada vez.

    Pasos:
      1. Crear CHROMA_DIR si no existe (mkdir parents=True).
      2. Devolver chromadb.PersistentClient(path=str(CHROMA_DIR)).
         path=str(...) porque Chroma espera un string, no un Path.
    """
    # 1) Crear la carpeta si es la primera indexación
    # 2) Cliente persistente (path como string)
    raise NotImplementedError("Implementa obtener_cliente_chroma() en index.py")


def obtener_coleccion(
    client: chromadb.PersistentClient,
    crear: bool = True,
) -> chromadb.Collection:
    """Abre o crea la colección. Métrica: coseno (hnsw:space=cosine).

    Una colección = un “cajón” de vectores con el mismo espacio de embedding.
    Usamos distancia coseno (cuanto más baja, más similar).

    Parámetro crear:
      - True  (indexación): get_or_create_collection(...)
      - False (retrieval):  get_collection(...) — falla si aún no indexaste

    Pasos:
      if crear:
          # Indexar: si no existe la colección, la crea; si existe, la reutiliza
          return client.get_or_create_collection(
              name=COLLECTION_NAME,
              metadata={"hnsw:space": "cosine"},
          )
      # Consultar: no queremos crear una colección vacía por accidente
      return client.get_collection(name=COLLECTION_NAME)
    """
    # Si crear=True → get_or_create_collection (métrica coseno)
    # Si crear=False → get_collection (no inventar colección vacía)
    raise NotImplementedError("Implementa obtener_coleccion() en index.py")


def borrar_coleccion(client: chromadb.PersistentClient) -> None:
    """Elimina la colección (útil con --recreate-index).

    Si indexas dos veces sin borrar, puedes duplicar ids o mezclar estados.
    --recreate-index llama a esto antes de volver a añadir vectores.
    """
    try:
        client.delete_collection(COLLECTION_NAME)
        print(f"  Colección '{COLLECTION_NAME}' eliminada.")
    except Exception:
        print(f"  Colección '{COLLECTION_NAME}' no existía.")


def ejecutar_indexacion(recreate: bool = False) -> int:
    """Orquesta la Fase 1: embeddings.json → ChromaDB.

    Devuelve el total de documentos en la colección tras indexar.

    Idea clave: cada fila del índice = (vector + texto + metadata + id).
    El retrieval (Fase 2) busca por vector y te devuelve texto + metadata.

    Pasos:
      1. items, modelo = cargar_embeddings_json()
         → Si items está vacío, lanza ValueError.
      2. client = obtener_cliente_chroma()
         Si recreate: borrar_coleccion(client)
      3. collection = obtener_coleccion(client)  # crear=True por defecto
      4. Recorre items y rellena cuatro listas paralelas (alineadas por índice):
           - ids         ← _generar_id(item, i)
           - embeddings  ← item["vector"]   (vector numérico del chunk)
           - documents   ← item["text"]     (texto que devolverá el retrieval)
           - metadatas   ← _sanitizar_metadata(...) + embedding_model
      5. Inserta en lotes (INDEX_BATCH_SIZE) con collection.add(...)
      6. return collection.count()
    """
    # 1) Cargar artefactos del Sprint 8
    # 2) Cliente persistente + (opcional) reset de la colección
    # 3) Abrir/crear colección (métrica coseno)
    # 4) Preparar las cuatro listas que espera collection.add()
    # 5) Insertar en lotes para no saturar memoria con corpora grandes
    # 6) Comprobar cuántos documentos quedaron en el índice
    raise NotImplementedError("Implementa ejecutar_indexacion() en index.py")
