# config.py — configuración del asistente y perfiles

MODEL = "gemini-3-flash-preview"
TEMPERATURE = 0.3
WINDOW = 6
MAX_TOKENS_INPUT = 8_000

ASSISTANT_CONFIG_DEFAULT = {
    "model": MODEL,
    "temperature": TEMPERATURE,
    "perfil_activo": "mentor",
    "max_turnos_historial": WINDOW,
    "idioma_respuesta": "español",
    "max_palabras": 200,
}

PERFILES = {
    "junior": {
        "rol": (
            "Eres un compañero de estudio amable. "
            "Explicas con ejemplos cortos y vocabulario accesible."
        ),
        "nivel_explicacion": "básico",
    },
    "senior": {
        "rol": (
            "Eres un ingeniero senior. "
            "Vas al grano y asumes conocimientos previos de Python y APIs."
        ),
        "nivel_explicacion": "avanzado",
    },
    "mentor": {
        "rol": (
            "Eres un mentor pedagógico. "
            "Guías con pasos y preguntas reflexivas, sin abrumar."
        ),
        "nivel_explicacion": "intermedio",
    },
}
