"""Estado del agente: preferencias, plan, done, traza."""

from __future__ import annotations

import copy
import json
from typing import Any


def crear_estado(pedido: str = "") -> dict[str, Any]:
    """Estado al empezar la conversación."""
    return {
        "objetivo": "Planificar una tarde cultural",
        "pedido_original": pedido,
        "preferencias": {
            "intereses": None,
            "presupuesto": None,
            "zona": None,
            "duracion_horas": None,
        },
        "plan": [],
        "respuesta": "",
        "done": False,
        "error": None,
        "traza": [],
    }


def tenemos_datos_minimos(estado: dict[str, Any]) -> bool:
    """¿Ya hay intereses, presupuesto y zona?"""
    prefs = estado["preferencias"]
    intereses = prefs.get("intereses") or []
    return (
        len(intereses) >= 1
        and bool(prefs.get("presupuesto"))
        and bool(prefs.get("zona"))
    )


def leer_json(texto: str) -> dict[str, Any]:
    """Convierte el texto del LLM en un diccionario."""
    texto = texto.strip()
    if texto.startswith("```"):
        lineas = texto.splitlines()
        texto = "\n".join(lineas[1:-1]).strip()
    return json.loads(texto)


def actualizar_estado(estado: dict[str, Any], cambios: dict[str, Any]) -> dict[str, Any]:
    """Aplica preferencias, plan y respuesta. No toca `done`."""
    nuevo = copy.deepcopy(estado)
    prefs_nuevas = cambios.get("preferencias") or {}
    for clave, valor in prefs_nuevas.items():
        if valor is not None:
            nuevo["preferencias"][clave] = valor
    if isinstance(cambios.get("plan"), list):
        nuevo["plan"] = cambios["plan"]
    if "respuesta" in cambios:
        nuevo["respuesta"] = cambios["respuesta"]
    return nuevo


def calcular_done(estado: dict[str, Any]) -> dict[str, Any]:
    """Python decide si la tarea ha terminado."""
    nuevo = copy.deepcopy(estado)
    plan = nuevo.get("plan") or []
    nuevo["done"] = tenemos_datos_minimos(nuevo) and len(plan) >= 2
    return nuevo
