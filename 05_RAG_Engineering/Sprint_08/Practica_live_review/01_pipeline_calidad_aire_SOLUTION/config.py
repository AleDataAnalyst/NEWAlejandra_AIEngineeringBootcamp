"""Parámetros centralizados del pipeline.

Aquí viven rutas, límites y constantes. Puedes cambiar CHUNK_SIZE / CHUNK_OVERLAP
para experimentar (ver entregable estrategia_chunking.md).
"""

from pathlib import Path

# --- Chunking (ver chunk.py) ---
CHUNK_SIZE = 800
CHUNK_OVERLAP = 100

# --- Rutas del proyecto ---
DATA_DIR = Path(__file__).parent / "data"
OUTPUT_DIR = Path(__file__).parent / "output"
ENTREGABLES_DIR = Path(__file__).parent / "entregables"
CHUNKS_JSON = OUTPUT_DIR / "chunks.json"
EMBEDDINGS_JSON = OUTPUT_DIR / "embeddings.json"

# --- Embeddings Gemini (ver embed.py) ---
EMBEDDING_MODEL = "gemini-embedding-2"
MAX_CHUNKS_EMBED: int | None = 50  # None = embeddear todos los chunks
EMBED_BATCH_SIZE = 50  # cuántos textos enviar por llamada a la API

# --- CSV meteorológico (ver load.py) ---
MAX_FILAS_CSV: int | None = 100  # None = leer todas las filas
CSV_METEO = "calidad_aire_datos_meteo_mes.csv"

EXTENSIONES_TEXTO = {".txt", ".md"}
EXTENSIONES_PDF = {".pdf"}
EXTENSIONES_CSV = {".csv"}

# Códigos de magnitud del Ayuntamiento de Madrid (usado en load.py)
MAGNITUDES: dict[int, str] = {
    81: "Velocidad del viento",
    82: "Dirección del viento",
    83: "Temperatura",
    86: "Humedad relativa",
    87: "Presión barométrica",
    88: "Radiación solar",
    89: "Precipitación",
}
