# config.py — reglas y parámetros de generación

MODEL = "gemini-3-flash-preview"
TEMPERATURE_TEXTO = 0.3
TEMPERATURE_JSON = 0

CATEGORIAS = {"soporte", "facturacion", "ventas", "otro"}
PRIORIDADES = {"baja", "media", "alta"}

TONOS_VALIDOS = {"formal", "cercano", "directo"}
IDIOMAS_VALIDOS = {"español", "inglés", "francés"}

MAX_CHARS_PROMPT = 30_000
