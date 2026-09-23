"""Configuración — modelo, max_turns y guion demo (calidad del aire)."""

GEMINI_MODEL = "gemini-3.1-flash-lite"
TEMPERATURE = 0.2

MAX_TURNS_DEFAULT = 8  # tope de mensajes de usuario → LLM

# Guion de demo: 5 mensajes. Con --max-turns 2 se ve el corte (solo 2 de 5).
DEMO_MENSAJES = [
    "Quiero orientarme sobre calidad del aire en Madrid.",
    "Me interesa el NO2 o la magnitud 83.",
    "Zona centro, cerca de Escuelas Aguirre.",
    "Quiero entender qué significa un valor alto.",
    "Sí, adelante con el plan de consulta.",
]
