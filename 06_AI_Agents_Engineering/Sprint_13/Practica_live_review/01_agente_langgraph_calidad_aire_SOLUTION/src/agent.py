"""Orquestación: grafo LangGraph + JSON + HITL + done + traza."""

from __future__ import annotations

from typing import Any

import config
from gemini_auth import configurar_gemini_api_key
from src.graph import invoke_tools_loop
from src.llm import sintetizar_estado
from src.state import actualizar_estado, calcular_done, crear_estado


def _aplicar_hitl(estado: dict[str, Any]) -> dict[str, Any]:
    nuevo = dict(estado)
    plan = nuevo.get("plan") or []
    if len(plan) >= 2 and not nuevo.get("plan_aprobado"):
        nuevo["pendiente_hitl"] = True
        nuevo["done"] = False
        aviso = (
            "\n\n_(Plan listo: aprueba o rechaza en la barra lateral antes de cerrar.)_"
        )
        resp = (nuevo.get("respuesta") or "").rstrip()
        if "aprueba o rechaza" not in resp.lower():
            nuevo["respuesta"] = resp + aviso
    else:
        nuevo["pendiente_hitl"] = False
    return nuevo


def aprobar_plan(estado: dict[str, Any], aprobado: bool) -> dict[str, Any]:
    nuevo = dict(estado)
    nuevo["plan_aprobado"] = bool(aprobado)
    nuevo["pendiente_hitl"] = False
    if aprobado:
        nuevo = calcular_done(nuevo)
        if nuevo.get("done"):
            prev = (nuevo.get("respuesta") or "").strip()
            cierre = "Plan aprobado. ¡Listo!"
            nuevo["respuesta"] = f"{prev}\n\n{cierre}".strip() if prev else cierre
    else:
        nuevo["plan"] = []
        nuevo["done"] = False
        nuevo["plan_aprobado"] = False
        nuevo["respuesta"] = (
            "Plan rechazado. Indica qué cambiar (zona, contaminante, tipo) "
            "y propongo otro."
        )
    return nuevo


def procesar_turno(
    estado: dict[str, Any],
    mensaje: str,
    max_steps: int | None = None,
) -> dict[str, Any]:
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
        texto_tools, traza_tools = invoke_tools_loop(mensaje, max_steps=max_steps)
        cambios = sintetizar_estado(estado, mensaje, texto_tools)
        estado = actualizar_estado(estado, cambios)
        if not estado.get("respuesta"):
            estado = {**estado, "respuesta": texto_tools}
        estado = calcular_done(estado)
        estado = _aplicar_hitl(estado)
        estado.setdefault("traza", []).append(
            {
                "turno": n,
                "mensaje": mensaje,
                "status": "ok",
                "done": estado.get("done"),
                "pendiente_hitl": estado.get("pendiente_hitl"),
                "tools": traza_tools,
            }
        )
    except Exception as e:  # noqa: BLE001
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
    auto_aprobar: bool = True,
) -> dict[str, Any]:
    msgs = list(mensajes) if mensajes is not None else list(config.DEMO_MENSAJES)
    limit = max_turns if max_turns is not None else config.MAX_TURNS_DEFAULT
    estado = crear_estado(msgs[0] if msgs else "")

    for mensaje in msgs[:limit]:
        if estado.get("done") or estado.get("error"):
            break
        estado = procesar_turno(estado, mensaje, max_steps=max_steps)
        if estado.get("pendiente_hitl") and auto_aprobar:
            estado = aprobar_plan(estado, True)

    if not estado.get("done") and not estado.get("error"):
        if len(estado.get("traza") or []) >= limit:
            aviso = "He parado por max_turns; esto es lo que llevo del plan."
            prev = (estado.get("respuesta") or "").strip()
            estado["respuesta"] = f"{prev}\n\n{aviso}".strip() if prev else aviso
    return estado
