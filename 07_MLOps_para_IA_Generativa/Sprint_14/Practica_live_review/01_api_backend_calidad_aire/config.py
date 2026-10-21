"""Configuración — agente calidad del aire + SQLite historial."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
ASSETS_DIR = ROOT / "assets"

DATABASE_URL = f"sqlite:///{ROOT / 'historial.db'}"

GEMINI_MODEL = "gemini-2.5-flash"
TEMPERATURE = 0.3
MAX_STEPS_DEFAULT = 4
MAX_TURNS_DEFAULT = 6
MAX_ITER = 8

MADRID_AIRE_URL = (
    "https://ciudadesabiertas.madrid.es/dynamicAPI/API/query/"
    "calair_tiemporeal.json?pageSize=50"
)
HTTP_TIMEOUT_SECONDS = 12

GUIA_PATH = DATA_DIR / "guia_calidad_aire.txt"
AIRE_FALLBACK_PATH = DATA_DIR / "aire_fallback.json"

IMAGEN_DEFAULT_PATH = ASSETS_DIR / "imagen_demo.jpg"

MAGNITUDES = {
    "1": "SO2",
    "6": "CO",
    "7": "NO",
    "8": "NO2",
    "9": "PM2.5",
    "10": "PM10",
    "12": "NOx",
    "14": "O3",
    "20": "TOL",
    "30": "BEN",
    "42": "TCH",
    "44": "CH4",
}

DEMO_MENSAJES = [
    (
        "Zona centro, contaminante NO2. Consulta la guía y datos de la API "
        "de Madrid. Propón un plan breve de qué hacer / cómo interpretar."
    ),
]
