"""Construcción del prompt RAG — Sprint 10 (COMPLETAR).

Separa instrucciones fijas, contexto recuperado y pregunta del usuario.
"""

# TODO: instrucciones restrictivas para calidad del aire / meteorología Madrid
INSTRUCCIONES_RAG = """Eres un asistente que responde preguntas sobre calidad del aire
y datos meteorológicos de Madrid (open data).

Reglas:
- Responde ÚNICAMENTE con la información del contexto proporcionado.
- Si el contexto no contiene información suficiente, indícalo explícitamente
  (no inventes magnitudes, estaciones ni datos fuera del corpus).
- Cuando cites un hecho, menciona la fuente si aparece en el contexto.
- No inventes respuestas a preguntas ajenas al dominio (p. ej. geografía general).
"""


def build_rag_prompt(contexto: str, pregunta: str) -> str:
    """Ensambla el prompt completo para el LLM.

    Debe incluir: instrucciones + CONTEXTO + PREGUNTA + marcador de RESPUESTA.
    """
    # TODO: devolver el string ensamblado (sin llamar al LLM aquí)
    raise NotImplementedError("Implementa build_rag_prompt() en src/prompts.py")
