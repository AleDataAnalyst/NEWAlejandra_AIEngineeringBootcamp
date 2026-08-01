"""Generación de respuestas con Gemini — Sprint 10 (COMPLETAR)."""

from google import genai

from config import GEMINI_MODEL, GENERATION_TEMPERATURE
from .gemini_auth import configurar_gemini_api_key


def generar_respuesta(prompt: str) -> str:
    """Envía el prompt a Gemini y devuelve el texto de la respuesta."""
    # TODO:
    # 1. configurar_gemini_api_key()
    # 2. client = genai.Client()
    # 3. client.models.generate_content(model=GEMINI_MODEL, contents=prompt,
    #       config={"temperature": GENERATION_TEMPERATURE})
    # 4. return (response.text or "").strip()
    raise NotImplementedError("Implementa generar_respuesta() en src/generate.py")
