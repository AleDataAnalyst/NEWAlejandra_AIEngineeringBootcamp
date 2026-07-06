# prompts.py — plantillas y construcción de prompts

import json

ROLE_CLASIFICADOR = (
    "Eres un analista de tickets de soporte. "
    "Respondes únicamente con JSON válido según las instrucciones."
)

TASK_CLASIFICAR = """
Tarea: clasifica el mensaje del usuario.

Devuelve EXCLUSIVAMENTE un objeto JSON con estas claves:
- "category": una de soporte, facturacion, ventas, otro
- "priority": una de baja, media, alta
- "summary": resumen en una frase

Sin markdown ni texto fuera del JSON.
"""

PLANTILLA_FICHA_PRODUCTO = """
Eres un redactor de ficha de producto para ecommerce.

--- DATOS DEL PRODUCTO (JSON) ---
{producto_json}
--- FIN DATOS ---

Tarea: escribe una descripción comercial de 80-100 palabras en español.
No inventes características que no estén en el JSON.
"""

PLANTILLA_RECOMENDACION_CLIMA = """
Eres un asistente de bienestar urbano.

--- DATOS METEOROLÓGICOS ---
{weather_json}
--- FIN DATOS ---

Tarea: genera 4 recomendaciones prácticas para salir hoy (ropa, hidratación, horarios).
Formato: lista numerada, frases cortas. Idioma: español.
"""


def build_clasificacion_prompt(mensaje: str) -> str:
    return f"{ROLE_CLASIFICADOR}\n\n{TASK_CLASIFICAR}\n\nMensaje:\n{mensaje.strip()}\n"


def build_ficha_producto_prompt(producto: dict) -> str:
    producto_json = json.dumps(producto, ensure_ascii=False, indent=2)
    return PLANTILLA_FICHA_PRODUCTO.format(producto_json=producto_json)


def build_recomendacion_clima_prompt(weather: dict) -> str:
    weather_json = json.dumps(weather, ensure_ascii=False, indent=2)
    return PLANTILLA_RECOMENDACION_CLIMA.format(weather_json=weather_json)
