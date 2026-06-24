"""validators.py — Validación de consultas en Python (Fase 1).

Qué hace este módulo:
  - Comprueba nombre, email y mensaje antes de llamar a Gemini.
  - Devuelve una lista de errores (vacía = consulta válida).

Para qué sirve:
  - Ahorrar tokens y evitar llamadas a la API con datos mal formados.
  - Es el primer paso del flujo en `clasificar_consulta()` (logic.py).

Función a implementar:
  - `validar_consulta(datos)` — ver README FASE 1, Tarea 1.
"""

from config import (
    MAX_CHARS_MENSAJE,
    MIN_CHARS_MENSAJE,
    PATRON_EMAIL,
)


def validar_consulta(datos: dict) -> list[str]:
    """TODO: clasificación — valida nombre, email y mensaje antes de llamar a Gemini.

    Entrada: {"nombre": "Ana", "email": "ana@ejemplo.com", "mensaje": "..."}
    Salida OK: []
    Salida error: ["Nombre inválido: ...", "Email inválido: ...", ...]

    Ver README FASE 1, Tarea 1 y config.py (MIN/MAX_CHARS, PATRON_EMAIL).
    """
    # TODO: clasificación — implementar validación
    raise NotImplementedError(
        "Completa validar_consulta() — revisa config.py y data/consultas_ejemplo.json"
    )
