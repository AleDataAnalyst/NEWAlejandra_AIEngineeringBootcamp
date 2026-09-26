"""Allowlist — COMPLETA ESTE ARCHIVO.

Solo las tools de TOOL_REGISTRY se pueden ejecutar.
Antes de ejecutar, validar_args sanea los parámetros.
"""

from src.tools.api_calidad_aire import API_consultar_calidad_aire
from src.tools.hora_actual import hora_actual
from src.tools.rag_guia import RAG_buscar_en_guia

# TODO [allowlist]: registra las 3 tools con estos nombres exactos:
#   "hora_actual" → hora_actual
#   "RAG_buscar_en_guia" → RAG_buscar_en_guia
#   "API_consultar_calidad_aire" → API_consultar_calidad_aire
TOOL_REGISTRY = {}


def validar_args(nombre, args=None):
    """Guardrails antes de fn(**args).

    - hora_actual → {}
    - RAG_buscar_en_guia → {"consulta": str limpio}
    - API_consultar_calidad_aire → {"limite": int entre 1 y 10}
    """
    # TODO [validar]: implementa las tres ramas de arriba
    raise NotImplementedError("Implementa validar_args en src/tools/__init__.py")


def ejecutar_tool(nombre, args=None):
    """Si el nombre no está en el registro, no se ejecuta."""
    # TODO [ejecutar]:
    #   1. Si nombre not in TOOL_REGISTRY → return Error: tool no permitida
    #   2. limpios = validar_args(nombre, args)
    #   3. Si RAG y consulta vacía → Error
    #   4. try: return TOOL_REGISTRY[nombre](**limpios)
    #      except → return Error al ejecutar ...
    raise NotImplementedError("Implementa ejecutar_tool en src/tools/__init__.py")
