"""Parámetros y rutas del pipeline (S8 dado + S9 a implementar).

Modifica TOP_K, TOP_K_CANDIDATES o MAX_CHUNKS_EMBED para experimentar.
"""

from pathlib import Path

# --- Ingesta y chunking (Sprint 8 — dado) ---
CHUNK_SIZE = 800
CHUNK_OVERLAP = 100

DATA_DIR = Path(__file__).parent / "data"
OUTPUT_DIR = Path(__file__).parent / "output"
ENTREGABLES_DIR = Path(__file__).parent / "entregables"
CHUNKS_JSON = OUTPUT_DIR / "chunks.json"
EMBEDDINGS_JSON = OUTPUT_DIR / "embeddings.json"

EMBEDDING_MODEL = "gemini-embedding-2"
MAX_CHUNKS_EMBED: int | None = 50  # None = embeddear todos los chunks
EMBED_BATCH_SIZE = 50

# --- CSV meteorológico (Sprint 8 — dado) ---
MAX_FILAS_CSV: int | None = 100  # None = leer todas las filas
CSV_METEO = "calidad_aire_datos_meteo_mes.csv"

EXTENSIONES_TEXTO = {".txt", ".md"}
EXTENSIONES_PDF = {".pdf"}
EXTENSIONES_CSV = {".csv"}

MAGNITUDES: dict[int, str] = {
    81: "Velocidad del viento",
    82: "Dirección del viento",
    83: "Temperatura",
    86: "Humedad relativa",
    87: "Presión barométrica",
    88: "Radiación solar",
    89: "Precipitación",
}

# --- Indexación Chroma (Sprint 9 — Fase 1) ---
CHROMA_DIR = OUTPUT_DIR / "chroma_db"
COLLECTION_NAME = "calidad_aire_madrid"
INDEX_BATCH_SIZE = 100

# --- Retrieval (Sprint 9 — Fase 2) ---
TOP_K = 3
TOP_K_CANDIDATES = [1, 3, 5]

# --- Evaluación (Sprint 9 — Fase 3) ---
QUERIES_EVAL_JSON = Path(__file__).parent / "queries" / "preguntas_eval.json"
