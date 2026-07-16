"""Autenticación con la API de Gemini.

Carga GEMINI_API_KEY desde .env; si no existe, la solicita con getpass.
"""

import getpass
import os

from dotenv import load_dotenv

_configured = False


def configurar_gemini_api_key() -> None:
    """Asegura que GEMINI_API_KEY está disponible para el cliente de Gemini.

    Lee el archivo .env la primera vez que se llama. Si no hay clave,
    la pide por consola (input oculto).
    """
    global _configured
    if _configured:
        return

    load_dotenv()

    if not os.getenv("GEMINI_API_KEY"):
        os.environ["GEMINI_API_KEY"] = getpass.getpass(
            "Pega aquí tu GEMINI_API_KEY (input oculto): "
        )

    print(
        "GEMINI_API_KEY configurada:",
        "sí" if os.getenv("GEMINI_API_KEY") else "no",
    )
    _configured = True
