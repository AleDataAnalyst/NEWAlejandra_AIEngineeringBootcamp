# config.py — reglas del juego (sin lógica de negocio)

VALID_TIPOS = ["summary", "translate", "qa"]

PRIORIDAD_MIN = 1
PRIORIDAD_MAX = 5

import re

PATRON_CODIGO = re.compile(r"^TKT-\d{4}$")

# Placeholder para Unidad 2 (sin llamar a la API en esta unidad)
MODEL = "gemini-proximamente"
