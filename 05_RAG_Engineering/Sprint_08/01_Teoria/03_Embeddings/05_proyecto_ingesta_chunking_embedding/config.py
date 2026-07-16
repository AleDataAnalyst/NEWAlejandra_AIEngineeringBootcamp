"""Parámetros y rutas del pipeline de ingesta.

Centraliza chunk_size, overlap y rutas a data/ y output/.
Modificar aquí para experimentar sin tocar load/clean/chunk.
"""

from pathlib import Path

CHUNK_SIZE = 800
CHUNK_OVERLAP = 100

DATA_DIR = Path(__file__).parent / "data"
OUTPUT_DIR = Path(__file__).parent / "output"
CHUNKS_JSON = OUTPUT_DIR / "chunks.json"
EMBEDDINGS_JSON = OUTPUT_DIR / "embeddings.json"

# Embeddings - modelo a utilizar de Gemini API
EMBEDDING_MODEL = "gemini-embedding-2"

# Limitar chunks al embeddear ( None = corpus completo)
MAX_CHUNKS_EMBED: int | None = 5

# Textos por llamada a embed_content (evita payloads enormes)
EMBED_BATCH_SIZE = 50

# Extensiones soportadas por load.py
EXTENSIONES_TEXTO = {".txt", ".md"}
EXTENSIONES_PDF = {".pdf"}
EXTENSIONES_CSV = {".csv"}
