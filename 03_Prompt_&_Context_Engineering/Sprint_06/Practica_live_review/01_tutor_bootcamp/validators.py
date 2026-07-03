"""validators.py — Validación de inputs y dominio (Fase 2).

Qué hace este módulo:
  - Capa 1: `validate_input()` — vacío, longitud, patrones sospechosos.
  - Capa 2: `parece_dominio_python()` — filtro didáctico antes del LLM.

Para qué sirve:
  - Rechazar ataques e inputs inválidos sin gastar tokens en Gemini.

Funciones a implementar (Fase 2):
  - validate_input, parece_dominio_python, rechazo_fuera_de_dominio
"""


def validate_input(texto: str) -> list[str]:
    """TODO: Fase 2 — devuelve lista de errores (vacía = OK).

    Reglas: vacío, MAX_INPUT_CHARS, PATRONES_SOSPECHOSOS en config.py.

    Ver README Fase 2, Tarea 1.
    """
    raise NotImplementedError("Implementa validate_input()")


def parece_dominio_python(texto: str) -> bool:
    """TODO: Fase 2 — True si el mensaje parece de Python/bootcamp.

    Usa DOMINIO_KEYWORDS de config.py.

    Ver README Fase 2, Tarea 2.
    """
    raise NotImplementedError("Implementa parece_dominio_python()")


def rechazo_fuera_de_dominio() -> str:
    """TODO: Fase 2 — mensaje fijo cuando la pregunta no encaja en el producto.

    Ver README Fase 2, Tarea 2.
    """
    raise NotImplementedError("Implementa rechazo_fuera_de_dominio()")
