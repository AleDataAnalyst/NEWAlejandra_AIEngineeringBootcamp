"""config.py — Constantes y reglas globales del asistente.

Qué hace este módulo:
  - Define modelo Gemini, temperaturas, límites de caracteres/tokens.
  - Lista categorías y prioridades permitidas (whitelist).
  - Guarda mensajes estándar de éxito y error.

Para qué sirve:
  - Un solo sitio para cambiar parámetros sin tocar la lógica de cada función.
  - Lo importan `validators.py`, `logic.py` y `gemini_client.py`.

Qué NO debes hacer aquí:
  - Normalmente no modificas este archivo en la práctica (salvo experimentos opcionales).
"""

import re

MODEL = "gemini-3-flash-preview"
TEMPERATURE_TEXTO = 0.3
TEMPERATURE_JSON = 0

CATEGORIAS = {"academico", "tecnico", "administrativo", "otro"}
PRIORIDADES = {"baja", "media", "alta"}

WINDOW = 6
MAX_TOKENS_INPUT = 8_000
MAX_CHARS_MENSAJE = 2_000
MIN_CHARS_MENSAJE = 10

PATRON_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

MSG_ERROR_VALIDACION = "Consulta inválida"
MSG_CLASIFICACION_OK = "Clasificación completada"
MSG_CHAT_OK = "Respuesta generada"
