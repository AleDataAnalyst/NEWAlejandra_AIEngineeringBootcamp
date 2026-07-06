# logic.py — validar, decidir, devolver dict estructurado

from config import PATRON_CODIGO, PRIORIDAD_MAX, PRIORIDAD_MIN, VALID_TIPOS
from prompts import MSG_ERROR_INPUT, MSG_REGISTRO_OK, PLANTILLA_TAREA


def respuesta_ok(mensaje: str, data: dict | None = None) -> dict:
    return {"status": "ok", "mensaje": mensaje, "data": data or {}}


def respuesta_error(mensaje: str, errores: list[str]) -> dict:
    return {"status": "error", "mensaje": mensaje, "data": {"errores": errores}}


def validar_registro(datos: dict) -> list[str]:
    errores: list[str] = []

    if not isinstance(datos, dict):
        return ["El registro debe ser un dict."]

    if not str(datos.get("nombre", "")).strip():
        errores.append("Nombre inválido: no puede estar vacío.")

    codigo = str(datos.get("codigo", "")).strip()
    if codigo and PATRON_CODIGO.fullmatch(codigo) is None:
        errores.append("Código inválido: usa formato TKT-1234.")

    tipo = str(datos.get("tipo", "")).strip().lower()
    if tipo not in VALID_TIPOS:
        errores.append(f"Tipo inválido. Usa una de: {VALID_TIPOS}")

    prioridad = datos.get("prioridad")
    if not isinstance(prioridad, int) or not (PRIORIDAD_MIN <= prioridad <= PRIORIDAD_MAX):
        errores.append(
            f"Prioridad inválida: debe ser un entero {PRIORIDAD_MIN}-{PRIORIDAD_MAX}."
        )

    return errores


def procesar_registro(datos: dict) -> dict:
    errores = validar_registro(datos)
    if errores:
        return respuesta_error(MSG_ERROR_INPUT, errores)

    tipo = str(datos.get("tipo", "")).strip().lower()
    prioridad = datos.get("prioridad")
    mensaje = PLANTILLA_TAREA.format(tipo=tipo, prioridad=prioridad)

    return respuesta_ok(
        MSG_REGISTRO_OK,
        data={"mensaje_tarea": mensaje, "tipo": tipo, "prioridad": prioridad},
    )
