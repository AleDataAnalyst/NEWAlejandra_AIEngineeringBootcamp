"""Orquestación pública — COMPLETA procesar_turno y run_demo.

HITL (`aprobar_plan`, `_aplicar_hitl`) viene DADO.
"""

from __future__ import annotations

from typing import Any

import config
from gemini_auth import configurar_gemini_api_key
from src.graph import invoke_tools_loop
from src.llm import sintetizar_estado
from src.state import actualizar_estado, calcular_done, crear_estado


def _aplicar_hitl(estado: dict[str, Any]) -> dict[str, Any]:
    """DADO: si hay plan ≥2 sin aprobar → pendiente_hitl (done sigue False)."""
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
    """DADO: decisión HITL desde Streamlit / CLI."""
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
    """Un mensaje → grafo → JSON → done/HITL → traza."""
    # Dado: mensaje vacío
    mensaje = (mensaje or "").strip()
    if not mensaje:
        nuevo = dict(estado)
        nuevo["respuesta"] = (
            "Escribe un mensaje (zona, contaminante, tipo de consulta…)."
        )
        return nuevo

    configurar_gemini_api_key()

    if not estado.get("pedido_original"):
        estado = {**estado, "pedido_original": mensaje}

    n = len(estado.get("traza") or []) + 1

    # TODO [turno]: dentro de try/except:
    #   1. texto_tools, traza_tools = invoke_tools_loop(mensaje, max_steps=max_steps)
    #   2. cambios = sintetizar_estado(estado, mensaje, texto_tools)
    #   3. estado = actualizar_estado(estado, cambios)
    #   4. si no hay respuesta → usa texto_tools
    #   5. estado = calcular_done(estado)
    #   6. estado = _aplicar_hitl(estado)
    #   7. append traza: turno, mensaje, status "ok", done, pendiente_hitl, tools
    #   En except: error + respuesta amigable + traza status "error", tools=[]
    raise NotImplementedError(
        "Implementa procesar_turno (grafo → JSON → HITL → traza). Consulta el README."
    )


def run_demo(
    mensajes: list[str] | None = None,
    max_turns: int | None = None,
    max_steps: int | None = None,
    auto_aprobar: bool = True,
) -> dict[str, Any]:
    """Demo CLI con max_turns; si pendiente_hitl y auto_aprobar → aprobar_plan(True)."""
    # TODO [demo]:
    #   1. msgs / limit / crear_estado
    #   2. for mensaje in msgs[:limit]: break si done/error; procesar_turno
    #   3. si pendiente_hitl y auto_aprobar → aprobar_plan(estado, True)
    #   4. aviso max_turns si cortaste sin done
    #   5. return estado
    raise NotImplementedError(
        "Implementa run_demo. Consulta el README."
    )
