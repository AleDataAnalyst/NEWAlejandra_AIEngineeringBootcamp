"""Estado de producto (API) y helpers."""

import copy
from typing import Any


def crear_estado(pedido: str = "") -> dict[str, Any]:
    """Plantilla del estado de sesión en RAM (FastAPI)."""
    return {
        "objetivo": "Orientar una consulta de calidad del aire (multiagente LangGraph)",
        "pedido_original": pedido,
        "pedido": pedido,
        "notas_diagnostico": "",
        "notas_practico": "",
        "respuesta": "",
        "plan": [],
        "siguiente": "",
        "iteracion": 0,
        "log": [],
        "traza_tools": [],
        "done": False,
        "error": None,
        "pendiente_hitl": False,
        "plan_aprobado": False,
        "traza": [],
    }


def estado_desde_grafo(
    resultado: dict[str, Any], base: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Fusiona la salida del grafo sobre el estado de producto."""
    nuevo = copy.deepcopy(base) if base else crear_estado()
    for clave in (
        "pedido",
        "notas_diagnostico",
        "notas_practico",
        "respuesta",
        "plan",
        "siguiente",
        "iteracion",
        "log",
        "traza_tools",
        "done",
        "plan_aprobado",
        "pendiente_hitl",
    ):
        if clave in resultado:
            nuevo[clave] = resultado[clave]
    if resultado.get("pedido") and not nuevo.get("pedido_original"):
        nuevo["pedido_original"] = resultado["pedido"]
    return nuevo
