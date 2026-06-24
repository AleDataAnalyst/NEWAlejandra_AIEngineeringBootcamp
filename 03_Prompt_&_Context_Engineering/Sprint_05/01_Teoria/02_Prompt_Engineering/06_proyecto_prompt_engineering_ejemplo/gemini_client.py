# gemini_client.py — llamadas a Gemini (sin construir prompts aquí)

from google import genai
from google.genai import types

from config import MODEL, TEMPERATURE_JSON, TEMPERATURE_TEXTO
from gemini_auth import configurar_gemini_api_key

configurar_gemini_api_key()


def llamar_gemini_texto(prompt: str) -> str:
    client = genai.Client()
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(temperature=TEMPERATURE_TEXTO),
    )
    return (response.text or "").strip()


def llamar_gemini_json(prompt: str) -> str:
    client = genai.Client()
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=TEMPERATURE_JSON,
            response_mime_type="application/json",
        ),
    )
    return (response.text or "").strip()
