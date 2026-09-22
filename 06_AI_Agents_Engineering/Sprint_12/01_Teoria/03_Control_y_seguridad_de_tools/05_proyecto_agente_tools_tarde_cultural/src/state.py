"""Estado del agente: preferencias, plan, done, traza.

Aquí no se habla con el LLM. Solo se crea, actualiza y valida
el diccionario de estado que pasa de turno en turno.
"""

from __future__ import annotations

import copy
import json
from typing import Any


def crear_estado(pedido: str = "") -> dict[str, Any]:
    """Crea el estado inicial vacío (plantilla del agente).

    Opcionalmente guarda el primer pedido del usuario en pedido_original.
    """
    return {
        "objetivo": "Planificar una tarde cultural con tools",
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
    """True si ya hay intereses, presupuesto y zona (lo mínimo para un plan)."""
    prefs = estado["preferencias"]
    intereses = prefs.get("intereses") or []
    return (
        len(intereses) >= 1
        and bool(prefs.get("presupuesto"))
        and bool(prefs.get("zona"))
    )


def leer_json(texto: str) -> dict[str, Any]:
    """Convierte texto del modelo a dict JSON.

    Si el LLM envuelve el JSON en un bloque ```...```, lo quita antes.
    """
    texto = texto.strip()
    if texto.startswith("```"):
        lineas = texto.splitlines()
        texto = "\n".join(lineas[1:-1]).strip()
    return json.loads(texto)


def actualizar_estado(estado: dict[str, Any], cambios: dict[str, Any]) -> dict[str, Any]:
    """Fusiona el JSON de sintetizar_estado sobre una copia del estado.

    Solo pisa preferencias con valores no None; actualiza plan y respuesta
    si vienen en cambios. No toca done ni traza.
    """
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
    """Marca done=True si hay datos mínimos y un plan con al menos 2 actividades.

    Lo decide el código, no el LLM (no existe tool marcar_done).
    """
    nuevo = copy.deepcopy(estado)
    plan = nuevo.get("plan") or []
    nuevo["done"] = tenemos_datos_minimos(nuevo) and len(plan) >= 2
    return nuevo
