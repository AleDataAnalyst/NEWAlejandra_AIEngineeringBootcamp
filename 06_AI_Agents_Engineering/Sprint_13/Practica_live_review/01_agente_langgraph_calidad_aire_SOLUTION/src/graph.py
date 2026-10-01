"""Grafo LangGraph: ciclo ReAct agent ↔ tools (calidad del aire)."""

from __future__ import annotations

import os
from typing import Any, Literal, TypedDict

from google import genai
from google.genai import types
from langgraph.graph import END, START, StateGraph

import config
from src.llm import INSTRUCCIONES_TOOLS, gen_config_tools, preview
from src.tools import TOOL_REGISTRY, ejecutar_tool


class LoopState(TypedDict):
    mensaje: str
    max_steps: int
    pasos: int
    historial: list
    traza: list
    texto_final: str
    pending_calls: list


def _nodo_agent(estado: LoopState) -> dict[str, Any]:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Falta GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)
    historial = list(estado.get("historial") or [])
    if not historial:
        historial = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(
                        text=INSTRUCCIONES_TOOLS
                        + "\n\nMENSAJE:\n"
                        + estado["mensaje"]
                    )
                ],
            )
        ]

    response = client.models.generate_content(
        model=config.GEMINI_MODEL,
        contents=historial,
        config=gen_config_tools(),
    )
    llamadas = list(response.function_calls or [])
    if not llamadas:
        return {
            "historial": historial,
            "pending_calls": [],
            "texto_final": (response.text or "").strip(),
        }

    historial.append(response.candidates[0].content)
    pending = [{"name": c.name, "args": dict(c.args or {})} for c in llamadas]
    return {
        "historial": historial,
        "pending_calls": pending,
        "texto_final": "",
    }


def _nodo_tools(estado: LoopState) -> dict[str, Any]:
    historial = list(estado.get("historial") or [])
    traza = list(estado.get("traza") or [])
    paso = int(estado.get("pasos") or 0) + 1
    partes: list[types.Part] = []

    for llamada in estado.get("pending_calls") or []:
        nombre = llamada["name"]
        args = dict(llamada.get("args") or {})
        if nombre not in TOOL_REGISTRY:
            resultado = f"Error: tool '{nombre}' no está permitida."
            status = "blocked"
        else:
            resultado = ejecutar_tool(nombre, args)
            status = "error" if str(resultado).startswith("Error") else "ok"

        traza.append(
            {
                "step": paso,
                "tool": nombre,
                "args": args,
                "status": status,
                "preview": preview(str(resultado)),
            }
        )
        partes.append(
            types.Part.from_function_response(
                name=nombre,
                response={"result": resultado},
            )
        )

    historial.append(types.Content(role="tool", parts=partes))
    return {
        "historial": historial,
        "traza": traza,
        "pasos": paso,
        "pending_calls": [],
    }


def _router(estado: LoopState) -> Literal["tools", "__end__"]:
    if int(estado.get("pasos") or 0) >= int(estado.get("max_steps") or 1):
        return "__end__"
    if estado.get("pending_calls"):
        return "tools"
    return "__end__"


def _router_tras_tools(estado: LoopState) -> Literal["agent", "__end__"]:
    if int(estado.get("pasos") or 0) >= int(estado.get("max_steps") or 1):
        return "__end__"
    return "agent"


def build_graph():
    grafo = StateGraph(LoopState)
    grafo.add_node("agent", _nodo_agent)
    grafo.add_node("tools", _nodo_tools)
    grafo.add_edge(START, "agent")
    grafo.add_conditional_edges(
        "agent",
        _router,
        {"tools": "tools", "__end__": END},
    )
    grafo.add_conditional_edges(
        "tools",
        _router_tras_tools,
        {"agent": "agent", "__end__": END},
    )
    return grafo.compile()


_APP = None


def get_app():
    global _APP
    if _APP is None:
        _APP = build_graph()
    return _APP


def invoke_tools_loop(
    mensaje: str,
    max_steps: int | None = None,
) -> tuple[str, list[dict[str, Any]]]:
    limit = max_steps if max_steps is not None else config.MAX_STEPS_DEFAULT
    final = get_app().invoke(
        {
            "mensaje": mensaje,
            "max_steps": limit,
            "pasos": 0,
            "historial": [],
            "traza": [],
            "texto_final": "",
            "pending_calls": [],
        }
    )
    texto = (final.get("texto_final") or "").strip()
    traza = list(final.get("traza") or [])
    if not texto and int(final.get("pasos") or 0) >= limit:
        texto = (
            f"He parado por max_steps={limit}. "
            "Esto es lo que pude avanzar con las tools."
        )
    return texto, traza
