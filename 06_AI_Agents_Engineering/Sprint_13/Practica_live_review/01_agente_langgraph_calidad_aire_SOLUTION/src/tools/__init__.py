"""Allowlist: solo las tools de TOOL_REGISTRY se pueden ejecutar.

Antes de ejecutar, validar_args sanea los parámetros (tipos, límites, vacíos).
"""

from src.tools.api_calidad_aire import API_consultar_calidad_aire
from src.tools.hora_actual import hora_actual
from src.tools.rag_guia import RAG_buscar_en_guia

# Solo estas tools se pueden ejecutar (allowlist).
TOOL_REGISTRY = {
    "hora_actual": hora_actual,
    "RAG_buscar_en_guia": RAG_buscar_en_guia,
    "API_consultar_calidad_aire": API_consultar_calidad_aire,
}


def validar_args(nombre, args=None):
    """Guardrails antes de fn(**args).

    - hora_actual: no acepta args (devuelve {}).
    - RAG_buscar_en_guia: consulta como string (sin espacios extra).
    - API_consultar_calidad_aire: limite entero entre 1 y 10.
    """
    args = args or {}
    if nombre == "hora_actual":
        return {}
    if nombre == "RAG_buscar_en_guia":
        return {"consulta": str(args.get("consulta") or "").strip()}
    if nombre == "API_consultar_calidad_aire":
        try:
            limite = int(args.get("limite", 5))
        except (TypeError, ValueError):
            limite = 5
        return {"limite": max(1, min(limite, 10))}
    return args


def ejecutar_tool(nombre, args=None):
    """Si el nombre no está en el registro, no se ejecuta."""
    if nombre not in TOOL_REGISTRY:
        return f"Error: tool '{nombre}' no está permitida."
    limpios = validar_args(nombre, args)
    if nombre == "RAG_buscar_en_guia" and not limpios.get("consulta"):
        return "Error: la consulta de RAG no puede estar vacía."
    try:
        return TOOL_REGISTRY[nombre](**limpios)
    except Exception as e:
        return f"Error al ejecutar {nombre}: {e}"
