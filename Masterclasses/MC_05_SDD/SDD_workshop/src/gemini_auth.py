"""Autenticación con la API de Gemini.

Carga GEMINI_API_KEY desde .env (raíz del proyecto) antes de embed/retriever/generate.
Si no hay clave, la pide por consola (input oculto).
"""

import getpass
import os
from pathlib import Path

from dotenv import load_dotenv

_configured = False
_ROOT = Path(__file__).resolve().parents[1]


def configurar_gemini_api_key() -> None:
    global _configured
    if _configured:
        return

    load_dotenv(_ROOT / ".env")

    if not os.getenv("GEMINI_API_KEY"):
        os.environ["GEMINI_API_KEY"] = getpass.getpass(
            "Pega aquí tu GEMINI_API_KEY (input oculto): "
        )

    print(
        "GEMINI_API_KEY configurada:",
        "sí" if os.getenv("GEMINI_API_KEY") else "no",
    )
    _configured = True
