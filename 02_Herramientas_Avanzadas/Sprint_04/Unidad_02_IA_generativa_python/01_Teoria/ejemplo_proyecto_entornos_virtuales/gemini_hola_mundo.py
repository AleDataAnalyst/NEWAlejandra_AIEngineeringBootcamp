# Ejemplo de script para ejecutar nuestro proyecto
import os
import getpass

from dotenv import load_dotenv
from google import genai

load_dotenv()  # carga variables desde .env (si existe)

if not os.getenv("GEMINI_API_KEY"):
    os.environ["GEMINI_API_KEY"] = getpass.getpass(
        "Pega aquí tu GEMINI_API_KEY (input oculto): "
    )

print("GEMINI_API_KEY configurada:", "sí" if os.getenv("GEMINI_API_KEY") else "no")

client = genai.Client()
MODEL = "gemini-3-flash-preview"

response = client.models.generate_content(
    model=MODEL,
    contents="Resume en 3 frases qué es la IA generativa.",
)

print(response.text)
