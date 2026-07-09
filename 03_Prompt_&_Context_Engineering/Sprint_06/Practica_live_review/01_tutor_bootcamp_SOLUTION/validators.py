"""validators.py — Validación de inputs y dominio (Fase 2).

Qué hace este módulo:
  - Capa 1: `validate_input()` — vacío, longitud, patrones sospechosos.
  - Capa 2: `parece_dominio_python()` — filtro didáctico antes del LLM.

Para qué sirve:
  - Rechazar ataques e inputs inválidos sin gastar tokens en Gemini.

Funciones a implementar (Fase 2):
  - validate_input, parece_dominio_python, rechazo_fuera_de_dominio
"""

from config import DOMINIO_KEYWORDS, MAX_INPUT_CHARS, PATRONES_SOSPECHOSOS


def validate_input(texto: str) -> list[str]:
    """Devuelve lista de errores (vacía = OK). Ver README Fase 2, Tarea 1."""
    errores: list[str] = []
    t = (texto or "").strip()
    if not t:
        errores.append("El mensaje no puede estar vacío.")
    if len(t) > MAX_INPUT_CHARS:
        errores.append(f"Mensaje demasiado largo (máx {MAX_INPUT_CHARS} caracteres).")
    t_lower = t.lower()
    for patron in PATRONES_SOSPECHOSOS:
        if patron in t_lower:
            errores.append(f"Patrón no permitido detectado: {patron!r}")
    return errores


def parece_dominio_python(texto: str) -> bool:
    """True si el mensaje parece relacionado con Python/bootcamp. Ver README Fase 2."""
    t = texto.lower()
    return any(k in t for k in DOMINIO_KEYWORDS)


def rechazo_fuera_de_dominio() -> str:
    """Mensaje fijo cuando la pregunta no encaja en el producto."""
    return (
        "Solo puedo ayudarte con Python y ejercicios del bootcamp. "
        "Reformula tu pregunta en ese contexto."
    )
