"""Parámetros y rutas del pipeline RAG (S8 + S9 + S10). Live Review calidad del aire."""

from pathlib import Path

# --- Ingesta y chunking (Sprint 8) ---
CHUNK_SIZE = 800
CHUNK_OVERLAP = 100

DATA_DIR = Path(__file__).parent / "data"
OUTPUT_DIR = Path(__file__).parent / "output"
ENTREGABLES_DIR = Path(__file__).parent / "entregables"
CHUNKS_JSON = OUTPUT_DIR / "chunks.json"
EMBEDDINGS_JSON = OUTPUT_DIR / "embeddings.json"

EMBEDDING_MODEL = "gemini-embedding-2"
MAX_CHUNKS_EMBED: int | None = None # None = todos; 50 puede dejar fuera FAQ/PDF
EMBED_BATCH_SIZE = 20

MAX_FILAS_CSV: int | None = 40
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

# --- Indexación Chroma (Sprint 9) ---
CHROMA_DIR = OUTPUT_DIR / "chroma_db"
COLLECTION_NAME = "calidad_aire_madrid"
INDEX_BATCH_SIZE = 100

# --- Retrieval (Sprint 9) ---
TOP_K = 3
TOP_K_CANDIDATES = [1, 3, 5]

# --- Generación (Sprint 10) ---
GEMINI_MODEL = "gemini-3.1-flash-lite"
GENERATION_TEMPERATURE = 0.2

# --- Evaluación ---
QUERIES_EVAL_JSON = Path(__file__).parent / "queries" / "preguntas_eval.json"
