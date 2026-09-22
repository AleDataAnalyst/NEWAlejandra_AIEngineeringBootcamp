"""Orquestación pública — COMPLETA ESTE ARCHIVO.

Contrato:
  procesar_turno(estado, mensaje) → estado
  run_demo(...) → estado (demo CLI con max_turns)
"""

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
    # Dado: mensaje vacío (no llames al LLM ni pidas API key)
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

    # TODO [turno]: dentro de un try/except:
    #   1. cambios = preguntar_al_modelo(estado, mensaje)
    #   2. estado = actualizar_estado(estado, cambios)
    #   3. estado = calcular_done(estado)   ← Python decide done, no el LLM
    #   4. añade a estado["traza"] un dict con: turno, mensaje, status "ok", done
    #   En except Exception:
    #   - estado["error"] = str(e)
    #   - si no hay respuesta, pon un mensaje amigable
    #   - traza con status "error" y detail
    #   - return estado (no re-lances)
    raise NotImplementedError(
        "Implementa procesar_turno (LLM → actualizar → calcular_done → traza). "
        "Consulta el README."
    )


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
    # TODO [demo]:
    #   1. Si mensajes no es None → msgs = list(mensajes)
    #      si no → msgs = list(config.DEMO_MENSAJES)
    #   2. Si max_turns no es None → limit = max_turns
    #      si no → limit = config.MAX_TURNS_DEFAULT
    #   3. estado = crear_estado(msgs[0]) si hay msgs; si no, crear_estado("")
    #   4. for mensaje in msgs[:limit]:
    #        break si done o error
    #        estado = procesar_turno(estado, mensaje)
    #   5. Si no hay done/error y cortaste por el tope → aviso en respuesta
    #   6. return estado
    raise NotImplementedError(
        "Implementa run_demo (bucle de mensajes + max_turns). "
        "Consulta el README."
    )
