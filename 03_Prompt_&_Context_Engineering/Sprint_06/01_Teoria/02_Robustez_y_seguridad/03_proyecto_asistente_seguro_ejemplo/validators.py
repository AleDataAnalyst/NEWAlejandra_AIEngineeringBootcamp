# validators.py — validación de inputs y dominio

from config import DOMINIO_KEYWORDS, MAX_INPUT_CHARS, PATRONES_SOSPECHOSOS


def validate_input(texto: str) -> list[str]:
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
    t = texto.lower()
    return any(k in t for k in DOMINIO_KEYWORDS)


def rechazo_fuera_de_dominio() -> str:
    return (
        "Solo puedo ayudarte con Python y ejercicios del bootcamp. "
        "Reformula tu pregunta en ese contexto."
    )
