"""Orquestación del agente (tools + JSON + done + traza)."""

from typing import Any

import config
from gemini_auth import configurar_gemini_api_key
from src.llm import run_tool_loop, sintetizar_estado
from src.state import actualizar_estado, calcular_done, crear_estado


def procesar_turno(
    estado: dict[str, Any],
    mensaje: str,
    max_steps: int | None = None,
) -> dict[str, Any]:
    """Procesa un mensaje: Fase 1 tools → Fase 2 JSON → done → traza."""
    configurar_gemini_api_key()
    mensaje = (mensaje or "").strip()
    if not mensaje:
        nuevo = dict(estado)
        nuevo["respuesta"] = (
            "Escribe un mensaje (zona, contaminante, tipo de consulta…)."
        )
        return nuevo

    if not estado.get("pedido_original"):
        estado = {**estado, "pedido_original": mensaje}

    n = len(estado.get("traza") or []) + 1
    try:
        texto_tools, traza_tools = run_tool_loop(mensaje, max_steps=max_steps)
        cambios = sintetizar_estado(estado, mensaje, texto_tools)
        estado = actualizar_estado(estado, cambios)
        if not estado.get("respuesta"):
            estado = {**estado, "respuesta": texto_tools}
        estado = calcular_done(estado)
        estado.setdefault("traza", []).append(
            {
                "turno": n,
                "mensaje": mensaje,
                "status": "ok",
                "done": estado.get("done"),
                "tools": traza_tools,
            }
        )
    except Exception as e:
        estado = dict(estado)
        estado["error"] = str(e)
        if not estado.get("respuesta"):
            estado["respuesta"] = (
                "No he podido continuar por un error técnico. "
                "Revisa la API key o la respuesta del modelo."
            )
        estado.setdefault("traza", []).append(
            {
                "turno": n,
                "mensaje": mensaje,
                "status": "error",
                "detail": str(e),
                "tools": [],
            }
        )
    return estado


def run_demo(
    mensajes: list[str] | None = None,
    max_turns: int | None = None,
    max_steps: int | None = None,
) -> dict[str, Any]:
    """Demo CLI: recorre mensajes con tope max_turns."""
    msgs = list(mensajes) if mensajes is not None else list(config.DEMO_MENSAJES)
    limit = max_turns if max_turns is not None else config.MAX_TURNS_DEFAULT
    estado = crear_estado(msgs[0] if msgs else "")

    for mensaje in msgs[:limit]:
        if estado.get("done") or estado.get("error"):
            break
        estado = procesar_turno(estado, mensaje, max_steps=max_steps)

    if not estado.get("done") and not estado.get("error"):
        if len(estado.get("traza") or []) >= limit:
            aviso = "He parado por max_turns; esto es lo que llevo del plan."
            prev = (estado.get("respuesta") or "").strip()
            estado["respuesta"] = f"{prev}\n\n{aviso}".strip() if prev else aviso
    return estado
