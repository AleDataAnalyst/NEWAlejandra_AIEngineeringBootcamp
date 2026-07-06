# config.py — límites y parámetros del asistente

MODEL = "gemini-3-flash-preview"
TEMPERATURE = 0.3
TEMPERATURE_RESUMEN = 0.2

# Ventana de mensajes recientes enviados al modelo
WINDOW = 6

# Cada cuántos mensajes (user+model) se intenta actualizar el resumen
RESUMIR_CADA = 8

# Umbral didáctico de tokens de entrada (no es límite oficial del modelo)
MAX_TOKENS_INPUT = 8_000
