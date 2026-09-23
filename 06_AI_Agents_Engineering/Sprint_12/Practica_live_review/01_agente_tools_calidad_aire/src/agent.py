"""Orquestación pública — COMPLETA ESTE ARCHIVO.

Contrato:
  procesar_turno(estado, mensaje, max_steps=None) → estado
  run_demo(...) → estado
"""

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
    """Un mensaje → tools → JSON → done → traza (con tools)."""
    # Dado: mensaje vacío (no llames al LLM)
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

    # TODO [turno]: dentro de un try/except:
    #   1. texto_tools, traza_tools = run_tool_loop(mensaje, max_steps=max_steps)
    #   2. cambios = sintetizar_estado(estado, mensaje, texto_tools)
    #   3. estado = actualizar_estado(estado, cambios)
    #   4. si no hay respuesta → usa texto_tools
    #   5. estado = calcular_done(estado)
    #   6. append a traza: turno, mensaje, status "ok", done, tools=traza_tools
    #   En except:
    #   - error + respuesta amigable + traza status "error", tools=[]
    raise NotImplementedError(
        "Implementa procesar_turno (tools → JSON → done → traza). Consulta el README."
    )


def run_demo(
    mensajes: list[str] | None = None,
    max_turns: int | None = None,
    max_steps: int | None = None,
) -> dict[str, Any]:
    """Demo CLI con tope max_turns (y max_steps por turno)."""
    # TODO [demo]:
    #   1. msgs = list(mensajes) o config.DEMO_MENSAJES
    #   2. limit = max_turns o config.MAX_TURNS_DEFAULT
    #   3. estado = crear_estado(msgs[0] si hay)
    #   4. for mensaje in msgs[:limit]: break si done/error; procesar_turno(..., max_steps)
    #   5. Si cortaste por tope sin done → aviso en respuesta
    #   6. return estado
    raise NotImplementedError(
        "Implementa run_demo (bucle + max_turns). Consulta el README."
    )
