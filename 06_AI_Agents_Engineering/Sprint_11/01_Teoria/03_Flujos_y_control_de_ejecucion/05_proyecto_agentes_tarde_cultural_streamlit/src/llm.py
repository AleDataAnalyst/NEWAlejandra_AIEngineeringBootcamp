"""Llamada a Gemini: un mensaje de usuario → patch JSON (sin `done`)."""

from __future__ import annotations

import json
import os
from typing import Any

from google import genai

import config
from src.state import leer_json

INSTRUCCIONES = """
Eres un planificador de tardes culturales.
No tienes bases de datos. Propón ideas genéricas (sin horarios inventados).

Responde SOLO con un JSON (sin markdown) con esta forma:
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

Reglas simples:
- No inventes preferencias que el usuario no haya dicho.
- Si faltan intereses, presupuesto o zona: plan=[], y pregunta (máximo 2 preguntas).
- No rellenes el plan hasta que haya intereses+presupuesto+zona y el usuario confirme (sí / adelante).
- Cuando cierres: plan con 2 a 4 ítems. duracion_horas es opcional; si falta, sugiere un número razonable (p. ej. 3).
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
