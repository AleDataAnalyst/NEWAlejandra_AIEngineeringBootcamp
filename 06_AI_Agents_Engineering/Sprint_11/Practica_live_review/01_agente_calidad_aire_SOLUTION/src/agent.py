"""Orquestación pública: procesar_turno (estado + done + traza). — SOLUCIÓN"""

from typing import Any

import config
from gemini_auth import configurar_gemini_api_key
from src.llm import preguntar_al_modelo
from src.state import actualizar_estado, calcular_done, crear_estado


def procesar_turno(estado: dict[str, Any], mensaje: str) -> dict[str, Any]:
    """Un mensaje de usuario → LLM → actualizar estado → calcular done.

    Ejemplo:
        estado = crear_estado("")
        estado = procesar_turno(estado, "Me interesa el NO2 en el centro.")
        # Mira estado["preferencias"], estado["respuesta"], estado["done"], ...

    Añade una entrada a `traza`. Si falla el JSON/API, rellena `error` y no tumba.
    """
    mensaje = (mensaje or "").strip()
    if not mensaje:
        nuevo = dict(estado)
        nuevo["respuesta"] = "Escribe un mensaje (zona, contaminante, tipo de consulta…)."
        return nuevo

    configurar_gemini_api_key()

    if not estado.get("pedido_original"):
        estado = {**estado, "pedido_original": mensaje}

    # Número de este turno (1, 2, 3…)
    traza_actual = estado.get("traza", [])
    n = len(traza_actual) + 1
    try:
        cambios = preguntar_al_modelo(estado, mensaje)
        estado = actualizar_estado(estado, cambios)
        estado = calcular_done(estado)
        estado.setdefault("traza", []).append(
            {
                "turno": n,
                "mensaje": mensaje,
                "status": "ok",
                "done": estado.get("done"),
            }
        )
    except Exception as e:  # noqa: BLE001
        estado = dict(estado)
        estado["error"] = str(e)
        if not estado.get("respuesta"):
            estado["respuesta"] = (
                "No he podido continuar por un error técnico. "
                "Revisa la API key o el JSON del modelo."
            )
        estado.setdefault("traza", []).append(
            {
                "turno": n,
                "mensaje": mensaje,
                "status": "error",
                "detail": str(e),
            }
        )
    return estado


def run_demo(
    mensajes: list[str] | None = None,
    max_turns: int | None = None,
) -> dict[str, Any]:
    """Ejecuta una conversación completa (demo CLI) con tope de turnos.

    Ejemplos:
        estado = run_demo()                 # guion de config.DEMO_MENSAJES
        estado = run_demo(max_turns=2)      # mismo guion, solo 2 turnos
        # Mira estado["done"], estado["plan"], estado["traza"], ...
    """
    # 1) Qué mensajes usamos
    if mensajes is not None:
        msgs = list(mensajes)
    else:
        msgs = list(config.DEMO_MENSAJES)

    # 2) Tope de turnos
    if max_turns is not None:
        limit = max_turns
    else:
        limit = config.MAX_TURNS_DEFAULT

    # 3) Estado inicial
    if msgs:
        estado = crear_estado(msgs[0])
    else:
        estado = crear_estado("")

    # 4) Un turno por mensaje (hasta el tope o hasta done/error)
    for mensaje in msgs[:limit]:
        if estado.get("done") or estado.get("error"):
            break
        estado = procesar_turno(estado, mensaje)

    # 5) Si cortamos por max_turns, avisar en la respuesta
    terminado = bool(estado.get("done") or estado.get("error"))
    turnos_hechos = len(estado.get("traza", []))
    corto_por_limite = turnos_hechos >= limit or len(msgs) > limit

    if not terminado and corto_por_limite:
        aviso = "He parado por max_turns; esto es lo que llevo del plan."
        prev = (estado.get("respuesta") or "").strip()
        if prev:
            estado["respuesta"] = prev + "\n\n" + aviso
        else:
            estado["respuesta"] = aviso

    return estado
