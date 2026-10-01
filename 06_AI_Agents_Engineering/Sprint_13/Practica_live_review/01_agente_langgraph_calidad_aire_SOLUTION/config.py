"""Configuración del proyecto — Sprint 13 LangGraph (paths, modelo y defaults)."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"

GEMINI_MODEL = "gemini-3.1-flash-lite"
TEMPERATURE = 0.3
MAX_STEPS_DEFAULT = 6
MAX_TURNS_DEFAULT = 8

# Open data Madrid — calidad del aire (tiempo real)
MADRID_AIRE_URL = (
    "https://ciudadesabiertas.madrid.es/dynamicAPI/API/query/"
    "calair_tiemporeal.json?pageSize=50"
)
HTTP_TIMEOUT_SECONDS = 12

GUIA_PATH = DATA_DIR / "guia_calidad_aire.txt"
AIRE_FALLBACK_PATH = DATA_DIR / "aire_fallback.json"

# Códigos de magnitud habituales (resumen para la tool API)
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
    # Msg 1: abre diálogo (sin tools ni prefs)
    "Quiero info de calidad del aire.",
    # Msg 2: empuja hora_actual
    "Quiero que te centres en la hora actual para contextualizar.",
    # Msg 3: fuerza RAG + API + prefs (útil también con --max-steps 1)
    (
        "Zona centro, contaminante NO2. Consulta la guía y datos de la API "
        "de Madrid. El tipo de consulta es interpretar un valor alto."
    ),
    "Añade otro paso al plan si falta.",
    "Perfecto, adelante con ese plan.",
]
