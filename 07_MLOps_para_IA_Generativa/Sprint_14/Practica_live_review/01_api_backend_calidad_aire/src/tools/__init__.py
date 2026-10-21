"""Allowlist de tools LangChain (@tool)."""

from src.tools.api_calidad_aire import API_consultar_calidad_aire
from src.tools.describir_imagen import describir_imagen
from src.tools.hora_actual import hora_actual
from src.tools.rag_guia import RAG_buscar_en_guia

TOOLS = [
    hora_actual,
    RAG_buscar_en_guia,
    API_consultar_calidad_aire,
    describir_imagen,
]

TOOL_BY_NAME = {t.name: t for t in TOOLS}


def ejecutar_tool(nombre: str, args: dict | None = None) -> str:
    """Ejecuta una tool de la allowlist; si no está, bloquea."""
    args = args or {}
    tool = TOOL_BY_NAME.get(nombre)
    if tool is None:
        return f"Error: tool '{nombre}' no está permitida."
    try:
        return str(tool.invoke(args))
    except Exception as e:  # noqa: BLE001
        return f"Error: {e}"
