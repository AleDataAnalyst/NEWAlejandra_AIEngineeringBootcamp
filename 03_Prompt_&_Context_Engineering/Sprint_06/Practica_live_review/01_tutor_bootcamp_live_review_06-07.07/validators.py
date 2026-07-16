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
    """TODO: Fase 2 — devuelve lista de errores (vacía = OK).

    Reglas: vacío, MAX_INPUT_CHARS, PATRONES_SOSPECHOSOS en config.py.

    Ver README Fase 2, Tarea 1.
    """
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

    # raise NotImplementedError("Implementa validate_input()")


def parece_dominio_python(texto: str) -> bool:
    """TODO: Fase 2 — True si el mensaje parece de Python/bootcamp.

    Usa DOMINIO_KEYWORDS de config.py.

    Ver README Fase 2, Tarea 2.
    """

    t = texto.lower()
    return any(k in t for k in DOMINIO_KEYWORDS)

    # raise NotImplementedError("Implementa parece_dominio_python()")


def rechazo_fuera_de_dominio() -> str:
    """TODO: Fase 2 — mensaje fijo cuando la pregunta no encaja en el producto.

    Ver README Fase 2, Tarea 2.
    """
    
    return (
        "Solo puedo ayudarte con Python y ejercicios del bootcamp. "
        "Reformula tu pregunta en ese contexto."
    )
    
    # raise NotImplementedError("Implementa rechazo_fuera_de_dominio()")
