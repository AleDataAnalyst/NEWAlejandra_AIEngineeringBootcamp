"""Estado del agente: preferencias de consulta, plan, done, traza."""

import copy
import json
from typing import Any


def crear_estado(pedido: str = "") -> dict[str, Any]:
    """Estado al empezar la conversación."""
    return {
        "objetivo": "Orientar una consulta sobre calidad del aire (Madrid)",
        "pedido_original": pedido,
        "preferencias": {
            "zona": None,
            "contaminante": None,
            "tipo_consulta": None,
        },
        "plan": [],
        "respuesta": "",
        "done": False,
        "error": None,
        "traza": [],
    }


def tenemos_datos_minimos(estado: dict[str, Any]) -> bool:
    """¿Ya hay zona, contaminante y tipo de consulta?"""
    prefs = estado["preferencias"]
    return (
        bool(prefs.get("zona"))
        and bool(prefs.get("contaminante"))
        and bool(prefs.get("tipo_consulta"))
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
