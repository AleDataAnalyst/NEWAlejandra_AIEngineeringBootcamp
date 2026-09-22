"""Orquestación pública: procesar_turno (estado + done + traza)."""

from __future__ import annotations

from typing import Any

import config
from gemini_auth import configurar_gemini_api_key
from src.llm import preguntar_al_modelo
from src.state import actualizar_estado, calcular_done, crear_estado


def procesar_turno(estado: dict[str, Any], mensaje: str) -> dict[str, Any]:
    """Un mensaje de usuario → LLM → actualizar estado → calcular done.

    Añade una entrada a `traza`. Si falla el JSON/API, rellena `error` y no tumba.
    """
    configurar_gemini_api_key()
    mensaje = (mensaje or "").strip()
    if not mensaje:
        nuevo = dict(estado)
        nuevo["respuesta"] = "Escribe un mensaje (intereses, presupuesto, zona…)."
        return nuevo

    if not estado.get("pedido_original"):
        estado = {**estado, "pedido_original": mensaje}

    n = len(estado.get("traza") or []) + 1
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
    except Exception as e:  # noqa: BLE001 — mostrar error al alumno
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
    """Ejecuta una conversación completa (demo CLI) con tope de turnos."""
    msgs = list(mensajes) if mensajes is not None else list(config.DEMO_MENSAJES)
    limit = max_turns if max_turns is not None else config.MAX_TURNS_DEFAULT
    estado = crear_estado(msgs[0] if msgs else "")

    for mensaje in msgs[:limit]:
        if estado.get("done") or estado.get("error"):
            break
        estado = procesar_turno(estado, mensaje)

    if not estado.get("done") and not estado.get("error"):
        if len(estado.get("traza") or []) >= limit or len(msgs) > limit:
            aviso = "He parado por max_turns; esto es lo que llevo del plan."
            prev = (estado.get("respuesta") or "").strip()
            estado["respuesta"] = f"{prev}\n\n{aviso}".strip() if prev else aviso
    return estado
