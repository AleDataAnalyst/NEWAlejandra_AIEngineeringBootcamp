# prompts.py — plantillas y construcción de prompts

PLANTILLA_RESUMEN = """
Eres un asistente que resume conversaciones de estudio.

Tarea: resume el texto en {max_puntos} puntos clave.
Reglas:
- no inventes datos
- conserva nombres, temas de estudio y preferencias del usuario
- devuelve solo la lista en texto plano

Texto:
{texto}
"""

PLANTILLA_ESTUDIO = """
Eres un tutor de AI Engineering. Respondes de forma clara y adaptada al nivel del alumno.

{perfil_bloque}

{faq_bloque}

{resumen_bloque}

{historial_bloque}

Pregunta actual del alumno:
{pregunta}
"""


def build_resumen_prompt(texto: str, max_puntos: int = 6) -> str:
    return PLANTILLA_RESUMEN.format(max_puntos=max_puntos, texto=texto.strip())


def build_profile_block(profile: dict) -> str:
    if not profile:
        return ""
    return (
        "--- PERFIL DEL ALUMNO ---\n"
        f"Nombre: {profile.get('name', 'desconocido')}\n"
        f"Idioma: {profile.get('language', 'español')}\n"
        f"Nivel: {profile.get('level', 'junior')}\n"
        f"Estilo: {profile.get('tone', 'claro')}\n"
        f"Tema de estudio: {profile.get('study_topic', 'general')}\n"
        "--- FIN PERFIL ---"
    )


def build_faq_block(faq_entries: list[dict]) -> str:
    if not faq_entries:
        return ""
    lines = ["--- FAQ (referencia seleccionada en Python) ---"]
    for entry in faq_entries:
        lines.append(f"P: {entry.get('question', '')}")
        lines.append(f"R: {entry.get('answer', '')}")
        lines.append("")
    lines.append("--- FIN FAQ ---")
    return "\n".join(lines)


def build_summary_block(summary: str) -> str:
    if not summary.strip():
        return ""
    return f"--- RESUMEN DE LA CONVERSACIÓN ---\n{summary.strip()}\n--- FIN RESUMEN ---"


def build_history_block(messages: list[dict]) -> str:
    if not messages:
        return ""
    lines = ["--- ÚLTIMOS TURNOS ---"]
    for msg in messages:
        role = msg.get("role", "user")
        text = msg.get("text", "")
        lines.append(f"{role}: {text}")
    lines.append("--- FIN TURNOS ---")
    return "\n".join(lines)


def build_study_prompt(
    *,
    pregunta: str,
    profile: dict,
    faq_entries: list[dict],
    summary: str,
    recent_messages: list[dict],
) -> str:
    return PLANTILLA_ESTUDIO.format(
        perfil_bloque=build_profile_block(profile),
        faq_bloque=build_faq_block(faq_entries),
        resumen_bloque=build_summary_block(summary),
        historial_bloque=build_history_block(recent_messages),
        pregunta=pregunta.strip(),
    ).strip()
