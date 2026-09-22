"""Gemini: dos fases por turno.

Fase 1 — run_tool_loop:
  Loop manual modelo ↔ tools (function calling).
  Nosotros ejecutamos las tools, guardamos traza y limitamos con max_steps.
  El AFC del SDK va desactivado a propósito (ver _gen_config_tools).

Fase 2 — sintetizar_estado:
  Segunda llamada sin tools: el modelo devuelve JSON
  (preferencias / plan / respuesta). El código calcula "done" después.
"""

from __future__ import annotations

import json
import os
from typing import Any

from google import genai
from google.genai import types

import config
from src.state import leer_json
from src.tools import TOOL_REGISTRY, ejecutar_tool

INSTRUCCIONES_TOOLS = """
Eres un planificador de tardes culturales en Madrid.
Puedes usar estas tools cuando haga falta:
- hora_actual: fecha/hora real.
- RAG_buscar_en_guia: consejos y normas de la guía local (no inventes el corpus).
- API_consultar_eventos_madrid: eventos del catálogo (API o fallback); no inventes eventos.

Reglas:
- Usa tools antes de afirmar horarios, normas de la guía o listados de eventos.
- Responde en español, claro y breve.
- Cuando tengas información suficiente, propone un plan concreto de tarde (2-4 actividades).
""".strip()

INSTRUCCIONES_JSON = """
A partir del ESTADO, el MENSAJE del usuario y la RESPUESTA_TOOLS del asistente,
devuelve SOLO un JSON (sin markdown) con esta forma:
{
  "preferencias": {
    "intereses": ["..."] o null,
    "presupuesto": "gratis_o_barato" o "medio" o "alto" o null,
    "zona": "..." o null,
    "duracion_horas": numero o null
  },
  "plan": [],
  "respuesta": "texto corto para el usuario"
}

Reglas:
- No inventes preferencias que el usuario no haya dicho.
- Si faltan intereses, presupuesto o zona: plan=[] y pregunta lo que falte (máx. 2 preguntas).
- Si ya hay datos mínimos y la respuesta_tools propone actividades: rellena plan con 2-4 ítems.
- No incluyas "done": lo calcula el código.
""".strip()


