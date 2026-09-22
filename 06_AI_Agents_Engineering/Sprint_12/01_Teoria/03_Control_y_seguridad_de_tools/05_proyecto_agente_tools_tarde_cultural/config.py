"""Configuración del proyecto — paths, modelo y defaults."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"

GEMINI_MODEL = "gemini-3.1-flash-lite"
TEMPERATURE = 0.3
MAX_STEPS_DEFAULT = 6
MAX_TURNS_DEFAULT = 8

MADRID_EVENTOS_URL = (
    "https://datos.madrid.es/egob/catalogo/206974-0-agenda-eventos-culturales-100.json"
)
HTTP_TIMEOUT_SECONDS = 12

GUIA_PATH = DATA_DIR / "guia_cultural.txt"
EVENTOS_FALLBACK_PATH = DATA_DIR / "eventos_fallback.json"

DEMO_MENSAJES = [
    # Msg 1: fuerza tools (útil con --max-steps 1) y ya trae prefs mínimas
    "Quiero una tarde cultural barata en el centro de Madrid. Consulta la guía y algún evento del catálogo.",
    "¿Qué horarios gratis recomienda la guía?",
    "Añade otra idea si puedes y afina el plan.",
    "¿Cuánto tiempo crees que necesitamos? Pon duración si falta.",
    "Perfecto, adelante con ese plan.",
]
