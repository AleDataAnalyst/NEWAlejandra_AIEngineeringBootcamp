"""Gemini: dos fases por turno.

Idea clave (léelo antes del código):
  Fase 1 — run_tool_loop: el modelo PIDE tools; Python las EJECUTA (allowlist).
  Fase 2 — sintetizar_estado: el modelo devuelve JSON (prefs / plan / respuesta).
  "done" NO lo decide el LLM: lo calcula Python en state.calcular_done.

El bloque _declaraciones / _gen_config_tools es catálogo del SDK Gemini.
No hace falta tocarlo: solo describe las tools al modelo y apaga el AFC
(automatic function calling) para hacer el loop a mano.
"""

import json
import os
from typing import Any

from google import genai
from google.genai import types

import config
from src.state import leer_json
from src.tools import TOOL_REGISTRY, ejecutar_tool

INSTRUCCIONES_TOOLS = """
Eres un asistente de calidad del aire en Madrid.
Puedes usar estas tools cuando haga falta:
- hora_actual: fecha/hora real.
- RAG_buscar_en_guia: consejos y códigos de la guía local (no inventes el corpus).
- API_consultar_calidad_aire: mediciones open data (API o fallback); no inventes valores.

Reglas:
- Usa tools antes de afirmar códigos de magnitud, estaciones o mediciones.
- Responde en español, claro y breve.
- No inventes umbrales oficiales ni cifras si la tool no las aportó.
- Cuando tengas información suficiente, propone un plan de consulta (2-4 pasos).
""".strip()

INSTRUCCIONES_JSON = """
A partir del ESTADO, el MENSAJE del usuario y la RESPUESTA_TOOLS del asistente,
devuelve SOLO un JSON (sin markdown) con esta forma:
{
  "preferencias": {
    "zona": "..." o null,
    "contaminante": "..." o null,
    "tipo_consulta": "que_mide" o "interpretar" o "comparar" o "general" o null
  },
  "plan": [],
  "respuesta": "texto corto para el usuario"
}

Reglas:
- No inventes preferencias que el usuario no haya dicho.
- Si faltan zona, contaminante o tipo_consulta: plan=[] y pregunta lo que falte (máx. 2 preguntas).
- Si ya hay datos mínimos: rellena plan con 2-4 pasos de consulta concretos.
- No incluyas "done": lo calcula el código.
""".strip()


def _declaraciones() -> list[types.FunctionDeclaration]:
    """Catálogo de tools para Gemini (nombres + args). DADO — no lo edites."""
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
                "Busca en la guía local de calidad del aire "
                "(magnitudes, estaciones, cómo interpretar datos)."
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
            name="API_consultar_calidad_aire",
            description=(
                "Trae un resumen de mediciones de calidad del aire en Madrid "
                "(open data tiempo real o fallback). Devuelve texto corto."
            ),
            parameters_json_schema={
                "type": "object",
                "properties": {
                    "limite": {
                        "type": "integer",
                        "description": "Máximo de filas a resumir (1-10).",
                    },
                },
                "required": [],
            },
        ),
    ]


def _gen_config_tools() -> types.GenerateContentConfig:
    """Config Gemini con tools + AFC desactivado (loop manual). DADO."""
    return types.GenerateContentConfig(
        tools=[types.Tool(function_declarations=_declaraciones())],
        temperature=config.TEMPERATURE,
        automatic_function_calling=types.AutomaticFunctionCallingConfig(
            disable=True
        ),
    )


def _preview(texto: str, n: int = 160) -> str:
    """Recorta el resultado de una tool para la traza (no saturar el JSON)."""
    texto = texto.replace("\n", " ")
    return texto if len(texto) <= n else texto[: n - 3] + "..."


def run_tool_loop(
    mensaje_usuario: str,
    max_steps: int | None = None,
) -> tuple[str, list[dict[str, Any]]]:
    """Fase 1: Gemini pide tools; Python ejecuta (allowlist) hasta texto o max_steps.

    Flujo por step:
      1) generate_content → ¿pide function_calls?
      2) Si no → devolvemos el texto final + traza.
      3) Si sí → por cada llamada: allowlist / ejecutar_tool → status ok|error|blocked
      4) Devolvemos los resultados al modelo y repetimos (tope = max_steps).
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Falta GEMINI_API_KEY")

    limit = max_steps if max_steps is not None else config.MAX_STEPS_DEFAULT
    client = genai.Client(api_key=api_key)
    gen_config = _gen_config_tools()
    traza = []

    # Historial de la conversación modelo↔tools (formato del SDK).
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
        response = client.models.generate_content(
            model=config.GEMINI_MODEL,
            contents=historial,
            config=gen_config,
        )
        # Si no pide tools, ya tenemos la respuesta en texto.
        llamadas = list(response.function_calls or [])
        if not llamadas:
            return (response.text or "").strip(), traza

        # Guardamos lo que dijo el modelo (incluye las function_calls).
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
            # El SDK espera function_response con el resultado de cada tool.
            respuestas_tools.append(
                types.Part.from_function_response(
                    name=nombre,
                    response={"result": resultado},
                )
            )
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

    DADO. Aquí no hay function calling: solo texto → JSON → leer_json.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Falta GEMINI_API_KEY")

    # No mandamos la traza al prompt (puede ser larga); el resto del estado sí.
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