def _declaraciones() -> list[types.FunctionDeclaration]:
    """Catálogo de tools que ve el modelo (nombre, descripción, parámetros).

    No ejecuta nada: es solo el "menú". La implementación está en src/tools/.
    """
    # Menú para Gemini. EL código real está en TOOL_REGISTRY.
    return [
        types.FunctionDeclaration(
            name="hora_actual",
            description="Devuelve la fecha y hora local actuales.",
            parameters_json_schema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        types.FunctionDeclaration(
            name="RAG_buscar_en_guia",
            description=(
                "Busca en la guía cultural local (museos gratis, zonas, tips de planificación)."
            ),
            parameters_json_schema={
                "type": "object",
                "properties": {
                    "consulta": {
                        "type": "string",
                        "description": "Pregunta o palabras clave.",
                    }
                },
                "required": ["consulta"],
            },
        ),
        types.FunctionDeclaration(
            name="API_consultar_eventos_madrid",
            description=(
                "Trae N eventos del catálogo cultural de Madrid (open data o fallback). "
                "Devuelve un resumen corto."
            ),
            parameters_json_schema={
                "type": "object",
                "properties": {
                    "limite": {
                        "type": "integer",
                        "description": "Máximo de eventos a devolver (1-10).",
                    },
                },
                "required": [],
            },
        ),
    ]


def _gen_config_tools() -> types.GenerateContentConfig:
    """Config de Gemini para la Fase 1: tools + temperatura + AFC off.

    Empaqueta el menú de `_declaraciones()` y desactiva el AFC del SDK
    para que el loop lo controlemos nosotros para aprender cómo funciona por dentro (traza, allowlist, max_steps).
    """
    return types.GenerateContentConfig(
        tools=[types.Tool(function_declarations=_declaraciones())],
        temperature=config.TEMPERATURE,
        # Desactivamos el AFC del SDK: el loop tools lo hacemos nosotros
        # (traza, allowlist, max_steps). Si AFC estuviera on, Gemini
        # intentaría ejecutar tools por su cuenta y perderíamos ese control.
        automatic_function_calling=types.AutomaticFunctionCallingConfig(
            disable=True
        ),
    )


def _preview(texto: str, n: int = 160) -> str:
    """Recorta un texto largo para guardarlo en la traza (solo un adelanto)."""
    texto = texto.replace("\n", " ")
    return texto if len(texto) <= n else texto[: n - 3] + "..."


def run_tool_loop(
    mensaje_usuario: str,
    max_steps: int | None = None,
) -> tuple[str, list[dict[str, Any]]]:
    """Fase 1: habla con Gemini pidiendo/ejecutando tools hasta un texto final.

    Devuelve (texto_del_asistente, traza_de_tools).
    Para si no hay más function_calls o se alcanza max_steps.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Falta GEMINI_API_KEY")

    limit = max_steps if max_steps is not None else config.MAX_STEPS_DEFAULT
    client = genai.Client(api_key=api_key)
    gen_config = _gen_config_tools()
    traza = []

    # Historial de la conversación con el modelo (roles: user / model / tool).
    # Cada vuelta del loop añade mensajes aquí.
    historial: list[types.Content] = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(
                    text=INSTRUCCIONES_TOOLS + "\n\nMENSAJE:\n" + mensaje_usuario
                )
            ],
        )
    ]

    for step in range(1, limit + 1):
        # 1) Pedir al modelo: texto final o una/varias tool calls.
        response = client.models.generate_content(
            model=config.GEMINI_MODEL,
            contents=historial,
            config=gen_config,
        )
        # El modelo puede pedir 0, 1 o varias tools en el mismo paso.
        # function_calls puede ser None → lo tratamos como lista vacía.
        llamadas = list(response.function_calls or [])
        if not llamadas:
            # Sin tools: ya tenemos la respuesta en texto.
            return (response.text or "").strip(), traza

        # 2) Ejecutar cada tool pedida (allowlist + traza).
        historial.append(response.candidates[0].content)
        respuestas_tools: list[types.Part] = []
        for llamada in llamadas:
            nombre = llamada.name
            args = dict(llamada.args or {})
            if nombre not in TOOL_REGISTRY:
                resultado = f"Error: tool '{nombre}' no está permitida."
                status = "blocked"
            else:
                resultado = ejecutar_tool(nombre, args)
                status = "error" if resultado.startswith("Error") else "ok"

            traza.append(
                {
                    "step": step,
                    "tool": nombre,
                    "args": args,
                    "status": status,
                    "preview": _preview(resultado),
                }
            )
            respuestas_tools.append(
                types.Part.from_function_response(
                    name=nombre,
                    response={"result": resultado},
                )
            )
        # 3) Devolver resultados al historial para la siguiente vuelta.
        historial.append(types.Content(role="tool", parts=respuestas_tools))

    return (
        f"He parado por max_steps={limit}. Esto es lo que pude avanzar con las tools.",
        traza,
    )


def sintetizar_estado(
    estado: dict[str, Any],
    mensaje_usuario: str,
    respuesta_tools: str,
) -> dict[str, Any]:
    """Fase 2: sin tools, pide a Gemini un JSON (preferencias / plan / respuesta).

    Usa el estado actual, el mensaje del usuario y el texto de la Fase 1.
    No calcula "done": eso lo hace el código en state.py después.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Falta GEMINI_API_KEY")

    estado_para_prompt = {k: v for k, v in estado.items() if k != "traza"}
    prompt = (
        INSTRUCCIONES_JSON
        + "\n\nESTADO:\n"
        + json.dumps(estado_para_prompt, ensure_ascii=False, indent=2)
        + "\n\nMENSAJE:\n"
        + mensaje_usuario
        + "\n\nRESPUESTA_TOOLS:\n"
        + respuesta_tools
        + "\n\nDevuelve el JSON:"
    )
    client = genai.Client(api_key=api_key)
    respuesta = client.models.generate_content(
        model=config.GEMINI_MODEL,
        contents=prompt,
        config={"temperature": config.TEMPERATURE},
    )
    return leer_json((respuesta.text or "").strip())
