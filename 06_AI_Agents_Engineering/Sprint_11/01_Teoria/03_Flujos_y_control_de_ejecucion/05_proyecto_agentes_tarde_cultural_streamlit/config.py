"""Configuración del proyecto — modelo, max_turns y guion demo."""

GEMINI_MODEL = "gemini-3.1-flash-lite"
MAX_TURNS_DEFAULT = 8  # tope de mensajes de usuario → LLM
TEMPERATURE = 0.3

# Guion de demo: 5 mensajes. Con --max-turns 2 se ve el corte (solo 2 de 5).
DEMO_MENSAJES = [
    "Quiero una tarde cultural.",
    "Cine o música en vivo, mejor barato.",
    "Zona centro.",
    "Unas 3 horas está bien.",
    "Sí, adelante con el plan.",
]
