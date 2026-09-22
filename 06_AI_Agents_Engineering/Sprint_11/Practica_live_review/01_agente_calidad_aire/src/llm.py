"""Llamada a Gemini: un mensaje de usuario → patch JSON (sin `done`)."""

import json
import os
from typing import Any

from google import genai

import config
from src.state import leer_json

INSTRUCCIONES = """
Eres un orientador de consultas sobre calidad del aire en Madrid.
NO tienes bases de datos, RAG ni mediciones en vivo.
NO inventes valores numéricos, umbrales oficiales ni lecturas de estaciones.

Tu trabajo: aclarar la consulta del usuario y, al cerrar, proponer un plan
de consulta genérico (pasos / qué mirar), no una respuesta con datos reales.

Responde SOLO con un JSON (sin markdown) con esta forma:
{
  "preferencias": {
    "zona": "string o null",
    "contaminante": "string o null (ej. NO2, PM10, magnitud 83)",
    "tipo_consulta": "que_mide" o "interpretar" o "comparar" o "general" o null
  },
  "plan": [],
  "respuesta": "texto corto para el usuario"
}

Reglas simples:
- No inventes preferencias que el usuario no haya dicho.
- Si faltan zona, contaminante o tipo_consulta: plan=[], y pregunta (máximo 2 preguntas).
- No rellenes el plan hasta tener zona+contaminante+tipo_consulta y que el usuario confirme (sí / adelante).
- Cuando cierres: plan con 2 a 4 ítems orientativos (ej. "revisar qué mide el contaminante",
  "mirar la estación de la zona", "comparar con el umbral cuando tengas datos").
- Si el usuario pide un dato concreto ahora: explica que en este ejercicio
  no hay mediciones ni corpus, y ofrece el plan de consulta en su lugar.
- No incluyas el campo "done": lo calcula el código.
""".strip()


def preguntar_al_modelo(estado: dict[str, Any], mensaje_usuario: str) -> dict[str, Any]:
    """Una llamada a Gemini → dict con cambios."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Falta GEMINI_API_KEY")

    estado_para_prompt = {k: v for k, v in estado.items() if k != "traza"}
    prompt = (
        INSTRUCCIONES
        + "\n\nESTADO ACTUAL:\n"
        + json.dumps(estado_para_prompt, ensure_ascii=False, indent=2)
        + "\n\nMENSAJE DEL USUARIO:\n"
        + mensaje_usuario
        + "\n\nDevuelve el JSON:"
    )

    client = genai.Client(api_key=api_key)
    respuesta = client.models.generate_content(
        model=config.GEMINI_MODEL,
        contents=prompt,
        config={"temperature": config.TEMPERATURE},
    )
    texto = (respuesta.text or "").strip()
    return leer_json(texto)
