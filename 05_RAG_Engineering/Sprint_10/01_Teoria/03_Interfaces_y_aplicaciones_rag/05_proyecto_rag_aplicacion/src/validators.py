"""Validación pre-LLM — Sprint 10.

Continuidad con Sprint 6: rechazar inputs inválidos antes de gastar tokens.
"""

PATRONES_SOSPECHOSOS = [
    "ignora instrucciones",
    "ignore previous",
    "actúa como",
    "system prompt",
]


def validar_pregunta(pregunta: str) -> tuple[bool, str | None]:
    """Devuelve (ok, mensaje_error)."""
    texto = (pregunta or "").strip()
    if not texto:
        return False, "La pregunta no puede estar vacía."
    if len(texto) > 2000:
        return False, "La pregunta es demasiado larga."

    lower = texto.lower()
    for patron in PATRONES_SOSPECHOSOS:
        if patron in lower:
            return False, "Entrada rechazada (patrón sospechoso detectado)."

    return True, None


def validar_contexto(contexto: str) -> tuple[bool, str | None]:
    """Comprueba que hay contexto recuperado antes de llamar al LLM."""
    if not contexto or contexto.strip() == "(sin fragmentos recuperados)":
        return False, "No se recuperó contexto. Revisa el índice o la pregunta."
    return True, None
