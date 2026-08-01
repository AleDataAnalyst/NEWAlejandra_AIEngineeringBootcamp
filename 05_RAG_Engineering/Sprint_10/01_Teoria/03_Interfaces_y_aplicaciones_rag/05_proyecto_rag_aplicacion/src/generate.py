"""Generación de respuestas con Gemini — Sprint 10.

Camino principal del bootcamp. Alternativa Hugging Face: ver teoría Bloque 1.
"""

from google import genai

from config import GEMINI_MODEL, GENERATION_TEMPERATURE

from .gemini_auth import configurar_gemini_api_key


def generar_respuesta(prompt: str) -> str:
    """Envía el prompt a Gemini y devuelve el texto de la respuesta."""
    configurar_gemini_api_key()
    client = genai.Client()

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config={"temperature": GENERATION_TEMPERATURE},
    )

    texto = response.text if response.text else ""
    return texto.strip()
