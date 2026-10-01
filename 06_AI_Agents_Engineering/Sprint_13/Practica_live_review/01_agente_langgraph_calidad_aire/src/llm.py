"""Gemini helpers: declaraciones, síntesis JSON. DADO — no hace falta editar.

El bucle agent ↔ tools vive en graph.py (LangGraph).
"""

from __future__ import annotations

import json
import os
from typing import Any

from google import genai
from google.genai import types

import config
from src.state import leer_json

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


def declaraciones() -> list[types.FunctionDeclaration]:
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


def gen_config_tools() -> types.GenerateContentConfig:
    return types.GenerateContentConfig(
        tools=[types.Tool(function_declarations=declaraciones())],
        temperature=config.TEMPERATURE,
        automatic_function_calling=types.AutomaticFunctionCallingConfig(
            disable=True
        ),
    )


def preview(texto: str, n: int = 160) -> str:
    texto = texto.replace("\n", " ")
    return texto if len(texto) <= n else texto[: n - 3] + "..."


def sintetizar_estado(
    estado: dict[str, Any],
    mensaje_usuario: str,
    respuesta_tools: str,
) -> dict[str, Any]:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Falta GEMINI_API_KEY")

    estado_para_prompt = {
        k: v
        for k, v in estado.items()
        if k not in {"traza", "pendiente_hitl", "plan_aprobado"}
    }
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
