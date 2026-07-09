"""prompts.py — Construcción de textos para enviar a Gemini.

Qué hace este módulo:
  - Ensambla strings (rol + instrucciones + contexto + pregunta).
  - Fase 1: `build_clasificacion_prompt()` para clasificar en JSON.
  - Fase 2: bloques de perfil, FAQ, historial y `build_chat_prompt()`.

Para qué sirve:
  - Separar el diseño del prompt de la lógica y de las llamadas a la API.
  - Aquí solo devuelves texto; no llamas a Gemini.

Funciones a implementar:
  - Fase 1: `build_clasificacion_prompt`
  - Fase 2: `build_perfil_block`, `build_faq_block`, `build_historial_block`, `build_chat_prompt`
"""

import json

ROLE_CLASIFICADOR = (
    "Eres un analista de consultas del bootcamp AI Engineering. "
    "Respondes únicamente con JSON válido según las instrucciones."
)

TASK_CLASIFICAR = """
Tarea: clasifica el mensaje del alumno sobre el bootcamp.

Devuelve EXCLUSIVAMENTE un objeto JSON con estas claves:
- "category": una de academico, tecnico, administrativo, otro
- "priority": una de baja, media, alta
- "summary": resumen en una frase

Sin markdown ni texto fuera del JSON.
"""

PLANTILLA_CHAT = """
Eres un asistente oficial del bootcamp AI Engineering. Respondes con claridad y sin inventar políticas.

{perfil_bloque}

{faq_bloque}

{historial_bloque}

Pregunta actual del alumno:
{pregunta}
"""


def build_clasificacion_prompt(mensaje: str) -> str:
    """TODO: clasificación — ensambla ROLE + TASK + mensaje (sin llamar a la API).

  Entrada: mensaje = "Mi GEMINI_API_KEY no funciona, ¿qué reviso?"
  Salida: str con ROLE_CLASIFICADOR, TASK_CLASIFICAR y el mensaje del alumno.
  Ver README FASE 1, Tarea 2.
    """
    
    # raise NotImplementedError("Implementa build_clasificacion_prompt()")

    return f"{ROLE_CLASIFICADOR}\n\n{TASK_CLASIFICAR}\n\nMensaje:\n{mensaje.strip()}\n"


def build_perfil_block(profile: dict) -> str:
    """TODO: contexto y chat — bloque de perfil del alumno.

  Entrada: profile = {"name": "Ana", "email": "...", "language": "español", ...}
  Salida: texto entre --- PERFIL DEL ALUMNO --- y --- FIN PERFIL ---, o "" si vacío.
  Ver README FASE 2, Tarea 2.
    """
    if not profile:
        return ""
    return (
        "--- PERFIL DEL ALUMNO ---\n"
        f"Nombre: {profile.get('name', 'desconocido')}\n"
        f"Email: {profile.get('email', '')}\n"
        f"Idioma: {profile.get('language', 'español')}\n"
        f"Nivel: {profile.get('level', 'junior')}\n"
        "--- FIN PERFIL ---"
    )

    # raise NotImplementedError("Implementa build_perfil_block()")


def build_faq_block(faq_entries: list[dict]) -> str:
    """TODO: contexto y chat — solo entradas seleccionadas (no todo faq.json).

  Entrada: lista con 0 o 1 dict del FAQ (salida de seleccionar_faq).
  Salida: bloque P:/R: entre delimitadores FAQ, o "" si la lista está vacía.
  Ver README FASE 2, Tarea 2.
    """
    if not faq_entries:
        return ""
    lines = ["--- FAQ BOOTCAMP (referencia seleccionada en Python) ---"]
    for entry in faq_entries:
        lines.append(f"P: {entry.get('question', '')}")
        lines.append(f"R: {entry.get('answer', '')}")
        lines.append("")
    lines.append("--- FIN FAQ ---")
    return "\n".join(lines)

    # raise NotImplementedError("Implementa build_faq_block()")


def build_historial_block(messages: list[dict]) -> str:
    """TODO: contexto y chat — últimos turnos (role + text).

  Entrada: [{"role": "user", "text": "..."}, {"role": "model", "text": "..."}]
  Salida: líneas "user: ..." / "model: ..." entre delimitadores, o "" si vacío.
  Ver README FASE 2, Tarea 2.
    """
    if not messages:
        return ""
    lines = ["--- ÚLTIMOS TURNOS ---"]
    for msg in messages:
        lines.append(f"{msg.get('role', 'user')}: {msg.get('text', '')}")
    lines.append("--- FIN TURNOS ---")
    return "\n".join(lines)

    # raise NotImplementedError("Implementa build_historial_block()")


def build_chat_prompt(
    *,
    pregunta: str,
    profile: dict,
    faq_entries: list[dict],
    recent_messages: list[dict],
) -> str:
    """TODO: contexto y chat — ensambla PLANTILLA_CHAT con los bloques anteriores.

  Entrada: pregunta actual + perfil + FAQ filtrado + ultimos_n(state, WINDOW).
  Salida: str listo para safe_generate_texto() en gemini_client.py.
  Ver README FASE 2, Tarea 2.
    """
    return PLANTILLA_CHAT.format(
        perfil_bloque=build_perfil_block(profile),
        faq_bloque=build_faq_block(faq_entries),
        historial_bloque=build_historial_block(recent_messages),
        pregunta=pregunta.strip(),
    ).strip()

    # raise NotImplementedError("Implementa build_chat_prompt()")
