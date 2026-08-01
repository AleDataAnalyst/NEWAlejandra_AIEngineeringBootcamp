"""Parámetros y rutas del pipeline RAG (S8 + S9).

Centraliza chunking, embeddings, Chroma y retrieval.
Modifica aquí para experimentar (p. ej. TOP_K, CHUNK_SIZE) sin tocar la lógica.
"""

from pathlib import Path

# --- Ingesta y chunking (Sprint 8) ---
CHUNK_SIZE = 800
CHUNK_OVERLAP = 100

DATA_DIR = Path(__file__).parent / "data"
OUTPUT_DIR = Path(__file__).parent / "output"
CHUNKS_JSON = OUTPUT_DIR / "chunks.json"
EMBEDDINGS_JSON = OUTPUT_DIR / "embeddings.json"

EMBEDDING_MODEL = "gemini-embedding-2"
MAX_CHUNKS_EMBED: int | None = 5  # None = embeddear todos los chunks
EMBED_BATCH_SIZE = 50

EXTENSIONES_TEXTO = {".txt", ".md"}
EXTENSIONES_PDF = {".pdf"}
EXTENSIONES_CSV = {".csv"}

# --- Indexación Chroma (Sprint 9) ---
CHROMA_DIR = OUTPUT_DIR / "chroma_db"
COLLECTION_NAME = "agenda_cultural_madrid"
INDEX_BATCH_SIZE = 100  # cuántos vectores insertar por lote en Chroma

# --- Retrieval (Sprint 9) ---
TOP_K = 3  # fragmentos a recuperar por defecto
TOP_K_CANDIDATES = [1, 3, 5]  # valores de K en la evaluación

# --- Evaluación ---
QUERIES_EVAL_JSON = Path(__file__).parent / "queries" / "preguntas_eval.json"
